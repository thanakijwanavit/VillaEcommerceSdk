#!/bin/bash
# Start local documentation server

cd "$(dirname "$0")/.."

echo "🚀 Starting Villa Ecommerce SDK Documentation Server..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found."
    exit 1
fi

# Install markdown if needed
python3 -m pip install markdown > /dev/null 2>&1

# Start server
python3 docs/serve_docs.py

