challenges = [
    {
        "title": "ReLU Activation Function",
        "slug": "relu-activation",
        "difficulty": "Easy",
        "category": "Deep Learning",
        "subcategory": "Activations",
        "description": "Implement the Rectified Linear Unit (ReLU) activation function for a list of floats.",
        "concept": "### ReLU Activation\nReLU outputs the input directly if positive, otherwise zero:\n$$f(x) = \\max(0, x)$$",
        "starter_code": "def relu(x: list[float]) -> list[float]:\n    # Write your code here\n    pass\n",
        "constraints": "x has length between 1 and 1000.",
        "challenge_type": "FUNCTION",
        "function_name": "relu",
        "function_signature": "def relu(x: list[float]) -> list[float]:",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "activation,neural-networks,math",
        "prerequisites": "",
        "tests": [
            {"name": "Standard values", "input_data": "[-1.0, 0.0, 2.5, -3.0]", "expected_output": "[0.0, 0.0, 2.5, 0.0]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5},
            {"name": "All negative", "input_data": "[-2.0, -10.0]", "expected_output": "[0.0, 0.0]", "visibility": "HIDDEN", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Loop through list and use max(0.0, val) for each element.", "order_index": 0}
        ],
        "reference_solution": "def relu(x: list[float]) -> list[float]:\n    return [max(0.0, val) for val in x]\n"
    },
    {
        "title": "Tanh Activation Function",
        "slug": "tanh-activation",
        "difficulty": "Easy",
        "category": "Deep Learning",
        "subcategory": "Activations",
        "description": "Implement the hyperbolic tangent (tanh) activation function for a list of floats.",
        "concept": "### Tanh Activation\nHyperbolic tangent maps inputs to the range (-1, 1):\n$$\\tanh(z) = \\frac{e^{z} - e^{-z}}{e^{z} + e^{-z}}$$",
        "starter_code": "import math\n\ndef tanh_activation(x: list[float]) -> list[float]:\n    # Implement tanh\n    pass\n",
        "constraints": "x is a list of floats.",
        "challenge_type": "FUNCTION",
        "function_name": "tanh_activation",
        "function_signature": "def tanh_activation(x: list[float]) -> list[float]:",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "activation,neural-networks,math",
        "prerequisites": "",
        "tests": [
            {"name": "Zero value", "input_data": "[0.0]", "expected_output": "[0.0]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5},
            {"name": "Standard values", "input_data": "[1.0, -1.0]", "expected_output": "[0.761594, -0.761594]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Use math.tanh(v) or exponent combinations.", "order_index": 0}
        ],
        "reference_solution": "import math\ndef tanh_activation(x: list[float]) -> list[float]:\n    return [math.tanh(val) for val in x]\n"
    },
    {
        "title": "Softmax Activation Function",
        "slug": "softmax-activation",
        "difficulty": "Easy",
        "category": "Deep Learning",
        "subcategory": "Activations",
        "description": "Implement the Softmax activation function for a 1D vector (list of floats). Ensure numerical stability.",
        "concept": "### Softmax Activation\nNormalizes vectors into categorical probabilities summing to 1.0:\n$$\\text{Softmax}(x)_i = \\frac{e^{x_i - \\max(x)}}{\\sum_j e^{x_j - \\max(x)}}$$",
        "starter_code": "def softmax(x: list[float]) -> list[float]:\n    # Implement stable softmax\n    pass\n",
        "constraints": "x has length between 1 and 100.",
        "challenge_type": "FUNCTION",
        "function_name": "softmax",
        "function_signature": "def softmax(x: list[float]) -> list[float]:",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "activation,neural-networks,math",
        "prerequisites": "",
        "tests": [
            {"name": "Uniform distribution", "input_data": "[1.0, 1.0, 1.0]", "expected_output": "[0.333333, 0.333333, 0.333333]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5},
            {"name": "Unbalanced logits", "input_data": "[0.0, 2.0]", "expected_output": "[0.1192029, 0.880797]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5},
            {"name": "Stable boundary tests", "input_data": "[1000.0, 999.0]", "expected_output": "[0.731058, 0.268941]", "visibility": "HIDDEN", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Subtract the maximum value from all elements before exponentiating to prevent numerical overflow.", "order_index": 0}
        ],
        "reference_solution": "import math\ndef softmax(x: list[float]) -> list[float]:\n    if not x: return []\n    max_val = max(x)\n    exps = [math.exp(val - max_val) for val in x]\n    sum_exps = sum(exps)\n    return [val / sum_exps for val in exps]\n"
    },
    {
        "title": "Binary Cross Entropy Loss",
        "slug": "binary-cross-entropy",
        "difficulty": "Easy",
        "category": "Deep Learning",
        "subcategory": "Loss Functions",
        "description": "Calculate the Binary Cross Entropy (BCE) loss given targets y_true (binary) and model predictions y_pred (probabilities). Ensure numerical stability.",
        "concept": "### Binary Cross Entropy Loss\nMeasures classification loss. Clipped bounds prevent log(0) issues:\n$$\\mathcal{L} = -\\frac{1}{N} \\sum_{i=1}^{N} \\left[ y_i \\log(\\hat{y}_i) + (1 - y_i) \\log(1 - \\hat{y}_i) \\right]$$",
        "starter_code": "def binary_cross_entropy(y_true: list[int], y_pred: list[float]) -> float:\n    # Implement stable BCE loss\n    pass\n",
        "constraints": "y_true and y_pred have equal dimensions. y_pred values are between 0.0 and 1.0.",
        "challenge_type": "FUNCTION",
        "function_name": "binary_cross_entropy",
        "function_signature": "def binary_cross_entropy(y_true: list[int], y_pred: list[float]) -> float:",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "loss-functions,classification,math",
        "prerequisites": "mean-squared-error",
        "tests": [
            {"name": "Standard values", "input_data": "[1, 0, 1] | [0.9, 0.1, 0.8]", "expected_output": "0.14462", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-4},
            {"name": "Stable boundaries", "input_data": "[1, 0] | [1.0, 0.0]", "expected_output": "0.0", "visibility": "HIDDEN", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-4}
        ],
        "hints": [
            {"hint_text": "Clip y_pred to [1e-15, 1 - 1e-15] before taking logs to prevent log(0) domain errors.", "order_index": 0}
        ],
        "reference_solution": "import math\ndef binary_cross_entropy(y_true: list[int], y_pred: list[float]) -> float:\n    total_loss = 0.0\n    for yt, yp in zip(y_true, y_pred):\n        # Clip to prevent infinity\n        yp_clipped = max(min(yp, 1.0 - 1e-15), 1e-15)\n        total_loss += yt * math.log(yp_clipped) + (1 - yt) * math.log(1.0 - yp_clipped)\n    return -total_loss / len(y_true)\n"
    },
    {
        "title": "Dense Layer Forward Pass",
        "slug": "dense-layer-forward",
        "difficulty": "Medium",
        "category": "Deep Learning",
        "subcategory": "Neural Networks",
        "description": "Implement a dense neural layer forward pass: outputs = relu(inputs @ weights + bias). Inputs shape (N, D), weights shape (D, M), bias shape (M,). Output shape (N, M).",
        "concept": "### Dense Layer Forward Pass\nMultiplies inputs by a weight matrix, adds a bias vector, and applies an activation function:\n$$Z = \\text{ReLU}(XW + b)$$",
        "starter_code": "import numpy as np\n\ndef dense_forward(X, weights, bias):\n    # Implement dense layer\n    pass\n",
        "constraints": "Dimensions match. Return list structures.",
        "challenge_type": "FUNCTION",
        "function_name": "dense_forward",
        "function_signature": "def dense_forward(X, weights, bias):",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "numpy,neural-networks,linear-algebra",
        "prerequisites": "linear-regression-prediction,relu-activation",
        "tests": [
            {"name": "Standard batch forward", "input_data": "[[1.0, 2.0]] | [[0.5, -0.5], [1.0, 2.0]] | [-1.0, 1.0]", "expected_output": "[[1.5, 4.5]]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5},
            {"name": "Negative thresholding relu", "input_data": "[[-1.0, -1.0]] | [[1.0, 0.0], [0.0, 1.0]] | [0.0, 0.0]", "expected_output": "[[0.0, 0.0]]", "visibility": "HIDDEN", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Compute X @ weights + bias first, then use np.maximum(0, output) to apply ReLU.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef dense_forward(X, weights, bias):\n    Z = np.array(X) @ np.array(weights) + np.array(bias)\n    return np.maximum(0, Z).tolist()\n"
    },
    {
        "title": "Neural Network Forward Pass",
        "slug": "nn-forward-pass",
        "difficulty": "Medium",
        "category": "Deep Learning",
        "subcategory": "Neural Networks",
        "description": "Perform a forward pass through a 2-layer Neural Network. Layer 1 uses ReLU activation. Layer 2 uses Softmax activation.",
        "concept": "### 2-Layer Neural Network Forward Pass\nFirst hidden layer outputs ReLU activations, while final layer outputs categorical Softmax probabilities:\n$$H = \\text{ReLU}(XW_1 + b_1), \\quad Y = \\text{Softmax}(HW_2 + b_2)$$",
        "starter_code": "import numpy as np\n\ndef forward_pass(X, W1, b1, W2, b2):\n    # Complete forward pass\n    pass\n",
        "constraints": "X dimensions N x D. Outputs probabilities vector N x C.",
        "challenge_type": "FUNCTION",
        "function_name": "forward_pass",
        "function_signature": "def forward_pass(X, W1, b1, W2, b2):",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "numpy,neural-networks,algorithms",
        "prerequisites": "dense-layer-forward,softmax-activation",
        "tests": [
            {"name": "Simple forward pass", "input_data": "[[1.0, 2.0]] | [[0.5, -0.5], [1.0, 1.0]] | [0.0, 0.0] | [[1.0], [-1.0]] | [0.0]", "expected_output": "[[1.0]]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Apply ReLU to the first layer outputs, then apply Softmax to the final output rows.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef forward_pass(X, W1, b1, W2, b2):\n    # Hidden layer\n    H = np.maximum(0, np.array(X) @ np.array(W1) + np.array(b1))\n    # Output layer\n    Z = H @ np.array(W2) + np.array(b2)\n    # Softmax row-wise\n    max_val = np.max(Z, axis=1, keepdims=True)\n    exps = np.exp(Z - max_val)\n    probs = exps / np.sum(exps, axis=1, keepdims=True)\n    return probs.tolist()\n"
    },
    {
        "title": "Backpropagation Step",
        "slug": "backpropagation-step",
        "difficulty": "Hard",
        "category": "Deep Learning",
        "subcategory": "Backpropagation",
        "description": "Calculate the gradients of weights and biases for a single linear layer given inputs X, weight matrix W, bias vector b, and output upstream gradients dL_dZ.",
        "concept": "### Linear Layer Backpropagation\nBackprop computes partial derivatives of the loss relative to model parameters using the chain rule:\n$$\\frac{\\partial \\mathcal{L}}{\\partial W} = X^T \\cdot dZ, \\quad \\frac{\\partial \\mathcal{L}}{\\partial b} = \\sum_{\\text{rows}} dZ$$",
        "starter_code": "import numpy as np\n\ndef backward_pass(X, W, b, dL_dZ):\n    # Return dL_dW, dL_db, dL_dX\n    pass\n",
        "constraints": "X has shape N x D, W has shape D x M, dL_dZ has shape N x M.",
        "challenge_type": "FUNCTION",
        "function_name": "backward_pass",
        "function_signature": "def backward_pass(X, W, b, dL_dZ):",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "numpy,neural-networks,backpropagation",
        "prerequisites": "nn-forward-pass",
        "tests": [
            {"name": "Standard gradients", "input_data": "[[1.0, 2.0]] | [[0.5], [1.5]] | [0.0] | [[0.1]]", "expected_output": "([[0.1], [0.2]], [0.1], [[0.05, 0.15]])", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "dL_dW is X.T @ dL_dZ. dL_db is the sum of dL_dZ along axis 0. dL_dX is dL_dZ @ W.T.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef backward_pass(X, W, b, dL_dZ):\n    X_arr = np.array(X)\n    W_arr = np.array(W)\n    dZ = np.array(dL_dZ)\n    \n    dW = (X_arr.T @ dZ).tolist()\n    db = np.sum(dZ, axis=0).tolist()\n    dX = (dZ @ W_arr.T).tolist()\n    return dW, db, dX\n"
    }
]
