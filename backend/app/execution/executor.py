import os
import uuid
import json
import shutil
import subprocess
import re
from typing import List, Dict, Any, Tuple, Optional
from app.core.config import settings

def to_wsl_path(win_path: str) -> str:
    """Translates a Windows file path into its corresponding WSL mount path."""
    p = win_path.replace("\\", "/")
    if len(p) >= 3 and p[1] == ":" and p[2] == "/":
        drive = p[0].lower()
        p = f"/mnt/{drive}/{p[3:]}"
    return p

def sanitize_traceback(tb_text: str, wsl_workspace_path: str) -> str:
    """Filters absolute workspace directories out of tracebacks for security."""
    if not tb_text:
        return ""
    # Remove absolute container workspace references
    tb_text = tb_text.replace(wsl_workspace_path + "/", "")
    tb_text = tb_text.replace("/workspace/", "")
    # General clean up of full host directory structure
    pattern = r"/mnt/[a-z]/[^ \n]*/backend/app/scratch/[^ \n]*/"
    tb_text = re.sub(pattern, "", tb_text)
    return tb_text

def run_in_sandbox(
    code: str,
    language: str,
    function_name: str,
    test_cases: List[Dict[str, Any]],
    challenge_slug: Optional[str] = None,
    custom_inputs: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Executes user Python code securely inside an isolated Docker container via WSL.
    Returns standard execution report.
    """
    if language != "python":
        return {
            "status": "FAILED",
            "stdout": "",
            "stderr": f"Unsupported language: {language}",
            "exit_code": 1,
            "runtime_ms": 0,
            "error_type": "UnsupportedLanguage"
        }

    task_id = str(uuid.uuid4())
    
    # Establish workspace directories on Windows host
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    scratch_dir = os.path.join(project_root, "app", "scratch", task_id)
    os.makedirs(scratch_dir, exist_ok=True)
    
    solution_path = os.path.join(scratch_dir, "solution.py")
    config_path = os.path.join(scratch_dir, "test_config.json")
    harness_dest = os.path.join(scratch_dir, "harness.py")
    
    # Write code draft and execution configurations
    with open(solution_path, "w", encoding="utf-8") as f:
        f.write(code)
        
    test_config = {
        "function_name": function_name,
        "challenge_slug": challenge_slug,
        "custom_inputs": custom_inputs,
        "test_cases": [
            {
                "id": str(tc.get("id")),
                "input": str(tc.get("input_data")),
                "expected": str(tc.get("expected_output")),
                "evaluation_type": tc.get("evaluation_type", "EXACT"),
                "tolerance": tc.get("tolerance", 1e-4),
                "metric": tc.get("metric"),
                "threshold": tc.get("threshold")
            }
            for tc in test_cases
        ]
    }
    
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(test_config, f, indent=2)
        
    # Copy harness.py script to temp directory
    harness_src = os.path.join(os.path.dirname(__file__), "harness.py")
    shutil.copy(harness_src, harness_dest)
    
    # Translate paths to WSL
    wsl_scratch_dir = to_wsl_path(scratch_dir)
    container_name = f"neuracode-run-{task_id}"
    
    # Formulate WSL docker run command with resource constraints
    cmd = [
        "wsl", "-d", "Ubuntu", "-u", "root",
        "docker", "run",
        "--name", container_name,
        "--network", "none",
        "--memory", settings.EXECUTION_MEMORY_LIMIT,
        "--cpus", str(settings.EXECUTION_CPU_LIMIT),
        "--pids-limit", str(settings.EXECUTION_PIDS_LIMIT),
        "--tmpfs", "/tmp:rw,size=16m,mode=1777",
        "--security-opt=no-new-privileges",
        "-v", f"{wsl_scratch_dir}:/workspace",
        "-w", "/workspace",
        "neuracode-executor",
        "python3", "harness.py"
    ]
    
    result_report = {
        "status": "COMPLETED",
        "stdout": "",
        "stderr": "",
        "exit_code": 0,
        "runtime_ms": 0,
        "error_type": None,
        "tests": []
    }
    
    import time
    start_time = time.time()
    
    try:
        # Run container. Add 10 seconds of headroom for container creation/WSL cold boot
        # Stdin redirected to DEVNULL prevents stdin waiting deadlock hangs
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            timeout=settings.EXECUTION_TIMEOUT_SECONDS + 10
        )
        
        runtime_ms = int((time.time() - start_time) * 1000)
        result_report["runtime_ms"] = runtime_ms
        result_report["exit_code"] = proc.returncode
        
        # Check if the command was killed by internal alarm (exits with code 124)
        if proc.returncode == 124:
            result_report["status"] = "TIMEOUT"
            result_report["error_type"] = "TimeoutExpired"
            result_report["stderr"] = f"Execution timed out. Program exceeded limit of {settings.EXECUTION_TIMEOUT_SECONDS}s."
            result_report["runtime_ms"] = settings.EXECUTION_TIMEOUT_SECONDS * 1000
        else:
            stdout_raw = proc.stdout.strip() if proc.stdout else ""
            stderr_raw = proc.stderr.strip() if proc.stderr else ""
            
            if proc.returncode != 0:
                result_report["status"] = "FAILED"
                result_report["stderr"] = sanitize_traceback(stderr_raw, wsl_scratch_dir)
                
            json_parsed = False
            if stdout_raw:
                lines = stdout_raw.splitlines()
                for line in reversed(lines):
                    if line.startswith("{") and line.endswith("}"):
                        try:
                            harness_out = json.loads(line)
                            result_report["tests"] = harness_out.get("tests", [])
                            result_report["visualization"] = harness_out.get("visualization")
                            
                            user_stdout = "\n".join(lines[:-1]) if len(lines) > 1 else ""
                            result_report["stdout"] = user_stdout
                            
                            if harness_out.get("status") == "error":
                                result_report["status"] = "FAILED"
                                result_report["error_type"] = harness_out.get("error_type")
                                result_report["stderr"] = sanitize_traceback(harness_out.get("stderr"), wsl_scratch_dir)
                            elif harness_out.get("status") == "TIMEOUT":
                                result_report["status"] = "TIMEOUT"
                                result_report["error_type"] = "TimeoutExpired"
                                result_report["stderr"] = harness_out.get("stderr")
                                
                            json_parsed = True
                            break
                        except Exception:
                            pass
                
                if not json_parsed:
                    result_report["stdout"] = stdout_raw
                    result_report["status"] = "FAILED"
                    result_report["stderr"] = sanitize_traceback(stderr_raw, wsl_scratch_dir)
                
    except subprocess.TimeoutExpired:
        result_report["status"] = "TIMEOUT"
        result_report["error_type"] = "TimeoutExpired"
        result_report["stderr"] = f"Execution timed out. Program exceeded limit of {settings.EXECUTION_TIMEOUT_SECONDS}s."
        result_report["runtime_ms"] = settings.EXECUTION_TIMEOUT_SECONDS * 1000
        
        subprocess.run(["wsl", "-d", "Ubuntu", "-u", "root", "docker", "kill", container_name], capture_output=True)
        
    except Exception as err:
        result_report["status"] = "FAILED"
        result_report["error_type"] = type(err).__name__
        result_report["stderr"] = str(err)
        
    finally:
        # Unconditional cleanup of container and folder
        subprocess.run(["wsl", "-d", "Ubuntu", "-u", "root", "docker", "rm", "-f", container_name], capture_output=True)
        shutil.rmtree(scratch_dir, ignore_errors=True)
        
    return result_report
