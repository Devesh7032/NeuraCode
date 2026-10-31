challenges = [
    {
        "title": "Vector Sum",
        "slug": "vector-sum",
        "difficulty": "Easy",
        "category": "Python for AI",
        "subcategory": "Python for AI",
        "description": "Implement a function that calculates the sum of a 1D vector (list of floats) without using any external libraries.",
        "concept": "### Vector Sum\nAdding all components of a vector yields a single scalar value. Used to compute sums, averages, and dot product components.",
        "starter_code": "def vector_sum(x: list[float]) -> float:\n    # Write your code here\n    pass\n",
        "constraints": "x has length between 0 and 1000.",
        "challenge_type": "FUNCTION",
        "function_name": "vector_sum",
        "function_signature": "def vector_sum(x: list[float]) -> float:",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "python,math,vector",
        "prerequisites": "",
        "tests": [
            {"name": "Standard Vector", "input_data": "[1.0, 2.0, 3.5]", "expected_output": "6.5", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Empty Vector", "input_data": "[]", "expected_output": "0.0", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Negative Elements", "input_data": "[-1.5, 3.0, -2.5]", "expected_output": "-1.0", "visibility": "HIDDEN", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Use Python's built-in sum() function or a basic for loop.", "order_index": 0}
        ],
        "reference_solution": "def vector_sum(x: list[float]) -> float:\n    return float(sum(x)) if x else 0.0\n"
    },
    {
        "title": "Mean of a Dataset",
        "slug": "mean-of-a-dataset",
        "difficulty": "Easy",
        "category": "Python for AI",
        "subcategory": "Python for AI",
        "description": "Calculate the arithmetic mean (average) of a list of numerical values.",
        "concept": "### Arithmetic Mean\nThe mean is the sum of all elements divided by the count of elements:\n$$\\mu = \\frac{1}{N} \\sum_{i=1}^{N} x_i$$",
        "starter_code": "def calculate_mean(x: list[float]) -> float:\n    # Write your code here\n    pass\n",
        "constraints": "x is a non-empty list of floats.",
        "challenge_type": "FUNCTION",
        "function_name": "calculate_mean",
        "function_signature": "def calculate_mean(x: list[float]) -> float:",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "python,math,statistics",
        "prerequisites": "vector-sum",
        "tests": [
            {"name": "Standard Mean", "input_data": "[1.0, 2.0, 3.0, 4.0]", "expected_output": "2.5", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Single Element", "input_data": "[5.5]", "expected_output": "5.5", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Large Dataset", "input_data": "[10.0, 20.0, 30.0, 40.0, 50.0]", "expected_output": "30.0", "visibility": "HIDDEN", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Divide the sum of the list by the length of the list.", "order_index": 0}
        ],
        "reference_solution": "def calculate_mean(x: list[float]) -> float:\n    return sum(x) / len(x) if x else 0.0\n"
    },
    {
        "title": "Standard Deviation",
        "slug": "standard-deviation",
        "difficulty": "Easy",
        "category": "Python for AI",
        "subcategory": "Python for AI",
        "description": "Compute the population standard deviation of a list of floats.",
        "concept": "### Standard Deviation\nStandard deviation measures the amount of variation or dispersion of a dataset:\n$$\\sigma = \\sqrt{\\frac{1}{N} \\sum_{i=1}^{N} (x_i - \\mu)^2}$$",
        "starter_code": "def calculate_std(x: list[float]) -> float:\n    # Write your code here\n    pass\n",
        "constraints": "x is a non-empty list of floats.",
        "challenge_type": "FUNCTION",
        "function_name": "calculate_std",
        "function_signature": "def calculate_std(x: list[float]) -> float:",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "python,math,statistics",
        "prerequisites": "mean-of-a-dataset",
        "tests": [
            {"name": "Uniform values", "input_data": "[2.0, 2.0, 2.0]", "expected_output": "0.0", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Spread out values", "input_data": "[1.0, 3.0]", "expected_output": "1.0", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Mixed signs", "input_data": "[-2.0, -1.0, 1.0, 2.0]", "expected_output": "1.5811388", "visibility": "HIDDEN", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "First calculate the mean. Then sum the squared differences from the mean, divide by N, and take the square root.", "order_index": 0}
        ],
        "reference_solution": "import math\ndef calculate_std(x: list[float]) -> float:\n    if not x: return 0.0\n    mean = sum(x) / len(x)\n    variance = sum((val - mean) ** 2 for val in x) / len(x)\n    return math.sqrt(variance)\n"
    },
    {
        "title": "Matrix Transpose",
        "slug": "matrix-transpose",
        "difficulty": "Easy",
        "category": "Python for AI",
        "subcategory": "Python for AI",
        "description": "Transpose a 2D matrix (represented as a list of lists of floats) without using external libraries.",
        "concept": "### Matrix Transpose\nSwapping the rows and columns of a matrix:\n$$A^T_{ij} = A_{ji}$$",
        "starter_code": "def transpose(matrix: list[list[float]]) -> list[list[float]]:\n    # Write your code here\n    pass\n",
        "constraints": "matrix is non-empty, and rows have equal lengths.",
        "challenge_type": "FUNCTION",
        "function_name": "transpose",
        "function_signature": "def transpose(matrix: list[list[float]]) -> list[list[float]]:",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "python,matrix,linear-algebra",
        "prerequisites": "",
        "tests": [
            {"name": "2x3 Matrix", "input_data": "[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]", "expected_output": "[[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5},
            {"name": "Square Matrix", "input_data": "[[1.0, 2.0], [3.0, 4.0]]", "expected_output": "[[1.0, 3.0], [2.0, 4.0]]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5},
            {"name": "Single row", "input_data": "[[1.0, 2.0, 3.0]]", "expected_output": "[[1.0], [2.0], [3.0]]", "visibility": "HIDDEN", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Use zip(*matrix) to zip rows together, or a double loop mapping row/col indices.", "order_index": 0}
        ],
        "reference_solution": "def transpose(matrix: list[list[float]]) -> list[list[float]]:\n    if not matrix or not matrix[0]: return []\n    return [list(row) for row in zip(*matrix)]\n"
    },
    {
        "title": "Batch Statistics",
        "slug": "batch-statistics",
        "difficulty": "Medium",
        "category": "Python for AI",
        "subcategory": "Python for AI",
        "description": "Given a batch of data (matrix of shape N x D), calculate the column-wise mean and variance vectors.",
        "concept": "### Batch Statistics\nUsed in Batch Normalization to compute features mean and variance across samples:\n$$\\mu_j = \\frac{1}{N} \\sum_{i=1}^{N} X_{ij}, \\quad \\sigma_j^2 = \\frac{1}{N} \\sum_{i=1}^{N} (X_{ij} - \\mu_j)^2$$",
        "starter_code": "def batch_stats(X: list[list[float]]) -> tuple[list[float], list[float]]:\n    # Implement column-wise stats\n    pass\n",
        "constraints": "X has dimensions N x D where N >= 1 and D >= 1.",
        "challenge_type": "FUNCTION",
        "function_name": "batch_stats",
        "function_signature": "def batch_stats(X: list[list[float]]) -> tuple[list[float], list[float]]:",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "python,statistics,matrix",
        "prerequisites": "standard-deviation",
        "tests": [
            {"name": "Standard Batch", "input_data": "[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]", "expected_output": "([3.0, 4.0], [2.666667, 2.666667])", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5},
            {"name": "Single row", "input_data": "[[10.0, 20.0]]", "expected_output": "([10.0, 20.0], [0.0, 0.0])", "visibility": "HIDDEN", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Transpose the matrix first to easily compute column statistics (which become row statistics of the transpose).", "order_index": 0}
        ],
        "reference_solution": "def batch_stats(X: list[list[float]]) -> tuple[list[float], list[float]]:\n    if not X or not X[0]: return [], []\n    N = len(X)\n    D = len(X[0])\n    means = []\n    vars_ = []\n    for col in range(D):\n        col_vals = [X[row][col] for row in range(N)]\n        col_mean = sum(col_vals) / N\n        col_var = sum((val - col_mean) ** 2 for val in col_vals) / N\n        means.append(col_mean)\n        vars_.append(col_var)\n    return means, vars_\n"
    }
]
