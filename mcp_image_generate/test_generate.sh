#!/bin/bash

# Test image generation
echo "Testing image generation:"
echo '{"jsonrpc": "2.0", "method": "generate_image", "params": {"prompt": "A cute cat", "negative_prompt": "blurry, low quality", "steps": 50}, "id": 1}' | python stdio_server.py

# Test with executable (if exists)
if [ -f "dist/image_stdio" ]; then
    echo -e "\nTesting with executable:"
    echo '{"jsonrpc": "2.0", "method": "generate_image", "params": {"prompt": "A cute cat", "negative_prompt": "blurry, low quality", "steps": 50}, "id": 1}' | ./dist/image_stdio
else
    echo -e "\nExecutable not found. Please build it first using: python build.py"
fi 