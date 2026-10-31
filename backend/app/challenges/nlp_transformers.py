challenges = [
    {
        "title": "Text Tokenization",
        "slug": "text-tokenization",
        "difficulty": "Easy",
        "category": "NLP",
        "subcategory": "Tokenization",
        "description": "Convert a text string into a list of lowercase tokens, removing punctuation characters: , . ! ? ; : . Keep alphanumeric words.",
        "concept": "### Text Tokenization\nSplits raw prose strings into word units while normalizing capitalization and punctuation structures.",
        "starter_code": "def tokenize(text: str) -> list[str]:\n    # Implement tokenization\n    pass\n",
        "constraints": "text string length between 0 and 1000.",
        "challenge_type": "FUNCTION",
        "function_name": "tokenize",
        "function_signature": "def tokenize(text: str) -> list[str]:",
        "evaluation_type": "EXACT",
        "tags": "nlp,tokenization,python",
        "prerequisites": "",
        "tests": [
            {"name": "Standard sentence", "input_data": "'Hello, World! Welcome to NLP?'", "expected_output": "['hello', 'world', 'welcome', 'to', 'nlp']", "visibility": "PUBLIC", "evaluation_type": "EXACT"},
            {"name": "Multiple spaces", "input_data": "'NLP   is...   fun.'", "expected_output": "['nlp', 'is', 'fun']", "visibility": "HIDDEN", "evaluation_type": "EXACT"}
        ],
        "hints": [
            {"hint_text": "Replace punctuation marks with spaces, convert to lowercase, and split on whitespaces.", "order_index": 0}
        ],
        "reference_solution": "import re\ndef tokenize(text: str) -> list[str]:\n    cleaned = re.sub(r'[\\,\\.\\!\\?\\;\\:]', ' ', text)\n    return [w.lower() for w in cleaned.split() if w]\n"
    },
    {
        "title": "Bag of Words Vectorizer",
        "slug": "bag-of-words",
        "difficulty": "Easy",
        "category": "NLP",
        "subcategory": "Text Classification",
        "description": "Convert a list of tokens into a Bag of Words frequency vector based on a provided vocabulary list.",
        "concept": "### Bag of Words\nCounts the occurrence of vocabulary words in a document, ignoring order:\n$$\\mathbf{x}_j = \\text{count}(\\text{word}_j)$$",
        "starter_code": "def bag_of_words(tokens: list[str], vocabulary: list[str]) -> list[int]:\n    # Implement BoW mapping\n    pass\n",
        "constraints": "vocabulary contains unique strings.",
        "challenge_type": "FUNCTION",
        "function_name": "bag_of_words",
        "function_signature": "def bag_of_words(tokens: list[str], vocabulary: list[str]) -> list[int]:",
        "evaluation_type": "EXACT",
        "tags": "nlp,vectorizer,python",
        "prerequisites": "text-tokenization",
        "tests": [
            {"name": "Basic frequencies", "input_data": "['cat', 'dog', 'cat'] | ['cat', 'dog', 'bird']", "expected_output": "[2, 1, 0]", "visibility": "PUBLIC", "evaluation_type": "EXACT"},
            {"name": "Out of vocabulary tokens", "input_data": "['fish', 'dog'] | ['cat', 'dog']", "expected_output": "[0, 1]", "visibility": "HIDDEN", "evaluation_type": "EXACT"}
        ],
        "hints": [
            {"hint_text": "Create a count array of vocabulary size and increment indices matching word tokens.", "order_index": 0}
        ],
        "reference_solution": "def bag_of_words(tokens: list[str], vocabulary: list[str]) -> list[int]:\n    token_counts = {}\n    for t in tokens:\n        token_counts[t] = token_counts.get(t, 0) + 1\n    return [token_counts.get(word, 0) for word in vocabulary]\n"
    },
    {
        "title": "N-Grams Generator",
        "slug": "n-grams",
        "difficulty": "Easy",
        "category": "NLP",
        "subcategory": "Tokenization",
        "description": "Create a list of word N-grams (tuples of strings) from a list of tokens.",
        "concept": "### N-Grams\nExtracts continuous sequences of $n$ words from a text stream. Bi-grams ($n=2$) and Tri-grams ($n=3$) capture local word ordering.",
        "starter_code": "def generate_ngrams(tokens: list[str], n: int) -> list[tuple[str, ...]]:\n    # Implement ngrams\n    pass\n",
        "constraints": "1 <= n <= len(tokens).",
        "challenge_type": "FUNCTION",
        "function_name": "generate_ngrams",
        "function_signature": "def generate_ngrams(tokens: list[str], n: int) -> list[tuple[str, ...]]:",
        "evaluation_type": "EXACT",
        "tags": "nlp,tokenization,python",
        "prerequisites": "text-tokenization",
        "tests": [
            {"name": "Bigrams test", "input_data": "['cat', 'dog', 'mouse'] | 2", "expected_output": "[('cat', 'dog'), ('dog', 'mouse')]", "visibility": "PUBLIC", "evaluation_type": "EXACT"},
            {"name": "Trigrams test", "input_data": "['a', 'b', 'c', 'd'] | 3", "expected_output": "[('a', 'b', 'c'), ('b', 'c', 'd')]", "visibility": "HIDDEN", "evaluation_type": "EXACT"}
        ],
        "hints": [
            {"hint_text": "Use list slicing inside a loop: loop from 0 to len(tokens) - n + 1.", "order_index": 0}
        ],
        "reference_solution": "def generate_ngrams(tokens: list[str], n: int) -> list[tuple[str, ...]]:\n    if n > len(tokens) or n <= 0:\n        return []\n    return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]\n"
    },
    {
        "title": "TF-IDF Weighting",
        "slug": "tf-idf",
        "difficulty": "Medium",
        "category": "NLP",
        "subcategory": "TF-IDF",
        "description": "Calculate the TF-IDF weight for a term in a document. Term Frequency is count of term / total terms. Inverse Document Frequency is ln(1 + total docs / (1 + doc frequency containing term)). Weight is TF * IDF.",
        "concept": "### TF-IDF\nTerm Frequency-Inverse Document Frequency highlights important terms in documents relative to a corpus:\n$$\\text{tf}(t, d) = \\frac{f_{t,d}}{\\sum_{t'} f_{t',d}}, \\quad \\text{idf}(t, D) = \\ln\\left(\\frac{1 + |D|}{1 + |\\{d \\in D : t \\in d\\}|}\\right)$$",
        "starter_code": "import math\n\ndef tf_idf(term: str, doc: list[str], corpus: list[list[str]]) -> float:\n    # Implement TF-IDF calculation\n    pass\n",
        "constraints": "corpus is non-empty. term is a string.",
        "challenge_type": "FUNCTION",
        "function_name": "tf_idf",
        "function_signature": "def tf_idf(term: str, doc: list[str], corpus: list[list[str]]) -> float:",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "nlp,tfidf,math",
        "prerequisites": "bag-of-words",
        "tests": [
            {"name": "Standard TF-IDF", "input_data": "'cat' | ['cat', 'dog', 'cat'] | [['cat', 'dog'], ['dog'], ['cat']]", "expected_output": "0.191788", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Calculate TF as count(term) / len(doc). Count how many corpus documents contain the term, and compute the natural log for IDF.", "order_index": 0}
        ],
        "reference_solution": "import math\ndef tf_idf(term: str, doc: list[str], corpus: list[list[str]]) -> float:\n    if not doc:\n        return 0.0\n    tf = doc.count(term) / len(doc)\n    # Document frequency containing term\n    df = sum(1 for d in corpus if term in d)\n    idf = math.log((1 + len(corpus)) / (1 + df))\n    return tf * idf\n"
    },
    {
        "title": "Text Similarity",
        "slug": "text-similarity",
        "difficulty": "Easy",
        "category": "NLP",
        "subcategory": "Text Classification",
        "description": "Calculate Jaccard similarity (size of intersection / size of union) between two token lists.",
        "concept": "### Jaccard similarity\n$$\\text{Jaccard}(A, B) = \\frac{|A \\cap B|}{|A \\cup B|}$$",
        "starter_code": "def jaccard_similarity(a: list[str], b: list[str]) -> float:\n    # Implement Jaccard similarity\n    pass\n",
        "constraints": "a and b are lists of string tokens.",
        "challenge_type": "FUNCTION",
        "function_name": "jaccard_similarity",
        "function_signature": "def jaccard_similarity(a: list[str], b: list[str]) -> float:",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "nlp,math,evaluation",
        "prerequisites": "",
        "tests": [
            {"name": "Identical lists", "input_data": "['a', 'b'] | ['b', 'a']", "expected_output": "1.0", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "No overlap", "input_data": "['a', 'b'] | ['c', 'd']", "expected_output": "0.0", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Partial overlap", "input_data": "['a', 'b', 'c'] | ['b', 'c', 'd']", "expected_output": "0.5", "visibility": "HIDDEN", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Convert both lists to sets. Compute set intersections and set unions, and divide sizes.", "order_index": 0}
        ],
        "reference_solution": "def jaccard_similarity(a: list[str], b: list[str]) -> float:\n    set_a = set(a)\n    set_b = set(b)\n    if not set_a and not set_b:\n        return 1.0\n    return len(set_a.intersection(set_b)) / len(set_a.union(set_b))\n"
    },
    {
        "title": "Token Embeddings Lookup",
        "slug": "token-embeddings",
        "difficulty": "Easy",
        "category": "Transformers",
        "subcategory": "Token Embeddings",
        "description": "Given a vocabulary index mapping dictionary and an embedding weight matrix, return the embedding vectors for a list of input tokens.",
        "concept": "### Token Embeddings\nConverts integer word IDs into dense multi-dimensional continuous vectors representing semantic parameters.",
        "starter_code": "import numpy as np\n\ndef embed_tokens(tokens, vocab_map, embedding_weights):\n    # Return embedding representations\n    pass\n",
        "constraints": "Unmapped tokens should look up '<UNK>' or map to zero vectors.",
        "challenge_type": "FUNCTION",
        "function_name": "embed_tokens",
        "function_signature": "def embed_tokens(tokens, vocab_map, embedding_weights):",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "numpy,embeddings,transformers",
        "prerequisites": "",
        "tests": [
            {"name": "Vocabulary lookup", "input_data": "['cat', 'dog'] | {'cat': 0, 'dog': 1, '<UNK>': 2} | [[0.1, 0.2], [0.3, 0.4], [0.0, 0.0]]", "expected_output": "[[0.1, 0.2], [0.3, 0.4]]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Look up token indices in vocab_map (fallback to '<UNK>' index or default). Retrieve the corresponding row from embedding_weights.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef embed_tokens(tokens, vocab_map, embedding_weights):\n    weights = np.array(embedding_weights)\n    unk_idx = vocab_map.get('<UNK>', len(vocab_map) - 1)\n    indices = [vocab_map.get(tok, unk_idx) for tok in tokens]\n    return weights[indices].tolist()\n"
    },
    {
        "title": "Positional Encoding",
        "slug": "positional-encoding",
        "difficulty": "Medium",
        "category": "Transformers",
        "subcategory": "Positional Encoding",
        "description": "Generate sinusoidal positional encoding vectors for sequences of length L and embedding dimension d_model.",
        "concept": "### Positional Encoding\nEncodes position indexes directly into vectors because self-attention disregards sequence ordering:\n$$PE_{(pos, 2i)} = \\sin\\left(\\frac{pos}{10000^{2i/d}}\\right), \\quad PE_{(pos, 2i+1)} = \\cos\\left(\\frac{pos}{10000^{2i/d}}\\right)$$",
        "starter_code": "import numpy as np\n\ndef positional_encoding(seq_len: int, d_model: int):\n    # Return positional encoding matrix L x d\n    pass\n",
        "constraints": "d_model is an even integer.",
        "challenge_type": "FUNCTION",
        "function_name": "positional_encoding",
        "function_signature": "def positional_encoding(seq_len: int, d_model: int):",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "numpy,math,transformers",
        "prerequisites": "token-embeddings",
        "tests": [
            {"name": "PE Matrix 2x4", "input_data": "2 | 4", "expected_output": "[[0.0, 1.0, 0.0, 1.0], [0.841471, 0.540302, 0.0099998, 0.99995]]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-4}
        ],
        "hints": [
            {"hint_text": "Loop pos from 0 to L-1 and i from 0 to d_model/2-1. Calculate division angles and apply sin/cos accordingly.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef positional_encoding(seq_len: int, d_model: int):\n    pe = np.zeros((seq_len, d_model))\n    for pos in range(seq_len):\n        for i in range(0, d_model, 2):\n            div_term = 10000.0 ** (i / d_model)\n            pe[pos, i] = np.sin(pos / div_term)\n            pe[pos, i + 1] = np.cos(pos / div_term)\n    return pe.tolist()\n"
    },
    {
        "title": "Scaled Dot Product Attention",
        "slug": "scaled-dot-product",
        "difficulty": "Hard",
        "category": "Transformers",
        "subcategory": "Attention",
        "description": "Calculate scaled dot-product attention output: softmax(Q @ K.T / sqrt(d_k)) @ V.",
        "concept": "### Scaled Dot-Product Attention\n$$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V$$",
        "starter_code": "import numpy as np\n\ndef scaled_dot_product(Q, K, V):\n    # Implement attention pass\n    pass\n",
        "constraints": "Q, K, V have matching dimensions.",
        "challenge_type": "FUNCTION",
        "function_name": "scaled_dot_product",
        "function_signature": "def scaled_dot_product(Q, K, V):",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "numpy,attention,transformers",
        "prerequisites": "matrix-multiplication,softmax-activation",
        "tests": [
            {"name": "Simple attention", "input_data": "[[1.0, 0.0], [0.0, 1.0]] | [[1.0, 0.0], [0.0, 1.0]] | [[10.0], [20.0]]", "expected_output": "[[13.30238], [16.69762]]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-4}
        ],
        "hints": [
            {"hint_text": "Dot Q with K.T, divide by sqrt(d_k), apply stable softmax row-wise, and dot with V.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef scaled_dot_product(Q, K, V):\n    Q_arr = np.array(Q)\n    K_arr = np.array(K)\n    V_arr = np.array(V)\n    d_k = Q_arr.shape[-1]\n    \n    scores = (Q_arr @ K_arr.T) / np.sqrt(d_k)\n    # Row softmax\n    max_scores = np.max(scores, axis=-1, keepdims=True)\n    exps = np.exp(scores - max_scores)\n    weights = exps / np.sum(exps, axis=-1, keepdims=True)\n    return (weights @ V_arr).tolist()\n"
    },
    {
        "title": "Attention Scores",
        "slug": "attention-scores",
        "difficulty": "Medium",
        "category": "Transformers",
        "subcategory": "Attention",
        "description": "Calculate scaled dot-product attention weights before multiplying Value: softmax(Q @ K.T / sqrt(d_k)).",
        "concept": "### Attention Scores\nWeighted similarities mapping source-target relations:\n$$\\text{Weights} = \\text{Softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)$$",
        "starter_code": "import numpy as np\n\ndef attention_weights(Q, K):\n    # Return softmax scaled dot-product matrices\n    pass\n",
        "constraints": "Q has shape (N, d_k), K has shape (M, d_k).",
        "challenge_type": "FUNCTION",
        "function_name": "attention_weights",
        "function_signature": "def attention_weights(Q, K):",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "numpy,attention,transformers",
        "prerequisites": "scaled-dot-product",
        "tests": [
            {"name": "Standard weights", "input_data": "[[1.0, 0.0], [0.0, 1.0]] | [[1.0, 0.0], [0.0, 1.0]]", "expected_output": "[[0.669762, 0.330238], [0.330238, 0.669762]]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-4}
        ],
        "hints": [
            {"hint_text": "Dot Q with K.T, divide by sqrt(d_k), and apply row-wise softmax.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef attention_weights(Q, K):\n    Q_arr = np.array(Q)\n    K_arr = np.array(K)\n    d_k = Q_arr.shape[-1]\n    scores = (Q_arr @ K_arr.T) / np.sqrt(d_k)\n    max_scores = np.max(scores, axis=-1, keepdims=True)\n    exps = np.exp(scores - max_scores)\n    return (exps / np.sum(exps, axis=-1, keepdims=True)).tolist()\n"
    },
    {
        "title": "Self Attention Layer",
        "slug": "self-attention-weights",
        "difficulty": "Hard",
        "category": "Transformers",
        "subcategory": "Q/K/V",
        "description": "Given sequence representations X (shape N x D) and linear layer project weights W_q, W_k, W_v (shape D x d_k), project vectors and return Attention outputs.",
        "concept": "### Self Attention Layer\nProjects input X to query, key, value matrices first, then applies attention:\n$$Q = XW_q, \\quad K = XW_k, \\quad V = XW_v$$",
        "starter_code": "import numpy as np\n\ndef self_attention(X, W_q, W_k, W_v):\n    # Return projected attention outputs\n    pass\n",
        "constraints": "Dimension constraints map correctly.",
        "challenge_type": "FUNCTION",
        "function_name": "self_attention",
        "function_signature": "def self_attention(X, W_q, W_k, W_v):",
        "evaluation_type": "ARRAY_TOLERANCE",
        "tags": "numpy,attention,transformers",
        "prerequisites": "attention-scores",
        "tests": [
            {"name": "Identity matrices", "input_data": "[[1.0, 0.0], [0.0, 1.0]] | [[1.0, 0.0], [0.0, 1.0]] | [[1.0, 0.0], [0.0, 1.0]] | [[10.0], [20.0]]", "expected_output": "[[13.30238], [16.69762]]", "visibility": "PUBLIC", "evaluation_type": "ARRAY_TOLERANCE", "tolerance": 1e-4}
        ],
        "hints": [
            {"hint_text": "Compute Q = X @ W_q, K = X @ W_k, V = X @ W_v, and then feed them to scaled dot-product attention.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef self_attention(X, W_q, W_k, W_v):\n    X_arr = np.array(X)\n    Q = X_arr @ np.array(W_q)\n    K = X_arr @ np.array(W_k)\n    V = X_arr @ np.array(W_v)\n    d_k = Q.shape[-1]\n    \n    scores = (Q @ K.T) / np.sqrt(d_k)\n    max_scores = np.max(scores, axis=-1, keepdims=True)\n    exps = np.exp(scores - max_scores)\n    weights = exps / np.sum(exps, axis=-1, keepdims=True)\n    return (weights @ V).tolist()\n"
    }
]
