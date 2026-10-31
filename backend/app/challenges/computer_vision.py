challenges = [
    {
        "title": "Normalize Pixel Values",
        "slug": "normalize-pixels",
        "difficulty": "Easy",
        "category": "Computer Vision",
        "subcategory": "Image Processing",
        "description": "Normalize a list of 8-bit integer pixel values [0-255] to float values in the range [0.0, 1.0].",
        "concept": "### Image Normalization\nScales integer pixel ranges to standard neural network float ranges to speed up gradient descent convergence:\n$$p_{\\text{norm}} = \\frac{p}{255.0}$$",
        "starter_code": "def normalize_pixels(pixels: list[int]) -> list[float]:\n    # Normalize values\n    pass\n",
        "constraints": "Pixels are integers between 0 and 255.",
        "challenge_type": "FUNCTION",
        "function_name": "normalize_pixels",
        "function_signature": "def normalize_pixels(pixels: list[int]) -> list[float]:",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "cv,image-processing,python",
        "prerequisites": "",
        "tests": [
            {"name": "Standard pixels", "input_data": "[0, 127, 255]", "expected_output": "[0.0, 0.498039, 1.0]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-4}
        ],
        "hints": [
            {"hint_text": "Divide each pixel value by 255.0.", "order_index": 0}
        ],
        "reference_solution": "def normalize_pixels(pixels: list[int]) -> list[float]:\n    return [p / 255.0 for p in pixels]\n"
    },
    {
        "title": "Grayscale Conversion",
        "slug": "grayscale-conversion",
        "difficulty": "Easy",
        "category": "Computer Vision",
        "subcategory": "Image Processing",
        "description": "Convert an RGB pixel (tuple or list of 3 integers) to a single grayscale value using the luminosity formula: Y = 0.299*R + 0.587*G + 0.114*B. Return the rounded integer.",
        "concept": "### Grayscale Conversion\nConverts multi-channel color representations into single luminance intensities matching human visual perception weighting:\n$$Y = 0.299R + 0.587G + 0.114B$$",
        "starter_code": "def rgb_to_gray(rgb: list[int]) -> int:\n    # Implement luminosity formula\n    pass\n",
        "constraints": "R, G, B are integers between 0 and 255.",
        "challenge_type": "FUNCTION",
        "function_name": "rgb_to_gray",
        "function_signature": "def rgb_to_gray(rgb: list[int]) -> int:",
        "evaluation_type": "EXACT",
        "tags": "cv,image-processing,python",
        "prerequisites": "normalize-pixels",
        "tests": [
            {"name": "Black pixel", "input_data": "[0, 0, 0]", "expected_output": "0", "visibility": "PUBLIC", "evaluation_type": "EXACT"},
            {"name": "White pixel", "input_data": "[255, 255, 255]", "expected_output": "255", "visibility": "PUBLIC", "evaluation_type": "EXACT"},
            {"name": "Standard RGB color", "input_data": "[100, 150, 200]", "expected_output": "141", "visibility": "HIDDEN", "evaluation_type": "EXACT"}
        ],
        "hints": [
            {"hint_text": "Apply the coefficients, sum them, and round using python's built-in round().", "order_index": 0}
        ],
        "reference_solution": "def rgb_to_gray(rgb: list[int]) -> int:\n    r, g, b = rgb\n    return round(0.299 * r + 0.587 * g + 0.114 * b)\n"
    },
    {
        "title": "Image Array Shape",
        "slug": "image-array-shape",
        "difficulty": "Easy",
        "category": "Computer Vision",
        "subcategory": "Image Processing",
        "description": "Given a flat list of pixel values of size N, reshape it into a height H x width W grayscale image matrix.",
        "concept": "### Image Reshaping\nReshapes raw 1D pixel vectors into structured 2D coordinate matrices suitable for spatial operations like convolutions.",
        "starter_code": "def reshape_image(pixels: list[int], H: int, W: int) -> list[list[int]]:\n    # Reshape list to 2D matrix\n    pass\n",
        "constraints": "len(pixels) == H * W.",
        "challenge_type": "FUNCTION",
        "function_name": "reshape_image",
        "function_signature": "def reshape_image(pixels: list[int], H: int, W: int) -> list[list[int]]:",
        "evaluation_type": "EXACT",
        "tags": "cv,matrix,python",
        "prerequisites": "",
        "tests": [
            {"name": "2x3 Image", "input_data": "[1, 2, 3, 4, 5, 6] | 2 | 3", "expected_output": "[[1, 2, 3], [4, 5, 6]]", "visibility": "PUBLIC", "evaluation_type": "EXACT"}
        ],
        "hints": [
            {"hint_text": "Slice pixels in a loop: from i * W to (i + 1) * W for each row index i.", "order_index": 0}
        ],
        "reference_solution": "def reshape_image(pixels: list[int], H: int, W: int) -> list[list[int]]:\n    return [pixels[i * W : (i + 1) * W] for i in range(H)]\n"
    },
    {
        "title": "2D Convolution Operation",
        "slug": "image-convolution",
        "difficulty": "Medium",
        "category": "Computer Vision",
        "subcategory": "Convolution",
        "description": "Apply a 2D convolution over a grayscale image matrix X (shape H x W) using a kernel K (shape 3 x 3). Assume valid padding (no padding). Output shape is (H - 2) x (W - 2).",
        "concept": "### 2D Spatial Convolution\nSlides a kernel across an image, computing dot products to extract edge or blur features:\n$$S_{ij} = \\sum_{m=1}^{3} \\sum_{n=1}^{3} X_{i+m-1, j+n-1} \\cdot K_{mn}$$",
        "starter_code": "import numpy as np\n\ndef convolve2d(X, K):\n    # Apply 2D convolution\n    pass\n",
        "constraints": "X has shape H x W where H >= 3 and W >= 3. K has shape 3 x 3.",
        "challenge_type": "FUNCTION",
        "function_name": "convolve2d",
        "function_signature": "def convolve2d(X, K):",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "numpy,cv,convolution",
        "prerequisites": "image-array-shape",
        "tests": [
            {"name": "Identity kernel filter", "input_data": "[[1, 2, 3], [4, 5, 6], [7, 8, 9]] | [[0, 0, 0], [0, 1, 0], [0, 0, 0]]", "expected_output": "[[5.0]]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5},
            {"name": "Box blur filter", "input_data": "[[1, 1, 1], [1, 9, 1], [1, 1, 1]] | [[1, 1, 1], [1, 1, 1], [1, 1, 1]]", "expected_output": "[[17.0]]", "visibility": "HIDDEN", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Loop row index from 0 to H-3 and column index from 0 to W-3. Element-wise multiply the 3x3 window by kernel K and sum.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef convolve2d(X, K):\n    img = np.array(X, dtype=float)\n    kernel = np.array(K, dtype=float)\n    H, W = img.shape\n    out_h, out_w = H - 2, W - 2\n    output = np.zeros((out_h, out_w))\n    for r in range(out_h):\n        for c in range(out_w):\n            window = img[r : r + 3, c : c + 3]\n            output[r, c] = np.sum(window * kernel)\n    return output.tolist()\n"
    },
    {
        "title": "Convolution Edge Kernel",
        "slug": "sobel-kernel",
        "difficulty": "Medium",
        "category": "Computer Vision",
        "subcategory": "Convolution Kernel",
        "description": "Generate a 3x3 Sobel horizontal edge detection kernel matrix.",
        "concept": "### Sobel Filter Kernel\nUsed in image processing to highlight horizontal gradients:\n$$K_{\\text{sobel}} = \\begin{bmatrix} -1 & -2 & -1 \\\\ 0 & 0 & 0 \\\\ 1 & 2 & 1 \\end{bmatrix}$$",
        "starter_code": "def get_sobel_horizontal() -> list[list[float]]:\n    # Return Sobel matrix\n    pass\n",
        "constraints": "Output must be a 3x3 list of floats.",
        "challenge_type": "FUNCTION",
        "function_name": "get_sobel_horizontal",
        "function_signature": "def get_sobel_horizontal() -> list[list[float]]:",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "cv,convolution,python",
        "prerequisites": "image-convolution",
        "tests": [
            {"name": "Correct Sobel structure", "input_data": "", "expected_output": "[[-1.0, -2.0, -1.0], [0.0, 0.0, 0.0], [1.0, 2.0, 1.0]]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Directly return the hardcoded 3x3 nested list representing the Sobel filter.", "order_index": 0}
        ],
        "reference_solution": "def get_sobel_horizontal() -> list[list[float]]:\n    return [[-1.0, -2.0, -1.0], [0.0, 0.0, 0.0], [1.0, 2.0, 1.0]]\n"
    },
    {
        "title": "Max Pooling Layer",
        "slug": "max-pooling",
        "difficulty": "Medium",
        "category": "Computer Vision",
        "subcategory": "CNNs",
        "description": "Apply a 2D Max Pooling operation over an input matrix X of shape H x W. Use a pool size of 2 x 2 and a stride of 2. Output shape is H/2 x W/2.",
        "concept": "### Max Pooling\nReduces spatial dimensions (downsampling) by picking the maximum value in local 2x2 windows, providing translation invariance.",
        "starter_code": "import numpy as np\n\ndef max_pooling(X):\n    # Apply 2x2 max pooling\n    pass\n",
        "constraints": "H and W are even integers >= 2.",
        "challenge_type": "FUNCTION",
        "function_name": "max_pooling",
        "function_signature": "def max_pooling(X):",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "numpy,cv,cnn",
        "prerequisites": "image-convolution",
        "tests": [
            {"name": "Basic pooling", "input_data": "[[1, 2, 5, 6], [3, 4, 7, 8], [9, 10, 13, 14], [11, 12, 15, 16]]", "expected_output": "[[4.0, 8.0], [12.0, 16.0]]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Loop r from 0 to H-1 with step 2, and c from 0 to W-1 with step 2. Extract X[r:r+2, c:c+2] and calculate the maximum value.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef max_pooling(X):\n    img = np.array(X, dtype=float)\n    H, W = img.shape\n    out_h, out_w = H // 2, W // 2\n    output = np.zeros((out_h, out_w))\n    for r in range(out_h):\n        for c in range(out_w):\n            window = img[r * 2 : r * 2 + 2, c * 2 : c * 2 + 2]\n            output[r, c] = np.max(window)\n    return output.tolist()\n"
    }
]
