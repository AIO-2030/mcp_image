#!/bin/bash

# Test help method via stdio
echo "Testing help method via stdio:"
echo '{"jsonrpc": "2.0", "method": "help", "params": {}, "id": 1}' | python stdio_server.py

# Test help method via executable (if exists)
if [ -f "dist/image_stdio" ]; then
    echo -e "\nTesting help method via executable:"
    echo '{"jsonrpc": "2.0", "method": "help", "params": {}, "id": 1}' | ./dist/image_stdio
else
    echo -e "\nExecutable not found. Please build it first using: python build.py"
fi 