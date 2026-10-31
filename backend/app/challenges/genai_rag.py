challenges = [
    {
        "title": "Embedding Similarity",
        "slug": "embedding-similarity",
        "difficulty": "Easy",
        "category": "Generative AI",
        "subcategory": "Similarity",
        "description": "Calculate the Cosine Similarity between a query embedding and a document embedding using NumPy.",
        "concept": "### Embedding Similarity\nMeasures the semantic proximity of dense vector embeddings of documents and queries:\n$$\\text{similarity} = \\frac{q \\cdot d}{\\|q\\| \\|d\\|}$$",
        "starter_code": "import numpy as np\n\ndef embedding_similarity(query_emb, doc_emb):\n    # Calculate cosine similarity\n    pass\n",
        "constraints": "Embeddings are 1D float vectors of matching shape.",
        "challenge_type": "FUNCTION",
        "function_name": "embedding_similarity",
        "function_signature": "def embedding_similarity(query_emb, doc_emb):",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "numpy,embeddings,genai",
        "prerequisites": "cosine-similarity",
        "tests": [
            {"name": "Standard overlap", "input_data": "[0.5, 0.5] | [0.5, 0.5]", "expected_output": "1.0", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Partially similar", "input_data": "[1.0, 0.0] | [0.707106, 0.707106]", "expected_output": "0.707106", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Apply the cosine similarity formula using np.dot and np.linalg.norm.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef embedding_similarity(query_emb, doc_emb):\n    q = np.array(query_emb)\n    d = np.array(doc_emb)\n    return float(np.dot(q, d) / (np.linalg.norm(q) * np.linalg.norm(d)))\n"
    },
    {
        "title": "Top-K Retrieval",
        "slug": "top-k-retrieval",
        "difficulty": "Medium",
        "category": "Generative AI",
        "subcategory": "Retrieval",
        "description": "Given a query embedding q and a list of document embeddings, return the indices of the top-k documents sorted by highest cosine similarity.",
        "concept": "### Top-K Retrieval\nFinds the most relevant context indices for RAG by sorting documents in descending order of similarity:\n$$\\text{indices} = \\text{argsort}(\\text{similarities})[-k:][::-1]$$",
        "starter_code": "import numpy as np\n\ndef retrieve_top_k(query_emb, doc_embs, k):\n    # Return top k document indices\n    pass\n",
        "constraints": "1 <= k <= len(doc_embs).",
        "challenge_type": "FUNCTION",
        "function_name": "retrieve_top_k",
        "function_signature": "def retrieve_top_k(query_emb, doc_embs, k):",
        "evaluation_type": "EXACT",
        "tags": "numpy,embeddings,retrieval",
        "prerequisites": "embedding-similarity",
        "tests": [
            {"name": "Retrieve top-1", "input_data": "[1.0, 0.0] | [[0.0, 1.0], [0.8, 0.6], [0.5, 0.5]] | 1", "expected_output": "[1]", "visibility": "PUBLIC", "evaluation_type": "EXACT"},
            {"name": "Retrieve top-2", "input_data": "[0.0, 1.0] | [[0.0, 1.0], [0.8, 0.6], [0.1, 0.9]] | 2", "expected_output": "[0, 2]", "visibility": "HIDDEN", "evaluation_type": "EXACT"}
        ],
        "hints": [
            {"hint_text": "Compute cosine similarity of query with each document. Argsort descending and return the first k indices.", "order_index": 0}
        ],
        "reference_solution": "import numpy as np\ndef retrieve_top_k(query_emb, doc_embs, k):\n    q = np.array(query_emb)\n    d = np.array(doc_embs)\n    dots = d @ q\n    norms = np.linalg.norm(d, axis=1) * np.linalg.norm(q)\n    sims = dots / norms\n    # argsort sorts ascending, negative gives descending order\n    sorted_indices = np.argsort(-sims)\n    return sorted_indices[:k].tolist()\n"
    },
    {
        "title": "Document Chunking",
        "slug": "document-chunking",
        "difficulty": "Easy",
        "category": "RAG",
        "subcategory": "Document Chunking",
        "description": "Given a text string, split it into chunks of exactly chunk_size words, overlapping adjacent chunks by exactly chunk_overlap words.",
        "concept": "### Document Chunking\nPrepares document sources for embedding retrieval by breaking down large articles into smaller segments to fit within LLM context windows.",
        "starter_code": "def chunk_document(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:\n    # Split text into overlapping word chunks\n    pass\n",
        "constraints": "chunk_overlap < chunk_size. Words are split by spaces.",
        "challenge_type": "FUNCTION",
        "function_name": "chunk_document",
        "function_signature": "def chunk_document(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:",
        "evaluation_type": "EXACT",
        "tags": "rag,text,python",
        "prerequisites": "",
        "tests": [
            {"name": "Standard overlap chunking", "input_data": "'one two three four five six' | 3 | 1", "expected_output": "['one two three', 'three four five', 'five six']", "visibility": "PUBLIC", "evaluation_type": "EXACT"},
            {"name": "No overlap chunking", "input_data": "'a b c d e' | 2 | 0", "expected_output": "['a b', 'c d', 'e']", "visibility": "HIDDEN", "evaluation_type": "EXACT"}
        ],
        "hints": [
            {"hint_text": "Split text by spaces to get words list. Loop with step size = (chunk_size - chunk_overlap) and join words.", "order_index": 0}
        ],
        "reference_solution": "def chunk_document(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:\n    words = text.split()\n    if not words: return []\n    chunks = []\n    step = chunk_size - chunk_overlap\n    if step <= 0: step = 1\n    for i in range(0, len(words), step):\n        chunk_words = words[i:i+chunk_size]\n        chunks.append(\" \".join(chunk_words))\n        if i + chunk_size >= len(words):\n            break\n    return chunks\n"
    },
    {
        "title": "Context Assembly",
        "slug": "context-assembly",
        "difficulty": "Easy",
        "category": "RAG",
        "subcategory": "Context Construction",
        "description": "Assemble a RAG context string from retrieved document chunks. Join chunks with '\\n---\\n'. Limit total token counts (word count) to a specified max_tokens cap.",
        "concept": "### Context Assembly\nPrepares contextual prompts for LLM querying by joining retrieved document snippets while respecting model token size constraints.",
        "starter_code": "def assemble_context(chunks: list[str], max_tokens: int) -> str:\n    # Join chunks with separator up to max_tokens limit\n    pass\n",
        "constraints": "Token counts are measured as space-separated words.",
        "challenge_type": "FUNCTION",
        "function_name": "assemble_context",
        "function_signature": "def assemble_context(chunks: list[str], max_tokens: int) -> str:",
        "evaluation_type": "EXACT",
        "tags": "rag,text,python",
        "prerequisites": "document-chunking",
        "tests": [
            {"name": "Fit under limit", "input_data": "['cat sat', 'dog barked'] | 10", "expected_output": "'cat sat\\n---\\ndog barked'", "visibility": "PUBLIC", "evaluation_type": "EXACT"},
            {"name": "Trunk at boundary", "input_data": "['first document snippet', 'second long paragraph details'] | 4", "expected_output": "'first document snippet'", "visibility": "HIDDEN", "evaluation_type": "EXACT"}
        ],
        "hints": [
            {"hint_text": "Iterate chunks, measure word counts, and append chunks only if total words remain under max_tokens.", "order_index": 0}
        ],
        "reference_solution": "def assemble_context(chunks: list[str], max_tokens: int) -> str:\n    assembled = []\n    current_tokens = 0\n    for c in chunks:\n        c_tokens = len(c.split())\n        if current_tokens + c_tokens <= max_tokens:\n            assembled.append(c)\n            current_tokens += c_tokens\n        else:\n            break\n    return \"\\n---\\n\".join(assembled)\n"
    },
    {
        "title": "Retrieval Ranking",
        "slug": "retrieval-ranking",
        "difficulty": "Medium",
        "category": "RAG",
        "subcategory": "Evaluation",
        "description": "Calculate the Reciprocal Rank (1 / rank of first relevant document) for a list of retrieved document IDs given the true target relevant document ID. Return 0.0 if not found.",
        "concept": "### Mean Reciprocal Rank (MRR)\nEvaluates retrieval ranking quality. Measures where the first relevant item appears in list:\n$$\\text{RR} = \\frac{1}{\\text{rank}_{\\text{first-relevant}}}$$",
        "starter_code": "def reciprocal_rank(retrieved_ids: list[int], ground_truth_id: int) -> float:\n    # Return reciprocal rank\n    pass\n",
        "constraints": "retrieved_ids is a list of unique integers.",
        "challenge_type": "FUNCTION",
        "function_name": "reciprocal_rank",
        "function_signature": "def reciprocal_rank(retrieved_ids: list[int], ground_truth_id: int) -> float:",
        "evaluation_type": "FLOAT_TOLERANCE",
        "tags": "rag,evaluation,metrics",
        "prerequisites": "top-k-retrieval",
        "tests": [
            {"name": "First item match", "input_data": "[10, 20, 30] | 10", "expected_output": "1.0", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "Second item match", "input_data": "[10, 20, 30] | 20", "expected_output": "0.5", "visibility": "PUBLIC", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5},
            {"name": "No match", "input_data": "[10, 20, 30] | 99", "expected_output": "0.0", "visibility": "HIDDEN", "evaluation_type": "FLOAT_TOLERANCE", "tolerance": 1e-5}
        ],
        "hints": [
            {"hint_text": "Find 0-indexed position of ground_truth_id in retrieved_ids. Rank is position + 1. Reciprocal rank is 1 / rank.", "order_index": 0}
        ],
        "reference_solution": "def reciprocal_rank(retrieved_ids: list[int], ground_truth_id: int) -> float:\n    if ground_truth_id in retrieved_ids:\n        idx = retrieved_ids.index(ground_truth_id)\n        return 1.0 / (idx + 1)\n    return 0.0\n"
    }
]
