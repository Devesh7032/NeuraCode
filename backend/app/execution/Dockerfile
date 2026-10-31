FROM python:3.11-slim

# Install system dependencies if any are needed (none for standard ML kernels, keep it lightweight)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install specific versions of supported libraries
RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    pandas==2.2.1 \
    matplotlib==3.8.3 \
    scikit-learn==1.4.1.post1

# Create an unprivileged user to execute code
RUN useradd -u 1000 -m -s /bin/bash coder

WORKDIR /workspace
USER coder
