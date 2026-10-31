import sys
import os
import json
import time

# Ensure python knows where the app package is
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.execution.executor import run_in_sandbox

# Import challenge lists
from app.challenges.python_for_ai import challenges as python_challenges
from app.challenges.mathematics import challenges as math_challenges
from app.challenges.machine_learning import challenges as ml_challenges
from app.challenges.deep_learning import challenges as dl_challenges
from app.challenges.computer_vision import challenges as cv_challenges
from app.challenges.nlp_transformers import challenges as nlp_challenges
from app.challenges.genai_rag import challenges as genai_challenges
from app.challenges.agents_mlops import challenges as agent_challenges

def validate_all_challenges():
    print("NEURACODE CHALLENGE VALIDATION")
    print("=" * 45)
    
    categories_map = {
        "Python for AI": python_challenges,
        "Mathematics": math_challenges,
        "Machine Learning": ml_challenges,
        "Deep Learning": dl_challenges,
        "Computer Vision": cv_challenges,
        "NLP": nlp_challenges,
        "Transformers": nlp_challenges, # NLP covers transformers in modules
        "Generative AI": genai_challenges,
        "RAG": genai_challenges,        # GenAI covers RAG in modules
        "AI Agents": agent_challenges,
        "MLOps": agent_challenges       # Agent covers MLOps in modules
    }
    
    # Track unique slugs
    seen_slugs = set()
    total_validated = 0
    failures = 0
    
    for category_name, challenge_list in categories_map.items():
        print(f"\nCategory: {category_name}")
        print("-" * 35)
        
        # Filter challenges belonging to this category
        category_challenges = [c for c in challenge_list if c["category"] == category_name]
        if not category_challenges:
            # If no direct match (e.g. transformers or RAG is a sub-category in the combined modules)
            category_challenges = [c for c in challenge_list if c["category"] in [category_name, category_name.split()[0]]]
            
        # Deduplicate challenges in case we process the same list twice (like nlp_challenges for NLP/Transformers)
        unique_category_challenges = []
        for c in category_challenges:
            if c["slug"] not in seen_slugs:
                seen_slugs.add(c["slug"])
                unique_category_challenges.append(c)
                
        for challenge in unique_category_challenges:
            title = challenge["title"]
            slug = challenge["slug"]
            func_name = challenge["function_name"]
            ref_sol = challenge["reference_solution"]
            eval_type = challenge["evaluation_type"]
            
            print(f"Validating: {title} ({slug})... ", end="", flush=True)
            
            # 1. Schema Validation
            required_keys = ["title", "slug", "difficulty", "category", "starter_code", "tests", "hints", "reference_solution", "function_name"]
            missing = [k for k in required_keys if k not in challenge]
            if missing:
                print(f"FAILED\n   -> Missing keys: {missing}")
                failures += 1
                continue
                
            if len(challenge["tests"]) == 0:
                print("FAILED\n   -> No test cases defined.")
                failures += 1
                continue
                
            # 2. Format tests
            test_cases_list = [
                {
                    "id": str(idx),
                    "input_data": t["input_data"],
                    "expected_output": t["expected_output"],
                    "evaluation_type": t.get("evaluation_type", eval_type),
                    "tolerance": t.get("tolerance", 1e-4),
                    "metric": t.get("metric"),
                    "threshold": t.get("threshold")
                }
                for idx, t in enumerate(challenge["tests"])
            ]
            
            # 3. Execute Reference Solution
            try:
                res = run_in_sandbox(
                    code=ref_sol,
                    language="python",
                    function_name=func_name,
                    test_cases=test_cases_list
                )
            except Exception as ex:
                print(f"FAILED (Sandbox exception: {ex})")
                failures += 1
                continue
                
            if res.get("status") == "TIMEOUT":
                print("FAILED (Execution timed out)")
                failures += 1
                continue
                
            if res.get("status") == "FAILED" and not res.get("tests"):
                print(f"FAILED (Syntax/Compilation Error)\nStderr:\n{res.get('stderr')}")
                failures += 1
                continue
                
            # Check individual tests
            sandbox_tests = res.get("tests", [])
            failed_tests = [t for t in sandbox_tests if t.get("status") != "passed"]
            
            if failed_tests:
                print(f"FAILED (Reference solution failed {len(failed_tests)}/{len(sandbox_tests)} tests)")
                for ft in failed_tests:
                    print(f"   -> Test index {ft['id']} failed. Error: {ft.get('error')}")
                failures += 1
                continue
                
            # 4. Execute Garbage Code (should fail/error)
            garbage_code = f"def {func_name}(*args, **kwargs):\n    return 'garbage_incorrect_value'\n"
            try:
                garbage_res = run_in_sandbox(
                    code=garbage_code,
                    language="python",
                    function_name=func_name,
                    test_cases=test_cases_list
                )
                garbage_passed = all(t.get("status") == "passed" for t in garbage_res.get("tests", []))
                if garbage_passed and len(test_cases_list) > 0:
                    # If all tests passed with garbage code, the tests aren't catching incorrect code!
                    print("FAILED (Garbage code passed all tests!)")
                    failures += 1
                    continue
            except Exception:
                # Exceptions on garbage code execution are fine
                pass
                
            print("PASSED")
            total_validated += 1
            
            # Small cooldown to prevent overwhelming docker mounts
            time.sleep(0.05)
            
    print("\n" + "=" * 45)
    print(f"Total Challenges Validated: {total_validated}")
    print(f"Failures Detected: {failures}")
    
    if failures > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    validate_all_challenges()
