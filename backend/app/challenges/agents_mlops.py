challenges = [
    {
        "title": "Tool Registry",
        "slug": "tool-registry",
        "difficulty": "Easy",
        "category": "AI Agents",
        "subcategory": "Tool Calling",
        "description": "Implement a ToolRegistry class that allows registering functions using a `@register` decorator and calling them by their string name with arguments.",
        "concept": "### Agent Tool Registry\nAllows autonomous agent loops to catalog and invoke environment-interacting APIs using string identifier mapping.",
        "starter_code": "class ToolRegistry:\n    def __init__(self):\n        # Initialize registry\n        pass\n        \n    def register(self, func):\n        # Decorator to register func\n        pass\n        \n    def call(self, name: str, *args, **kwargs):\n        # Call registered function\n        pass\n",
        "constraints": "Function names must be unique. Call raises ValueError if not found.",
        "challenge_type": "COMPLETE_FUNCTION",
        "function_name": "test_registry",
        "function_signature": "def test_registry():",
        "evaluation_type": "EXACT",
        "tags": "agents,python,architecture",
        "prerequisites": "",
        "tests": [
            {"name": "Register and call", "input_data": "", "expected_output": "'success'", "visibility": "PUBLIC", "evaluation_type": "EXACT"}
        ],
        "hints": [
            {"hint_text": "Keep a dictionary mapping function names to function references. The register decorator should add functions to this dict.", "order_index": 0}
        ],
        "reference_solution": "class ToolRegistry:\n    def __init__(self):\n        self.tools = {}\n    def register(self, func):\n        self.tools[func.__name__] = func\n        return func\n    def call(self, name, *args, **kwargs):\n        if name not in self.tools:\n            raise ValueError(\"Tool not found\")\n        return self.tools[name](*args, **kwargs)\n\ndef test_registry():\n    reg = ToolRegistry()\n    @reg.register\n    def add(x, y):\n        return x + y\n    val = reg.call('add', 5, 10)\n    return 'success' if val == 15 else 'fail'\n"
    },
    {
        "title": "Tool Selection",
        "slug": "tool-selection",
        "difficulty": "Easy",
        "category": "AI Agents",
        "subcategory": "Tool Calling",
        "description": "Given a user intent keyword and a list of tool specs (each a dict with 'name' and 'keywords'), select and return the name of the tool that matches the intent keyword. Return None if no tool matches.",
        "concept": "### Agent Tool Selection\nMaps semantic user queries to specific function signatures using keyword matching or embeddings similarity.",
        "starter_code": "def select_tool(intent: str, tools: list[dict]) -> str:\n    # Select matching tool name\n    pass\n",
        "constraints": "intent is a lowercase string.",
        "challenge_type": "FUNCTION",
        "function_name": "select_tool",
        "function_signature": "def select_tool(intent: str, tools: list[dict]) -> str:",
        "evaluation_type": "EXACT",
        "tags": "agents,nlp,python",
        "prerequisites": "tool-registry",
        "tests": [
            {"name": "Match calculator", "input_data": "'addition' | [{'name': 'add', 'keywords': ['sum', 'addition']}, {'name': 'sub', 'keywords': ['minus']}]", "expected_output": "'add'", "visibility": "PUBLIC", "evaluation_type": "EXACT"},
            {"name": "No match found", "input_data": "'multiply' | [{'name': 'add', 'keywords': ['sum']}]", "expected_output": "None", "visibility": "HIDDEN", "evaluation_type": "EXACT"}
        ],
        "hints": [
            {"hint_text": "Iterate tool specs, check if intent is in the keywords list, and return matching tool name.", "order_index": 0}
        ],
        "reference_solution": "def select_tool(intent: str, tools: list[dict]) -> str:\n    for t in tools:\n        if intent in t.get('keywords', []):\n            return t['name']\n    return None\n"
    },
    {
        "title": "Agent State Tracker",
        "slug": "agent-state",
        "difficulty": "Easy",
        "category": "AI Agents",
        "subcategory": "Memory",
        "description": "Implement an AgentState class that stores a history of user inputs, selected tools, tool outputs, and allows retrieving the full history as a conversation context.",
        "concept": "### Agent State & Memory\nMaintains execution context across multiple steps in a loop, allowing the agent to reference past actions and observations.",
        "starter_code": "class AgentState:\n    def __init__(self):\n        pass\n    def add_input(self, text: str):\n        pass\n    def add_action(self, tool_name: str, output: str):\n        pass\n    def get_history(self) -> list[str]:\n        pass\n",
        "constraints": "History should contain formatted string segments.",
        "challenge_type": "COMPLETE_FUNCTION",
        "function_name": "test_state",
        "function_signature": "def test_state():",
        "evaluation_type": "EXACT",
        "tags": "agents,python,architecture",
        "prerequisites": "tool-selection",
        "tests": [
            {"name": "Track dialog logs", "input_data": "", "expected_output": "'success'", "visibility": "PUBLIC", "evaluation_type": "EXACT"}
        ],
        "hints": [
            {"hint_text": "Maintain an internal list and append formatted messages on add calls.", "order_index": 0}
        ],
        "reference_solution": "class AgentState:\n    def __init__(self):\n        self.history = []\n    def add_input(self, text: str):\n        self.history.append(f\"User: {text}\")\n    def add_action(self, tool_name: str, output: str):\n        self.history.append(f\"Tool {tool_name} returned: {output}\")\n    def get_history(self) -> list[str]:\n        return self.history\n\ndef test_state():\n    state = AgentState()\n    state.add_input(\"hello\")\n    state.add_action(\"greet\", \"hi\")\n    h = state.get_history()\n    return 'success' if len(h) == 2 and h[0] == 'User: hello' else 'fail'\n"
    },
    {
        "title": "Action Observation Loop",
        "slug": "action-observation-loop",
        "difficulty": "Medium",
        "category": "AI Agents",
        "subcategory": "Agent Loops",
        "description": "Implement a simple agent execution loop. Given user query, select matching tool, run tool, update state, and return final output.",
        "concept": "### ReAct Agent Loop\nRepeats a cycle of Planning (Thought) -> Action (Tool Call) -> Observation (Tool Output) until the goal is achieved.",
        "starter_code": "def run_agent_loop(query: str, state, registry, tools_spec) -> str:\n    # Implement agent run cycle\n    pass\n",
        "constraints": "Tools are triggered via intent matching.",
        "challenge_type": "COMPLETE_FUNCTION",
        "function_name": "test_agent_loop",
        "function_signature": "def test_agent_loop():",
        "evaluation_type": "EXACT",
        "tags": "agents,python,algorithms",
        "prerequisites": "agent-state",
        "tests": [
            {"name": "Run complete execution loop", "input_data": "", "expected_output": "'success'", "visibility": "PUBLIC", "evaluation_type": "EXACT"}
        ],
        "hints": [
            {"hint_text": "Extract keyword from query, match with tool selection, invoke tool in registry, update state, and return output.", "order_index": 0}
        ],
        "reference_solution": "class ToolRegistry:\n    def __init__(self): self.tools = {}\n    def register(self, func): self.tools[func.__name__] = func; return func\n    def call(self, name, *args): return self.tools[name](*args)\nclass AgentState:\n    def __init__(self): self.history = []\n    def add_input(self, text): self.history.append(f\"User: {text}\")\n    def add_action(self, tool_name, output): self.history.append(f\"Tool {tool_name}: {output}\")\n\ndef run_agent_loop(query: str, state, registry, tools_spec) -> str:\n    state.add_input(query)\n    selected_tool = None\n    for t in tools_spec:\n        if any(kw in query for kw in t['keywords']):\n            selected_tool = t['name']\n            break\n    if not selected_tool:\n        return \"I cannot help with that.\"\n    res = registry.call(selected_tool)\n    state.add_action(selected_tool, res)\n    return f\"Result: {res}\"\n\ndef test_agent_loop():\n    reg = ToolRegistry()\n    @reg.register\n    def get_weather(): return \"sunny\"\n    \n    state = AgentState()\n    specs = [{'name': 'get_weather', 'keywords': ['weather', 'temp']}]\n    out = run_agent_loop(\"how is the weather?\", state, reg, specs)\n    return 'success' if \"sunny\" in out and len(state.history) == 2 else 'fail'\n"
    },
    {
        "title": "Train-Test Split",
        "slug": "train-test-split",
        "difficulty": "Easy",
        "category": "MLOps",
        "subcategory": "MLOps",
        "description": "Split a dataset (list of features X and targets y) into training and testing slices given a test_size ratio (between 0.0 and 1.0). Do not shuffle.",
        "concept": "### Train-Test Dataset Splitting\nPartitions dataset into non-overlapping training and verification segments to evaluate generalization performance without data leakage:\n$$N_{\\text{train}} = N - \\lfloor N \\cdot \\text{ratio} \\rfloor$$",
        "starter_code": "def train_test_split(X: list, y: list, test_size: float) -> tuple[list, list, list, list]:\n    # Split dataset without shuffling\n    pass\n",
        "constraints": "len(X) == len(y). test_size is a float.",
        "challenge_type": "FUNCTION",
        "function_name": "train_test_split",
        "function_signature": "def train_test_split(X: list, y: list, test_size: float) -> tuple[list, list, list, list]:",
        "evaluation_type": "EXACT",
        "tags": "mlops,validation,python",
        "prerequisites": "",
        "tests": [
            {"name": "Standard split ratio", "input_data": "[1, 2, 3, 4, 5] | [10, 20, 30, 40, 50] | 0.2", "expected_output": "([1, 2, 3, 4], [5], [10, 20, 30, 40], [50])", "visibility": "PUBLIC", "evaluation_type": "EXACT"}
        ],
        "hints": [
            {"hint_text": "Determine split index using integer math: len(X) * test_size. Slice X and y accordingly.", "order_index": 0}
        ],
        "reference_solution": "def train_test_split(X: list, y: list, test_size: float) -> tuple[list, list, list, list]:\n    split_idx = len(X) - int(len(X) * test_size)\n    return X[:split_idx], X[split_idx:], y[:split_idx], y[split_idx:]\n"
    },
    {
        "title": "Batch Inference serving",
        "slug": "batch-inference",
        "difficulty": "Easy",
        "category": "MLOps",
        "subcategory": "Inference",
        "description": "Given batch request inputs (list of feature dictionaries), perform predictions using a loaded model dict of weights and filter out invalid rows (missing keys).",
        "concept": "### Batch Inference serving\nProcesses multiple data samples concurrently while verifying input validation schemas.",
        "starter_code": "def serve_batch(requests: list[dict], weights: dict) -> list[float]:\n    # Filter invalid and calculate prediction score\n    pass\n",
        "constraints": "Model performs prediction: score = w1*x1 + w2*x2.",
        "challenge_type": "FUNCTION",
        "function_name": "serve_batch",
        "function_signature": "def serve_batch(requests: list[dict], weights: dict) -> list[float]:",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "mlops,inference,python",
        "prerequisites": "train-test-split",
        "tests": [
            {"name": "Filter and predict", "input_data": "[{'x1': 1.0, 'x2': 2.0}, {'x1': 2.0}] | {'x1': 2.0, 'x2': 3.0}", "expected_output": "[8.0]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Loop requests, check if both 'x1' and 'x2' exist, compute prediction, and append to outputs.", "order_index": 0}
        ],
        "reference_solution": "def serve_batch(requests: list[dict], weights: dict) -> list[float]:\n    w1 = weights.get('x1', 0.0)\n    w2 = weights.get('x2', 0.0)\n    preds = []\n    for req in requests:\n        if 'x1' in req and 'x2' in req:\n            score = req['x1'] * w1 + req['x2'] * w2\n            preds.append(score)\n    return preds\n"
    },
    {
        "title": "Model Evaluation metrics",
        "slug": "model-evaluation",
        "difficulty": "Easy",
        "category": "MLOps",
        "subcategory": "Model Evaluation",
        "description": "Given predictions y_pred and targets y_true, return a dictionary containing both MSE and MAE metrics.",
        "concept": "### Model Performance Evaluation\nTracks multiple numerical summary statistics (MSE, MAE) to monitor quality regressions during model deployments.",
        "starter_code": "def evaluate_performance(y_true: list[float], y_pred: list[float]) -> dict:\n    # Calculate MSE and MAE\n    pass\n",
        "constraints": "Lists are non-empty and of equal size.",
        "challenge_type": "FUNCTION",
        "function_name": "evaluate_performance",
        "function_signature": "def evaluate_performance(y_true: list[float], y_pred: list[float]) -> dict:",
        "evaluation_type": "EXACT",
        "tags": "mlops,evaluation,metrics",
        "prerequisites": "",
        "tests": [
            {"name": "Evaluate summary", "input_data": "[1.0, 2.0] | [1.5, 2.5]", "expected_output": "{'mse': 0.25, 'mae': 0.5}", "visibility": "PUBLIC", "evaluation_type": "EXACT"}
        ],
        "hints": [
            {"hint_text": "MSE is mean of squared differences. MAE is mean of absolute differences.", "order_index": 0}
        ],
        "reference_solution": "def evaluate_performance(y_true: list[float], y_pred: list[float]) -> dict:\n    mse = sum((yt - yp) ** 2 for yt, yp in zip(y_true, y_pred)) / len(y_true)\n    mae = sum(abs(yt - yp) for yt, yp in zip(y_true, y_pred)) / len(y_true)\n    return {'mse': mse, 'mae': mae}\n"
    },
    {
        "title": "Data Drift Detection",
        "slug": "data-drift",
        "difficulty": "Medium",
        "category": "MLOps",
        "subcategory": "Monitoring",
        "description": "Calculate feature mean drift: return True if absolute difference between training feature mean and production feature mean exceeds threshold, otherwise False.",
        "concept": "### Data Drift Monitoring\nData drift happens when production input distributions change over time relative to the training distribution. Mean drift detection is a simple baseline monitoring check.",
        "starter_code": "def detect_drift(train_feature: list[float], prod_feature: list[float], threshold: float) -> bool:\n    # Detect mean drift\n    pass\n",
        "constraints": "Features lists are non-empty.",
        "challenge_type": "FUNCTION",
        "function_name": "detect_drift",
        "function_signature": "def detect_drift(train_feature: list[float], prod_feature: list[float], threshold: float) -> bool:",
        "evaluation_type": "EXACT",
        "tags": "mlops,monitoring,statistics",
        "prerequisites": "model-evaluation",
        "tests": [
            {"name": "No drift detected", "input_data": "[1.0, 2.0, 3.0] | [1.1, 2.1, 3.1] | 0.5", "expected_output": "False", "visibility": "PUBLIC", "evaluation_type": "EXACT"},
            {"name": "Drift detected", "input_data": "[1.0, 2.0, 3.0] | [2.5, 3.5, 4.5] | 0.5", "expected_output": "True", "visibility": "HIDDEN", "evaluation_type": "EXACT"}
        ],
        "hints": [
            {"hint_text": "Calculate average of train_feature and average of prod_feature. Compare absolute difference of these averages with the threshold.", "order_index": 0}
        ],
        "reference_solution": "def detect_drift(train_feature: list[float], prod_feature: list[float], threshold: float) -> bool:\n    mean_train = sum(train_feature) / len(train_feature)\n    mean_prod = sum(prod_feature) / len(prod_feature)\n    return abs(mean_train - mean_prod) > threshold\n"
    }
]
