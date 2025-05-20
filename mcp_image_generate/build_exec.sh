#!/bin/bash

# Install required packages with specific version
pip install "pyinstaller>=5.13.0,<6.0.0"

# Parse command line arguments
MODE="stdio"
if [ "$1" == "mcp" ]; then
    MODE="mcp"
fi

# Run build script
python build.py $MODE

# Check if build was successful
if [ "$MODE" == "stdio" ]; then
    if [ -f "dist/image_stdio" ]; then
        echo "Build successful! stdio mode executable created at dist/image_stdio"
    else
        echo "Build failed! Please check the error messages above."
    fi
else
    if [ -f "dist/image_mcp" ]; then
        echo "Build successful! MCP mode executable created at dist/image_mcp"
    else
        echo "Build failed! Please check the error messages above."
    fi
fi 