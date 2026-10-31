import sys
import os
import json
import ast
import traceback
import math
import signal

# Define evaluation strategies
class BaseEvaluator:
    def evaluate(self, actual, expected, tolerance=1e-4, **kwargs) -> tuple[bool, str | None]:
        raise NotImplementedError

class ExactEvaluator(BaseEvaluator):
    def evaluate(self, actual, expected, tolerance=1e-4, **kwargs) -> tuple[bool, str | None]:
        passed = actual == expected
        info = None if passed else f"Expected: {expected}\nReceived: {actual}"
        return passed, info

class FloatToleranceEvaluator(BaseEvaluator):
    def evaluate(self, actual, expected, tolerance=1e-4, **kwargs) -> tuple[bool, str | None]:
        try:
            act_val = float(actual)
            exp_val = float(expected)
        except Exception:
            return False, f"Type mismatch or invalid numerical output.\nExpected: {expected}\nReceived: {actual}"
            
        if math.isnan(act_val) or math.isnan(exp_val):
            passed = math.isnan(act_val) == math.isnan(exp_val)
            return passed, None if passed else "NaN mismatch"
        if math.isinf(act_val) or math.isinf(exp_val):
            passed = act_val == exp_val
            return passed, None if passed else "Infinity mismatch"
            
        diff = abs(act_val - exp_val)
        passed = diff <= tolerance
        info = None if passed else f"Expected: {exp_val}\nReceived: {act_val}\nDifference: {diff} (Tolerance: {tolerance})"
        return passed, info

class ArrayToleranceEvaluator(BaseEvaluator):
    def evaluate(self, actual, expected, tolerance=1e-4, **kwargs) -> tuple[bool, str | None]:
        try:
            import numpy as np
            act_arr = np.array(actual)
            exp_arr = np.array(expected)
        except Exception:
            # Fallback recursive list comparison
            passed = self._recursive_compare(actual, expected, tolerance)
            return passed, None if passed else f"Expected: {expected}\nReceived: {actual}"
            
        if act_arr.shape != exp_arr.shape:
            return False, f"Expected shape: {exp_arr.shape}\nReceived shape: {act_arr.shape}"
            
        diff = np.abs(act_arr - exp_arr)
        max_diff = float(np.max(diff))
        passed = bool(np.allclose(act_arr, exp_arr, atol=tolerance, rtol=tolerance))
        
        info = None
        if not passed:
            info = (
                f"Expected shape: {exp_arr.shape}\n"
                f"Received shape: {act_arr.shape}\n\n"
                f"Maximum absolute difference:\n"
                f"{max_diff}\n\n"
                f"Tolerance:\n"
                f"{tolerance}"
            )
        return passed, info

    def _recursive_compare(self, actual, expected, tolerance) -> bool:
        if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
            return abs(actual - expected) <= tolerance
        if isinstance(actual, (list, tuple)) and isinstance(expected, (list, tuple)):
            if len(actual) != len(expected):
                return False
            return all(self._recursive_compare(a, e, tolerance) for a, e in zip(actual, expected))
        return actual == expected

class ShapeEvaluator(BaseEvaluator):
    def evaluate(self, actual, expected, tolerance=1e-4, **kwargs) -> tuple[bool, str | None]:
        try:
            import numpy as np
            act_shape = np.array(actual).shape
            # expected shape is list/tuple
            exp_shape = tuple(expected)
        except Exception:
            return False, "Unable to extract shapes."
            
        passed = act_shape == exp_shape
        info = None if passed else f"Expected shape: {exp_shape}\nReceived shape: {act_shape}"
        return passed, info

class MetricEvaluator(BaseEvaluator):
    def evaluate(self, actual, expected, tolerance=1e-4, **kwargs) -> tuple[bool, str | None]:
        comparison = kwargs.get("comparison", "GTE")
        try:
            act_val = float(actual)
            exp_val = float(expected)
        except Exception:
            return False, "Metric numerical conversion failed."
            
        if comparison == "GTE":
            passed = act_val >= exp_val
            info = None if passed else f"Metric value too low. Expected >= {exp_val}, Received: {act_val}"
        elif comparison == "LTE":
            passed = act_val <= exp_val
            info = None if passed else f"Metric value too high. Expected <= {exp_val}, Received: {act_val}"
        else:
            passed = abs(act_val - exp_val) <= tolerance
            info = None if passed else f"Metric value mismatch. Expected: {exp_val}, Received: {act_val}"
        return passed, info

EVALUATOR_REGISTRY = {
    "EXACT": ExactEvaluator(),
    "FLOAT_TOLERANCE": FloatToleranceEvaluator(),
    "ARRAY_TOLERANCE": ArrayToleranceEvaluator(),
    "NUMPY_ALLCLOSE": ArrayToleranceEvaluator(),
    "SHAPE": ShapeEvaluator(),
    "METRIC": MetricEvaluator()
}

def check_equal(actual, expected, evaluation_type="EXACT", tolerance=1e-4, **kwargs) -> tuple[bool, str | None]:
    evaluator = EVALUATOR_REGISTRY.get(evaluation_type, ExactEvaluator())
    return evaluator.evaluate(actual, expected, tolerance, **kwargs)

def parse_input(input_str):
    if not input_str or not input_str.strip():
        return []
    parts = input_str.split(" | ")
    parsed = []
    for part in parts:
        try:
            parsed.append(ast.literal_eval(part.strip()))
        except Exception:
            parsed.append(part.strip())
    return parsed

def parse_expected(expected_str):
    try:
        return ast.literal_eval(expected_str.strip())
    except Exception:
        return expected_str.strip()

def generate_visualization_data(slug, target_func, custom_inputs):
    if not custom_inputs:
        custom_inputs = {}
    if slug == "sigmoid-activation":
        inputs = [float(x) / 2.0 for x in range(-20, 21)]
        outputs = [float(target_func(x)) for x in inputs]
        custom_z = float(custom_inputs.get("z", 2.0))
        custom_y = float(target_func(custom_z))
        return {
            "type": "FUNCTION",
            "x": inputs,
            "y": outputs,
            "custom_x": custom_z,
            "custom_y": custom_y
        }
    elif slug == "relu-activation":
        inputs = [float(x) / 2.0 for x in range(-20, 21)]
        outputs = target_func(inputs)
        custom_z = float(custom_inputs.get("z", 2.0))
        custom_y = float(target_func([custom_z])[0])
        return {
            "type": "FUNCTION",
            "x": inputs,
            "y": outputs,
            "custom_x": custom_z,
            "custom_y": custom_y
        }
    elif slug == "tanh-activation":
        inputs = [float(x) / 2.0 for x in range(-20, 21)]
        outputs = target_func(inputs)
        custom_z = float(custom_inputs.get("z", 2.0))
        custom_y = float(target_func([custom_z])[0])
        return {
            "type": "FUNCTION",
            "x": inputs,
            "y": outputs,
            "custom_x": custom_z,
            "custom_y": custom_y
        }
    elif slug == "softmax-activation":
        logits = custom_inputs.get("logits", [1.0, 2.0, 3.0])
        probabilities = target_func(logits)
        return {
            "type": "BAR_CHART",
            "x": [f"Logit {i}" for i in range(len(logits))],
            "logits": logits,
            "probabilities": probabilities
        }
    elif slug == "normalize-vector":
        v = custom_inputs.get("vector", [3.0, 4.0])
        out = target_func(v)
        mag = math.sqrt(sum(x**2 for x in v))
        return {
            "type": "VECTOR",
            "original_vector": v,
            "normalized_vector": out,
            "magnitude": mag
        }
    elif slug == "matrix-multiplication":
        a = custom_inputs.get("matrix_a", [[1, 2], [3, 4]])
        b = custom_inputs.get("matrix_b", [[2, 0], [1, 2]])
        out = target_func(a, b)
        return {
            "type": "MATRIX_MULTIPLICATION",
            "matrix_a": a,
            "matrix_b": b,
            "matrix_c": out
        }
    elif slug == "single-step-gradient-descent":
        lr = float(custom_inputs.get("learning_rate", 0.1))
        epochs = int(custom_inputs.get("iterations", 20))
        MAX_TRACE_STEPS = 100
        epochs = min(max(5, epochs), MAX_TRACE_STEPS)
        w = float(custom_inputs.get("w", 0.0))
        steps = []
        for epoch in range(epochs):
            loss = (w - 2.0) ** 2
            dw = 2.0 * w - 4.0
            w_new = float(target_func(w, dw, lr))
            steps.append({
                "epoch": epoch,
                "loss": float(loss),
                "weight": float(w),
                "derivative": float(dw),
                "w_new": float(w_new)
            })
            w = w_new
        return {
            "type": "GRADIENT_DESCENT",
            "steps": steps,
            "learning_rate": lr,
            "target_weight": 2.0
        }
    elif slug == "linear-regression-prediction":
        X = [[1.0], [2.0], [3.0], [4.0]]
        weights = custom_inputs.get("weights", [2.0])
        bias = float(custom_inputs.get("bias", 1.0))
        out = target_func(X, weights, bias)
        return {
            "type": "LINEAR_REGRESSION",
            "X": X,
            "weights": weights,
            "bias": bias,
            "predictions": out
        }
    elif slug == "k-means-centroid":
        X = custom_inputs.get("X", [[1.0, 1.0], [2.0, 2.0], [6.0, 6.0], [7.0, 7.0]])
        centroids = custom_inputs.get("centroids", [[1.5, 1.5], [6.5, 6.5]])
        assignments = target_func(X, centroids)
        return {
            "type": "K_MEANS",
            "X": X,
            "centroids": centroids,
            "assignments": assignments
        }
    elif slug == "pca-projection":
        X = [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]]
        components = [[0.707106], [0.707106]]
        out = target_func(X, components)
        return {
            "type": "PCA",
            "X": X,
            "components": components,
            "projection": out
        }
    elif slug == "dense-layer-forward":
        X = [[1.0, 2.0]]
        weights = [[0.5, -0.5], [1.0, 2.0]]
        bias = [-1.0, 1.0]
        out = target_func(X, weights, bias)
        return {
            "type": "DENSE_LAYER",
            "X": X,
            "weights": weights,
            "bias": bias,
            "output": out
        }
    elif slug == "nn-forward-pass":
        X = [[1.0, 2.0]]
        W1 = [[0.5, -0.5], [1.0, 1.0]]
        b1 = [0.0, 0.0]
        W2 = [[1.0], [-1.0]]
        b2 = [0.0]
        out = target_func(X, W1, b1, W2, b2)
        return {
            "type": "NEURAL_NETWORK",
            "X": X,
            "W1": W1,
            "b1": b1,
            "W2": W2,
            "b2": b2,
            "output": out
        }
    elif slug == "scaled-dot-product":
        Q = [[1.0, 0.0], [0.0, 1.0]]
        K = [[1.0, 0.0], [0.0, 1.0]]
        V = [[10.0], [20.0]]
        out = target_func(Q, K, V)
        return {
            "type": "SCALED_DOT_PRODUCT",
            "Q": Q,
            "K": K,
            "V": V,
            "output": out
        }
    elif slug == "attention-scores":
        Q = [[1.0, 0.0], [0.0, 1.0]]
        K = [[1.0, 0.0], [0.0, 1.0]]
        out = target_func(Q, K)
        return {
            "type": "ATTENTION_SCORES",
            "Q": Q,
            "K": K,
            "attention_matrix": out
        }
    elif slug == "self-attention-weights":
        X = [[1.0, 0.0], [0.0, 1.0]]
        W_q = [[1.0, 0.0], [0.0, 1.0]]
        W_k = [[1.0, 0.0], [0.0, 1.0]]
        W_v = [[10.0], [20.0]]
        out = target_func(X, W_q, W_k, W_v)
        return {
            "type": "SELF_ATTENTION",
            "X": X,
            "W_q": W_q,
            "W_k": W_k,
            "W_v": W_v,
            "output": out
        }
    elif slug == "embedding-similarity":
        q = [0.5, 0.5]
        d = [0.5, 0.5]
        out = target_func(q, d)
        return {
            "type": "EMBEDDING_SIMILARITY",
            "query": q,
            "document": d,
            "similarity": out
        }
    return None

def main():
    # Capture stdout and stderr
    import io
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    sys.stdout = stdout_capture
    sys.stderr = stderr_capture
    
    # Enforce strict timeout inside the container
    def alarm_handler(signum, frame):
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        report = {
            "status": "TIMEOUT",
            "stdout": stdout_capture.getvalue(),
            "stderr": "Execution timed out. Program exceeded limit of 5s.",
            "exit_code": 124,
            "error_type": "TimeoutExpired",
            "tests": []
        }
        print(json.dumps(report))
        os._exit(124)
        
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(5) # 5-second timeout

    report = {
        "status": "completed",
        "stdout": "",
        "stderr": "",
        "exit_code": 0,
        "error_type": None,
        "tests": []
    }
    
    try:
        # Load test cases config
        config_path = "test_config.json"
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file {config_path} not found.")
            
        with open(config_path, "r") as f:
            config = json.load(f)
            
        # Secure isolation step: Delete test_config.json BEFORE importing user code
        # This prevents malicious user solution code from reading hidden outputs from disk.
        try:
            os.remove(config_path)
        except Exception:
            pass
            
        function_name = config.get("function_name")
        test_cases = config.get("test_cases", [])
        
        # Import user solution
        if not os.path.exists("solution.py"):
            raise FileNotFoundError("User solution file solution.py not found.")
            
        import solution
        
        if not hasattr(solution, function_name):
            raise AttributeError(f"Function '{function_name}' not found in your code.")
            
        target_func = getattr(solution, function_name)
        
        for idx, tc in enumerate(test_cases):
            input_str = tc.get("input")
            expected_str = tc.get("expected")
            test_id = tc.get("id")
            eval_type = tc.get("evaluation_type", "EXACT")
            tolerance = tc.get("tolerance", 1e-4)
            metric_name = tc.get("metric")
            threshold = tc.get("threshold")
            
            args = parse_input(input_str)
            expected = parse_expected(expected_str)
            
            try:
                # Execute user function
                if len(args) == 1:
                    actual = target_func(args[0])
                elif len(args) > 1:
                    actual = target_func(*args)
                else:
                    actual = target_func()
                
                # Check outcome using strategy evaluators
                kwargs = {}
                if metric_name:
                    kwargs["metric"] = metric_name
                if threshold is not None:
                    kwargs["threshold"] = threshold
                    
                passed, fail_info = check_equal(actual, expected, eval_type, tolerance, **kwargs)
                
                # Recursively clean NumPy arrays/types
                def clean_numpy(obj):
                    if "numpy" in sys.modules:
                        import numpy as np
                        if isinstance(obj, np.ndarray):
                            return obj.tolist()
                        if isinstance(obj, (np.float32, np.float64)):
                            return float(obj)
                        if isinstance(obj, (np.int32, np.int64)):
                            return int(obj)
                    if isinstance(obj, list):
                        return [clean_numpy(x) for x in obj]
                    if isinstance(obj, dict):
                        return {k: clean_numpy(v) for k, v in obj.items()}
                    return obj
                
                try:
                    serializable_actual = clean_numpy(actual)
                except Exception:
                    serializable_actual = actual
                
                tc_result = {
                    "id": test_id,
                    "status": "passed" if passed else "failed",
                    "actual": str(serializable_actual),
                    "expected": str(expected),
                    "error": fail_info
                }
            except Exception as e:
                tb_lines = traceback.format_exception(*sys.exc_info())
                clean_tb = "".join(tb_lines)
                tc_result = {
                    "id": test_id,
                    "status": "error",
                    "actual": None,
                    "expected": str(expected),
                    "error": clean_tb
                }
                
            report["tests"].append(tc_result)
            
        # Generate visualization data
        report["visualization"] = None
        challenge_slug = config.get("challenge_slug")
        custom_inputs = config.get("custom_inputs")
        if challenge_slug:
            try:
                report["visualization"] = generate_visualization_data(challenge_slug, target_func, custom_inputs)
            except Exception as vis_ex:
                sys.stderr.write(f"\nVisualization generator error: {vis_ex}\n")
            
    except Exception as e:
        report["status"] = "error"
        report["error_type"] = type(e).__name__
        report["stderr"] = traceback.format_exc()
        report["exit_code"] = 1
        
    finally:
        # Cancel alarm if completed
        signal.alarm(0)
        
        # Restore stdout/stderr
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        
        report["stdout"] = stdout_capture.getvalue()
        report["stderr"] = report["stderr"] + stderr_capture.getvalue()
        
        # Output final JSON report
        print(json.dumps(report))

if __name__ == "__main__":
    main()
