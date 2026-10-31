challenges = [
    {
        "title": "Dot Product",
        "slug": "dot-product",
        "difficulty": "Easy",
        "category": "Mathematics",
        "subcategory": "Linear Algebra",
        "description": "Calculate the dot product of two 1D vectors a and b using NumPy.",
        "concept": "### Vector Dot Product\nThe dot product multiplies components and sums them:\n$$a \\cdot b = \\sum_{i=1}^{N} a_i b_i$$",
        "starter_code": "import numpy as np\n\ndef dot_product(a, b):\n    # Write your code here\n    pass\n",
        "constraints": "a and b are 1D NumPy arrays of the same length.",
        "challenge_type": "FUNCTION",
        "function_name": "dot_product",
        "function_signature": "def dot_product(a, b):",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "numpy,linear-algebra,math",
        "prerequisites": "vector-sum",
        "tests": [
            {"name": "Standard Vectors", "input_data": "[1, 2, 3] | [4, 5, 6]", "expected_output": "32.0", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Orthogonal Vectors", "input_data": "[1, 0] | [0, 1]", "expected_output": "0.0", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Negative Elements", "input_data": "[-1, 2] | [3, -4]", "expected_output": "-11.0", "visibility": "HIDDEN", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Use np.dot(a, b) or np.sum(a * b).", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef dot_product(a, b):\n    return float(np.dot(a, b))\n"
    },
    {
        "title": "Matrix Multiplication",
        "slug": "matrix-multiplication",
        "difficulty": "Easy",
        "category": "Mathematics",
        "subcategory": "Linear Algebra",
        "description": "Multiply two 2D matrices A and B using NumPy. A has shape (M, N) and B has shape (N, P). Output should have shape (M, P).",
        "concept": "### Matrix Multiplication\nColumn dimensions of A must match row dimensions of B:\n$$C_{ij} = \\sum_{k=1}^{N} A_{ik} B_{kj}$$",
        "starter_code": "import numpy as np\n\ndef matrix_multiply(A, B):\n    # Implement your solution\n    pass\n",
        "constraints": "Dimensions of A and B are between 1 and 100.",
        "challenge_type": "FUNCTION",
        "function_name": "matrix_multiply",
        "function_signature": "def matrix_multiply(A, B):",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "numpy,linear-algebra,math",
        "prerequisites": "dot-product",
        "tests": [
            {"name": "Square Matrices", "input_data": "[[1, 2], [3, 4]] | [[5, 6], [7, 8]]", "expected_output": "[[19, 22], [43, 50]]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5},
            {"name": "Non-Square Dimensions", "input_data": "[[1, 2]] | [[3], [4]]", "expected_output": "[[11]]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5},
            {"name": "Zero Matrix", "input_data": "[[0, 0], [0, 0]] | [[1, 2], [3, 4]]", "expected_output": "[[0, 0], [0, 0]]", "visibility": "HIDDEN", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Use the Python matrix multiplication operator @ or np.matmul().", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef matrix_multiply(A, B):\n    return np.matmul(np.array(A), np.array(B)).tolist()\n"
    },
    {
        "title": "Cosine Similarity",
        "slug": "cosine-similarity",
        "difficulty": "Easy",
        "category": "Mathematics",
        "subcategory": "Linear Algebra",
        "description": "Calculate the cosine similarity between two 1D vectors a and b using NumPy.",
        "concept": "### Cosine Similarity\nCosine similarity measures similarity in direction, regardless of vector scale:\n$$\\text{similarity} = \\frac{a \\cdot b}{\\|a\\| \\|b\\|}$$",
        "starter_code": "import numpy as np\n\ndef cosine_similarity(a, b):\n    # Write your code here\n    pass\n",
        "constraints": "a and b are non-zero vectors of the same length.",
        "challenge_type": "FUNCTION",
        "function_name": "cosine_similarity",
        "function_signature": "def cosine_similarity(a, b):",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "numpy,linear-algebra,math",
        "prerequisites": "dot-product",
        "tests": [
            {"name": "Identical Vectors", "input_data": "[1.0, 2.0] | [1.0, 2.0]", "expected_output": "1.0", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Orthogonal Vectors", "input_data": "[1.0, 0.0] | [0.0, 1.0]", "expected_output": "0.0", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Opposite Vectors", "input_data": "[1.0, -1.0] | [-1.0, 1.0]", "expected_output": "-1.0", "visibility": "HIDDEN", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Divide dot product np.dot(a, b) by product of L2 norms using np.linalg.norm.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef cosine_similarity(a, b):\n    norm_a = np.linalg.norm(a)\n    norm_b = np.linalg.norm(b)\n    return float(np.dot(a, b) / (norm_a * norm_b))\n"
    },
    {
        "title": "Vector Normalization",
        "slug": "normalize-vector",
        "difficulty": "Easy",
        "category": "Mathematics",
        "subcategory": "Linear Algebra",
        "description": "Normalize a 1D vector x to have unit length (L2 norm of 1).",
        "concept": "### Vector Normalization\nDivides a vector by its Euclidean length:\n$$\\hat{x} = \\frac{x}{\\|x\\|_2}$$",
        "starter_code": "import numpy as np\n\ndef normalize(x):\n    # Write your code here\n    pass\n",
        "constraints": "x is a non-zero vector.",
        "challenge_type": "FUNCTION",
        "function_name": "normalize",
        "function_signature": "def normalize(x):",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "numpy,linear-algebra,math",
        "prerequisites": "",
        "tests": [
            {"name": "Standard Vector", "input_data": "[3.0, 4.0]", "expected_output": "[0.6, 0.8]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5},
            {"name": "Uniform Vector", "input_data": "[1.0, 1.0]", "expected_output": "[0.707106, 0.707106]", "visibility": "HIDDEN", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5},
            {"name": "Negative Elements", "input_data": "[-1.0, 2.0, -2.0]", "expected_output": "[-0.333333, 0.666667, -0.666667]", "visibility": "HIDDEN", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Calculate norm using np.linalg.norm(x) or math.sqrt(sum(v**2)) and divide.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef normalize(x):\n    x_arr = np.array(x, dtype=float)\n    norm = np.linalg.norm(x_arr)\n    return (x_arr / norm).tolist() if norm > 0 else x_arr.tolist()\n"
    },
    {
        "title": "Gradient Descent Step",
        "slug": "single-step-gradient-descent",
        "difficulty": "Medium",
        "category": "Mathematics",
        "subcategory": "Calculus",
        "description": "Perform a single step of gradient descent update for parameter w.",
        "concept": "### Gradient Descent Parameter Update\nSubtract gradient multiplied by learning rate:\n$$w_{\\text{new}} = w - \\alpha \\cdot dw$$",
        "starter_code": "def gradient_update(w: float, dw: float, learning_rate: float) -> float:\n    # Write your code here\n    pass\n",
        "constraints": "learning_rate is a positive float.",
        "challenge_type": "FUNCTION",
        "function_name": "gradient_update",
        "function_signature": "def gradient_update(w: float, dw: float, learning_rate: float) -> float:",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "math,optimization,gradient-descent",
        "prerequisites": "",
        "tests": [
            {"name": "Step Positive Gradient", "input_data": "1.0 | 0.1 | 0.01", "expected_output": "0.999", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Step Negative Gradient", "input_data": "0.5 | -0.2 | 0.1", "expected_output": "0.52", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "w_new = w - learning_rate * dw", "order_index": 0}
        ],
        "reference_solution": "def gradient_update(w: float, dw: float, learning_rate: float) -> float:\n    return w - learning_rate * dw\n"
    }
]
