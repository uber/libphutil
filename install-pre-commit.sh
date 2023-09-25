#!/bin/bash

# Check if pre-commit is already installed
if ! command -v pre-commit &> /dev/null; then
    echo "pre-commit is not installed. Installing..."

    # Install pre-commit using pip
    python3 -m pip install pre-commit

    # Check if installation was successful
    if [ $? -eq 0 ]; then
        echo "pre-commit installed successfully."

    else
        echo "Failed to install pre-commit."
    fi
else
    echo "pre-commit is already installed."
fi

# Run pre-commit installation
pre-commit install
