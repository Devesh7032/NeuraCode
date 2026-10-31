challenges = [
    {
        "title": "Sigmoid Activation Function",
        "slug": "sigmoid-activation",
        "difficulty": "Easy",
        "category": "Machine Learning",
        "subcategory": "Classification",
        "description": "Implement the sigmoid activation function σ(z) = 1 / (1 + e^-z) handling numerical floats.",
        "concept": "### Sigmoid Activation\nMaps inputs to probabilities in the range (0, 1):\n$$\\sigma(z) = \\frac{1}{1 + e^{-z}}$$",
        "starter_code": "import math\n\ndef sigmoid(z: float) -> float:\n    # Write your code here\n    pass\n",
        "constraints": "z is a float between -100 and 100.",
        "challenge_type": "FUNCTION",
        "function_name": "sigmoid",
        "function_signature": "def sigmoid(z: float) -> float:",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "math,activation,neural-networks",
        "prerequisites": "",
        "tests": [
            {"name": "Zero Input", "input_data": "0.0", "expected_output": "0.5", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Positive Input", "input_data": "2.0", "expected_output": "0.880797", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Negative Input", "input_data": "-2.0", "expected_output": "0.1192029", "visibility": "HIDDEN", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Large Positive", "input_data": "10.0", "expected_output": "0.9999546", "visibility": "HIDDEN", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Large Negative", "input_data": "-10.0", "expected_output": "0.0000454", "visibility": "HIDDEN", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Use math.exp(-z) inside the sigmoid formula.", "order_index": 0}
        ],
        "reference_solution": "import math\ndef sigmoid(z: float) -> float:\n    # Prevent overflow in math.exp\n    if z >= 0:\n        return 1.0 / (1.0 + math.exp(-z))\n    else:\n        return math.exp(z) / (1.0 + math.exp(z))\n"
    },
    {
        "title": "Mean Squared Error (MSE)",
        "slug": "mean-squared-error",
        "difficulty": "Easy",
        "category": "Machine Learning",
        "subcategory": "Regression",
        "description": "Calculate the Mean Squared Error (MSE) between actual and predicted target lists.",
        "concept": "### Mean Squared Error\nCalculates the average squared difference:\n$$MSE = \\frac{1}{n} \\sum_{i=1}^{n} (y_i - \\hat{y}_i)^2$$",
        "starter_code": "from typing import List\n\ndef mean_squared_error(y_true: List[float], y_pred: List[float]) -> float:\n    # Write your code here\n    pass\n",
        "constraints": "y_true and y_pred have equal non-empty dimensions.",
        "challenge_type": "FUNCTION",
        "function_name": "mean_squared_error",
        "function_signature": "def mean_squared_error(y_true: List[float], y_pred: List[float]) -> float:",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "loss-functions,regression,metrics",
        "prerequisites": "",
        "tests": [
            {"name": "Zero Difference", "input_data": "[1.0, 2.0, 3.0] | [1.0, 2.0, 3.0]", "expected_output": "0.0", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Uniform Difference", "input_data": "[1.0, 2.0, 3.0] | [1.5, 2.5, 3.5]", "expected_output": "0.25", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Arbitrary Arrays", "input_data": "[10.0, -5.0] | [12.0, -3.0]", "expected_output": "4.0", "visibility": "HIDDEN", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Iterate values in a loop, square their differences, sum them, and divide by length.", "order_index": 0}
        ],
        "reference_solution": "from typing import List\ndef mean_squared_error(y_true: List[float], y_pred: List[float]) -> float:\n    if not y_true: return 0.0\n    return sum((yt - yp) ** 2 for yt, yp in zip(y_true, y_pred)) / len(y_true)\n"
    },
    {
        "title": "Linear Regression Prediction",
        "slug": "linear-regression-prediction",
        "difficulty": "Easy",
        "category": "Machine Learning",
        "subcategory": "Regression",
        "description": "Compute linear regression predictions: Y = X @ weights + bias.",
        "concept": "### Linear Regression Prediction\nWeighted combinations of input vectors with bias offsets:\n$$Y = XW + b$$",
        "starter_code": "import numpy as np\n\ndef predict(X, weights, bias):\n    # Implement prediction\n    pass\n",
        "constraints": "X has shape (N, D), weights has shape (D,), and bias is a float.",
        "challenge_type": "FUNCTION",
        "function_name": "predict",
        "function_signature": "def predict(X, weights, bias):",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "numpy,regression,linear-algebra",
        "prerequisites": "matrix-multiplication",
        "tests": [
            {"name": "2x2 Dataset", "input_data": "[[1, 2], [3, 4]] | [0.5, -0.5] | 1.0", "expected_output": "[0.5, 0.5]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5},
            {"name": "1D Input List", "input_data": "[[0, 0], [1, 1]] | [2.0, 3.0] | -1.0", "expected_output": "[-1.0, 4.0]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Convert inputs to numpy arrays. Perform dot/matmul operations and add bias.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef predict(X, weights, bias):\n    return (np.array(X) @ np.array(weights) + bias).tolist()\n"
    },
    {
        "title": "Logistic Prediction",
        "slug": "logistic-prediction",
        "difficulty": "Medium",
        "category": "Machine Learning",
        "subcategory": "Classification",
        "description": "Perform logistic regression prediction: Y = sigmoid(X @ weights + bias). Return probability outputs.",
        "concept": "### Logistic Regression Prediction\nOutputs logistic class probabilities by feeding linear outputs through a sigmoid:\n$$\\hat{P} = \\sigma(XW + b)$$",
        "starter_code": "import numpy as np\n\ndef logistic_predict(X, weights, bias):\n    # Write your prediction logic\n    pass\n",
        "constraints": "X has shape (N, D), weights has shape (D,), and bias is a float.",
        "challenge_type": "FUNCTION",
        "function_name": "logistic_predict",
        "function_signature": "def logistic_predict(X, weights, bias):",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "numpy,classification,math",
        "prerequisites": "linear-regression-prediction,sigmoid-activation",
        "tests": [
            {"name": "Zero weight offset", "input_data": "[[0.0, 0.0], [1.0, 1.0]] | [0.0, 0.0] | 0.0", "expected_output": "[0.5, 0.5]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5},
            {"name": "Simple weights", "input_data": "[[1.0, 0.0]] | [2.0, 3.0] | -2.0", "expected_output": "[0.5]", "visibility": "HIDDEN", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Compute X @ weights + bias, then apply sigmoid: 1 / (1 + np.exp(-z)).", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef logistic_predict(X, weights, bias):\n    z = np.array(X) @ np.array(weights) + bias\n    return (1.0 / (1.0 + np.exp(-z))).tolist()\n"
    },
    {
        "title": "Accuracy Metric",
        "slug": "accuracy-metric",
        "difficulty": "Easy",
        "category": "Machine Learning",
        "subcategory": "Evaluation",
        "description": "Compute the classification accuracy (ratio of correctly predicted labels) between y_true and y_pred lists.",
        "concept": "### Classification Accuracy\n$$\\text{Accuracy} = \\frac{\\text{Correct Predictions}}{\\text{Total Predictions}}$$",
        "starter_code": "def calculate_accuracy(y_true: list[int], y_pred: list[int]) -> float:\n    # Implement accuracy\n    pass\n",
        "constraints": "Lists are non-empty and of equal size.",
        "challenge_type": "FUNCTION",
        "function_name": "calculate_accuracy",
        "function_signature": "def calculate_accuracy(y_true: list[int], y_pred: list[int]) -> float:",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "classification,evaluation,metrics",
        "prerequisites": "",
        "tests": [
            {"name": "Perfect predictions", "input_data": "[1, 0, 1, 1] | [1, 0, 1, 1]", "expected_output": "1.0", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Partial accuracy", "input_data": "[1, 0, 1, 0] | [1, 1, 1, 1]", "expected_output": "0.5", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Zero accuracy", "input_data": "[1, 1, 1] | [0, 0, 0]", "expected_output": "0.0", "visibility": "HIDDEN", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Count how many elements match at each position and divide by total length.", "order_index": 0}
        ],
        "reference_solution": "def calculate_accuracy(y_true: list[int], y_pred: list[int]) -> float:\n    if not y_true: return 0.0\n    correct = sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp)\n    return correct / len(y_true)\n"
    },
    {
        "title": "Precision Metric",
        "slug": "precision-metric",
        "difficulty": "Easy",
        "category": "Machine Learning",
        "subcategory": "Evaluation",
        "description": "Compute classification precision: TP / (TP + FP). Return 0.0 if TP + FP is 0.",
        "concept": "### Classification Precision\nRatio of correct positive predictions relative to all predicted positives:\n$$\\text{Precision} = \\frac{TP}{TP + FP}$$",
        "starter_code": "def calculate_precision(y_true: list[int], y_pred: list[int]) -> float:\n    # Implement precision\n    pass\n",
        "constraints": "Elements are binary integers (0 or 1).",
        "challenge_type": "FUNCTION",
        "function_name": "calculate_precision",
        "function_signature": "def calculate_precision(y_true: list[int], y_pred: list[int]) -> float:",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "classification,evaluation,metrics",
        "prerequisites": "accuracy-metric",
        "tests": [
            {"name": "Standard Precision", "input_data": "[1, 0, 1, 0] | [1, 1, 0, 0]", "expected_output": "0.5", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "No Positive predictions", "input_data": "[1, 1] | [0, 0]", "expected_output": "0.0", "visibility": "HIDDEN", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Identify True Positives (yt=1, yp=1) and False Positives (yt=0, yp=1). Precision is TP / (TP + FP).", "order_index": 0}
        ],
        "reference_solution": "def calculate_precision(y_true: list[int], y_pred: list[int]) -> float:\n    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)\n    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)\n    return tp / (tp + fp) if (tp + fp) > 0 else 0.0\n"
    },
    {
        "title": "Recall Metric",
        "slug": "recall-metric",
        "difficulty": "Easy",
        "category": "Machine Learning",
        "subcategory": "Evaluation",
        "description": "Compute classification recall: TP / (TP + FN). Return 0.0 if TP + FN is 0.",
        "concept": "### Classification Recall\nRatio of correct positive predictions relative to all true positive targets:\n$$\\text{Recall} = \\frac{TP}{TP + FN}$$",
        "starter_code": "def calculate_recall(y_true: list[int], y_pred: list[int]) -> float:\n    # Implement recall\n    pass\n",
        "constraints": "Elements are binary integers.",
        "challenge_type": "FUNCTION",
        "function_name": "calculate_recall",
        "function_signature": "def calculate_recall(y_true: list[int], y_pred: list[int]) -> float:",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "classification,evaluation,metrics",
        "prerequisites": "precision-metric",
        "tests": [
            {"name": "Standard Recall", "input_data": "[1, 0, 1, 0] | [1, 1, 0, 0]", "expected_output": "0.5", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Recall Zero Target", "input_data": "[0, 0] | [1, 1]", "expected_output": "0.0", "visibility": "HIDDEN", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "True Positives are where both are 1. False Negatives are where yt=1 and yp=0.", "order_index": 0}
        ],
        "reference_solution": "def calculate_recall(y_true: list[int], y_pred: list[int]) -> float:\n    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)\n    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)\n    return tp / (tp + fn) if (tp + fn) > 0 else 0.0\n"
    },
    {
        "title": "F1 Score Metric",
        "slug": "f1-score-metric",
        "difficulty": "Easy",
        "category": "Machine Learning",
        "subcategory": "Evaluation",
        "description": "Compute the F1 score: harmonic mean of Precision and Recall. Return 0.0 if precision + recall is 0.",
        "concept": "### F1 Score\nBalances precision and recall in a single metric:\n$$F1 = 2 \\cdot \\frac{\\text{Precision} \\cdot \\text{Recall}}{\\text{Precision} + \\text{Recall}}$$",
        "starter_code": "def calculate_f1(y_true: list[int], y_pred: list[int]) -> float:\n    # Implement F1\n    pass\n",
        "constraints": "Elements are binary integers.",
        "challenge_type": "FUNCTION",
        "function_name": "calculate_f1",
        "function_signature": "def calculate_f1(y_true: list[int], y_pred: list[int]) -> float:",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "classification,evaluation,metrics",
        "prerequisites": "recall-metric",
        "tests": [
            {"name": "Standard F1", "input_data": "[1, 0, 1, 0] | [1, 1, 0, 0]", "expected_output": "0.5", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Zero F1 Score", "input_data": "[1, 1] | [0, 0]", "expected_output": "0.0", "visibility": "HIDDEN", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Calculate precision and recall first, then plug into the harmonic mean formula.", "order_index": 0}
        ],
        "reference_solution": "def calculate_f1(y_true: list[int], y_pred: list[int]) -> float:\n    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)\n    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)\n    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)\n    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0\n    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0\n    return 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0\n"
    },
    {
        "title": "K-Means Assignment Step",
        "slug": "k-means-centroid",
        "difficulty": "Medium",
        "category": "Machine Learning",
        "subcategory": "Clustering",
        "description": "Given D-dimensional data points X (shape N x D) and cluster centroids (shape K x D), calculate the index of the closest centroid for each data point.",
        "concept": "### Centroid Assignment\nAssign each data point to its closest centroid using Euclidean distance:\n$$c^{(i)} = \\text{argmin}_k \\|x^{(i)} - \\mu_k\\|^2$$",
        "starter_code": "import numpy as np\n\ndef assign_centroids(X, centroids):\n    # Write assignment logic\n    pass\n",
        "constraints": "X shape (N, D) and centroids shape (K, D). Outputs indices list of size N.",
        "challenge_type": "FUNCTION",
        "function_name": "assign_centroids",
        "function_signature": "def assign_centroids(X, centroids):",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "numpy,clustering,algorithms",
        "prerequisites": "",
        "tests": [
            {"name": "1D cluster sorting", "input_data": "[[1.0], [6.0], [9.0]] | [[0.0], [10.0]]", "expected_output": "[0, 1, 1]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5},
            {"name": "2D cluster sorting", "input_data": "[[1.0, 1.0], [6.0, 5.0]] | [[0.0, 0.0], [5.0, 5.0]]", "expected_output": "[0, 1]", "visibility": "HIDDEN", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Loop through each row in X, compute Euclidean distance to all centroids, and find the index with the minimum distance.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef assign_centroids(X, centroids):\n    X_arr = np.array(X)\n    cents = np.array(centroids)\n    assignments = []\n    for x in X_arr:\n        dists = np.linalg.norm(cents - x, axis=1)\n        assignments.append(int(np.argmin(dists)))\n    return assignments\n"
    },
    {
        "title": "PCA Projection",
        "slug": "pca-projection",
        "difficulty": "Hard",
        "category": "Machine Learning",
        "subcategory": "Dimensionality Reduction",
        "description": "Project centered data X (shape N x D) onto top-k principal components (loadings matrix of shape D x k). Return the projected matrix (shape N x k).",
        "concept": "### PCA Projection\nPrincipal Component Analysis projects high-dimensional data onto orthogonal axes of maximal variance:\n$$Z = X_{\\text{centered}} \\cdot V_k$$",
        "starter_code": "import numpy as np\n\ndef project_pca(X, components):\n    # Project X onto eigenvectors\n    pass\n",
        "constraints": "X has shape N x D. components has shape D x k.",
        "challenge_type": "FUNCTION",
        "function_name": "project_pca",
        "function_signature": "def project_pca(X, components):",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "numpy,linear-algebra,pca",
        "prerequisites": "matrix-multiplication",
        "tests": [
            {"name": "2D to 1D projection", "input_data": "[[1.0, 2.0], [3.0, 4.0]] | [[0.707106], [0.707106]]", "expected_output": "[[2.121320], [4.949747]]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-4}
        ],
        "hints": [
            {"hint_text": "Matrix multiply X by components: X @ components.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef project_pca(X, components):\n    return (np.array(X) @ np.array(components)).tolist()\n"
    }
]
