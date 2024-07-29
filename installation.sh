#!/bin/bash

# Upgrade pip
python -m pip install --upgrade pip
ollama pull llama3

echo "Pip has been successfully upgraded."
