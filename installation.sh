#!/bin/bash

# Upgrade pip
python -m pip install --upgrade pip

# Pull llama3 using ollama
ollama pull llama3

# Check if the model was pulled successfully
if ollama list | grep -q "llama3"; then
  echo "llama3 model has been successfully pulled."
else
  echo "Failed to pull llama3 model."
  exit 1
fi

echo "Pip has been successfully upgraded and llama3 has been pulled."
