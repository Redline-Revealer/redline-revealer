#!/bin/bash

echo "✨ Running auto-formatting for Flake8 compatibility..."

# Ensure autopep8 is installed
pip install autopep8

# Run autopep8 recursively on src/ and tests/
autopep8 --in-place --aggressive --aggressive --recursive src/
autopep8 --in-place --aggressive --aggressive --recursive tests/

echo "✅ Format complete. Re-run your commit or CI job!"
