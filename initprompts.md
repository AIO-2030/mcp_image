Project Path: mcp_voice_identify

Source Tree:

```txt
mcp_voice_identify
├── LICENSE
├── README.md
├── build.py
├── build_exec.sh
├── mcp_server.py
├── requirements.txt
├── stdio_server.py
├── test_help.sh
├── test_voice_base64.sh
├── test_voice_file.sh
└── voice_service.py

```

`mcp_voice_identify/LICENSE`:

```
MIT License

Copyright (c) 2025 Yeo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

`mcp_voice_identify/README.md`:

```md
# Voice Recognition MCP Service

This service provides voice recognition and text extraction capabilities through both stdio and MCP modes.

## Features

- Voice recognition from file
- Voice recognition from base64 encoded data
- Text extraction
- Support for both stdio and MCP modes
- Structured voice recognition results

## Project Structure

- `voice_service.py` - Core service implementation
- `stdio_server.py` - stdio mode entry point
- `mcp_server.py` - MCP mode entry point
- `build.py` - Build script for executables
- `build_exec.sh` - Build execution script
- `test_*.sh` - Test scripts for different functionalities

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AIO-2030/mcp_voice_identify.git
cd mcp_voice_identify
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```
API_URL=your_api_url
API_KEY=your_api_key
```

## Usage

### stdio Mode

1. Run the service:
```bash
python stdio_server.py
```

2. Send JSON-RPC requests via stdin:
```json
{
    "jsonrpc": "2.0",
    "method": "help",
    "params": {},
    "id": 1
}
```

3. Or use the executable:
```bash
./dist/voice_stdio
```

### MCP Mode

1. Run the service:
```bash
python mcp_server.py
```

2. Or use the executable:
```bash
./dist/voice_mcp
```

## Voice Recognition Results

The service provides structured voice recognition results. Here's an example of the response format:

### Original API Response
```json
{
    "jsonrpc": "2.0",
    "result": {
        "message": "input processed successfully",
        "results": "test test test",
        "label_result": "<|en|><|EMO_UNKNOWN|><|Speech|><|woitn|>test test test"
    },
    "id": 1
}
```

### Restructured Response
```json
{
    "jsonrpc": "2.0",
    "result": {
        "message": "input processed successfully",
        "results": "test test test",
        "label_result": {
            "lan": "en",
            "emo": "unknown",
            "type": "speech",
            "speaker": "woitn",
            "text": "test test test"
        }
    },
    "id": 1
}
```

### Label Result Fields

The `label_result` field contains the following structured information:

| Field    | Description                          | Example Value |
|----------|--------------------------------------|---------------|
| lan      | Language code                        | "en"          |
| emo      | Emotion state                        | "unknown"     |
| type     | Audio type                          | "speech"      |
| speaker  | Speaker identifier                   | "woitn"       |
| text     | Recognized text content              | "test test test" |

### Special Labels

The service recognizes and processes the following special labels in the original response:

- `<|en|>` - Language code
- `<|EMO_UNKNOWN|>` - Emotion state
- `<|Speech|>` - Audio type
- `<|woitn|>` - Speaker identifier

## Building Executables

1. Make the build script executable:
```bash
chmod +x build_exec.sh
```

2. Build stdio mode executable:
```bash
./build_exec.sh
```

3. Build MCP mode executable:
```bash
./build_exec.sh mcp
```

The executables will be created at:
- stdio mode: `dist/voice_stdio`
- MCP mode: `dist/voice_mcp`

## Testing

Run the test scripts:

```bash
chmod +x test_*.sh
./test_help.sh
./test_voice_file.sh
./test_voice_base64.sh
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

```

`mcp_voice_identify/build.py`:

```py
import os
import PyInstaller.__main__

def build_stdio():
    """Build stdio mode executable"""
    # Ensure dist directory exists
    if not os.path.exists('dist'):
        os.makedirs('dist')
    
    # Build parameters for stdio mode
    params = [
        'stdio_server.py',
        '--name=voice_stdio',
        '--onefile',
        '--clean',
        '--noconfirm',
        '--add-data=.env:.',
        '--hidden-import=voice_service'
    ]
    
    # Execute build
    PyInstaller.__main__.run(params)

def build_mcp():
    """Build MCP mode executable"""
    # Ensure dist directory exists
    if not os.path.exists('dist'):
        os.makedirs('dist')
    
    # Build parameters for MCP mode
    params = [
        'mcp_server.py',
        '--name=voice_mcp',
        '--onefile',
        '--clean',
        '--noconfirm',
        '--add-data=.env:.',
        '--hidden-import=voice_service',
        '--hidden-import=mcp.server',
        '--hidden-import=mcp.server.stdio',
        '--hidden-import=mcp.server.fastmcp.tools',
        '--hidden-import=anyio',
        '--hidden-import=anyio.streams.memory'
    ]
    
    # Execute build
    PyInstaller.__main__.run(params)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'mcp':
        build_mcp()
    else:
        build_stdio() 
```

`mcp_voice_identify/build_exec.sh`:

```sh
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
    if [ -f "dist/voice_stdio" ]; then
        echo "Build successful! stdio mode executable created at dist/voice_stdio"
    else
        echo "Build failed! Please check the error messages above."
    fi
else
    if [ -f "dist/voice_mcp" ]; then
        echo "Build successful! MCP mode executable created at dist/voice_mcp"
    else
        echo "Build failed! Please check the error messages above."
    fi
fi 
```

`mcp_voice_identify/mcp_server.py`:

```py
import asyncio
import time
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.fastmcp.tools import Tool
from voice_service import VoiceService

# Create MCP server instance
mcp = Server("Voice Recognition MCP")

# Initialize VoiceService with explicit values
service = VoiceService(
    api_url="https://openapi.emchub.ai/emchub/api/openapi/task/executeTaskByUser/edgematrix:yiminger/extract_text",  # Replace with your actual API URL
    api_key="833_txLiSbJibu160317539183112192"  # Replace with your actual API key
)

# Define tools
@Tool.from_function
async def help() -> dict:
    """Return help information in JSON-RPC 2.0 format"""
    return {
        "jsonrpc": "2.0",
        "result": service.get_help_info(include_mcp=True),
        "id": int(time.time() * 1000)
    }

@Tool.from_function
async def identify_voice(file_path: str) -> dict:
    """Identify voice from file"""
    return service.identify_voice(file_path)

@Tool.from_function
async def identify_voice_base64(base64_data: str) -> dict:
    """Identify voice from base64 encoded data"""
    return service.identify_voice_base64(base64_data)

@Tool.from_function
async def extract_text(text: str) -> dict:
    """Extract text"""
    return service.extract_text(text)

@Tool.from_function
def voice_recognition_prompt(file_path: str) -> str:
    """Create a voice recognition prompt template"""
    return service.voice_recognition_prompt(file_path)

@Tool.from_function
async def voice_resource(file_path: str) -> str:
    """Provide voice file content as a resource"""
    return service.voice_resource(file_path)

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await mcp.run(read_stream, write_stream, {})

if __name__ == "__main__":
    asyncio.run(main()) 
```

`mcp_voice_identify/requirements.txt`:

```txt
python-dotenv>=1.0.1,<2.0.0
requests>=2.26.0,<3.0.0
pydantic>=2.10.6,<3.0.0
mcp==1.6.0
PyInstaller>=4.5.1,<5.0.0
pytest>=6.2.5,<7.0.0
pillow>=9.2.0,<11.0.0
modelcontextprotocol>=0.1.0,<1.0.0 
```

`mcp_voice_identify/stdio_server.py`:

```py
import json
import sys
from voice_service import VoiceService

def main():
    service = VoiceService(
        api_url="https://openapi.emchub.ai/emchub/api/openapi/task/executeTaskByUser/edgematrix:yiminger/extract_text",
        api_key="833_txLiSbJibu160317539183112192"
    )
    
    try:
        # Read all input from stdin at once
        request_data = sys.stdin.read()
        
        # Parse JSON-RPC request
        request = json.loads(request_data)
        
        # Get method and params
        method = request.get("method")
        params = request.get("params", {})
        
        # Handle different methods
        if method == "help":
            response = service.help()
        elif method == "identify_voice":
            response = {
                "jsonrpc": "2.0",
                "result": service.identify_voice(params.get("file_path")),
                "id": request.get("id")
            }
        elif method == "identify_voice_base64":
            response = {
                "jsonrpc": "2.0",
                "result": service.identify_voice_base64(params.get("base64_data")),
                "id": request.get("id")
            }
        elif method == "extract_text":
            response = {
                "jsonrpc": "2.0",
                "result": service.extract_text(params.get("text")),
                "id": request.get("id")
            }
        else:
            response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                },
                "id": request.get("id")
            }
        
        # Write response to stdout
        print(json.dumps(response))
        sys.stdout.flush()
        
    except json.JSONDecodeError as e:
        print(json.dumps({
            "jsonrpc": "2.0",
            "error": {
                "code": -32700,
                "message": f"Parse error: {str(e)}"
            },
            "id": None
        }))
        sys.stdout.flush()
    except Exception as e:
        print(json.dumps({
            "jsonrpc": "2.0",
            "error": {
                "code": -32000,
                "message": str(e)
            },
            "id": request.get("id") if "request" in locals() else None
        }))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
```

`mcp_voice_identify/test_help.sh`:

```sh
#!/bin/bash

# Test help method via stdio
echo "Testing help method via stdio:"
echo '{"jsonrpc": "2.0", "method": "help", "params": {}, "id": 1}' | python stdio_server.py

# Test help method via executable (if exists)
if [ -f "dist/voice_stdio" ]; then
    echo -e "\nTesting help method via executable:"
    echo '{"jsonrpc": "2.0", "method": "help", "params": {}, "id": 1}' | ./dist/voice_stdio
else
    echo -e "\nExecutable not found. Please build it first using: python build.py"
fi 
```

`mcp_voice_identify/test_voice_base64.sh`:

```sh
#!/bin/bash

# Set test file path
TEST_FILE="test.wav"

# Check if file exists
if [ ! -f "$TEST_FILE" ]; then
    echo "Error: Test file $TEST_FILE not found"
    exit 1
fi

# Convert file to base64
BASE64_DATA=$(base64 -w 0 "$TEST_FILE")

# Test with Python directly
#echo "Testing voice identification with base64 data:"
#echo '{"jsonrpc": "2.0", "method": "identify_voice_base64", "params": {"base64_data": "'$BASE64_DATA'"}, "id": 1}' | python stdio_server.py

# Test with executable (if exists)
if [ -f "dist/voice_stdio" ]; then
    echo -e "\nTesting with executable:"
    echo '{"jsonrpc": "2.0", "method": "identify_voice_base64", "params": {"base64_data": "'$BASE64_DATA'"}, "id": 1}' | ./dist/voice_stdio
else
    echo -e "\nExecutable not found. Please build it first using: python build.py"
fi 

```

`mcp_voice_identify/test_voice_file.sh`:

```sh
#!/bin/bash

# Set test file path
TEST_FILE="test.wav"

# Check if file exists
if [ ! -f "$TEST_FILE" ]; then
    echo "Error: Test file $TEST_FILE not found"
    exit 1
fi

# Test with Python directly
echo "Testing voice identification:"
echo '{"jsonrpc": "2.0", "method": "identify_voice", "params": {"file_path": "'$TEST_FILE'"}, "id": 1}' | python stdio_server.py

# Test with executable (if exists)
if [ -f "dist/voice_stdio" ]; then
    echo -e "\nTesting with executable:"
    echo '{"jsonrpc": "2.0", "method": "identify_voice", "params": {"file_path": "'$TEST_FILE'"}, "id": 1}' | ./dist/voice_stdio
else
    echo -e "\nExecutable not found. Please build it first using: python build.py"
fi 
```

`mcp_voice_identify/voice_service.py`:

```py
import os
import time
import base64
import re
from typing import Dict, Any, Optional
import requests

class VoiceService:
    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        self.name = "Voice Recognition Service"
        self.version = "1.0.0"
        self.author = "AIO-2030"
        self.github = "https://github.com/AIO-2030/mcp_voice_identify"
        
        # Initialize API configuration
        self.api_url = api_url or os.getenv("API_URL")
        self.api_key = api_key or os.getenv("API_KEY")
        
        if not self.api_url or not self.api_key:
            raise ValueError("API_URL and API_KEY must be provided either through constructor or environment variables")

    def parse_label_result(self, label_result: str) -> Dict[str, str]:
        """Parse label result into structured format"""
        # Extract values between <| and |>
        pattern = r'<\|(.*?)\|>'
        matches = re.findall(pattern, label_result)
        
        # Initialize result dictionary
        result = {
            "lan": "unknown",
            "emo": "unknown",
            "type": "unknown",
            "speaker": "unknown",
            "text": ""
        }
        
        # Map labels to keys
        label_mapping = {
            "en": "lan",
            "EMO_UNKNOWN": "emo",
            "Speech": "type",
            "woitn": "speaker"
        }
        
        # Process matches
        for match in matches:
            if match in label_mapping:
                result[label_mapping[match]] = match.lower()
            elif match not in ["", " "]:
                result["text"] = match
        
        return result

    def restructure_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Restructure API response with parsed label result"""
        if "label_result" in response:
            parsed_label = self.parse_label_result(response["label_result"])
            response["label_result"] = parsed_label
        return response

    def get_help_info(self, include_mcp: bool = True) -> Dict[str, Any]:
        """Return help information"""
        help_info = {
            "type": "voice_service",
            "description": "This service provides voice recognition and text extraction services",
            "author": self.author,
            "version": self.version,
            "github": self.github,
            "transport": ["stdio"],
            "methods": [
                {
                    "name": "help",
                    "description": "Show this help information."
                },
                {
                    "name": "identify_voice",
                    "description": "Identify voice from file",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Voice file path"
                            }
                        },
                        "required": ["file_path"]
                    }
                },
                {
                    "name": "identify_voice_base64",
                    "description": "Identify voice from base64 encoded data",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "base64_data": {
                                "type": "string",
                                "description": "Base64 encoded voice data"
                            }
                        },
                        "required": ["base64_data"]
                    }
                },
                {
                    "name": "extract_text",
                    "description": "Extract text",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Text to extract"
                            }
                        },
                        "required": ["text"]
                    }
                }
            ]
        }

        if include_mcp:
            help_info["transport"].append("mcp")
            help_info["methods"].extend([
                {
                    "name": "tools_list",
                    "description": "List all available tools"
                },
                {
                    "name": "tools_call",
                    "description": "Call a tool",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Tool name"
                            },
                            "arguments": {
                                "type": "object",
                                "description": "Tool arguments"
                            }
                        },
                        "required": ["name"]
                    }
                }
            ])
            help_info["prompts"] = [
                {
                    "name": "voice_recognition_prompt",
                    "description": "Create a voice recognition prompt template",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Voice file path"
                            }
                        },
                        "required": ["file_path"]
                    }
                }
            ]
            help_info["resources"] = [
                {
                    "name": "voice_resource",
                    "description": "Provide voice file content as a resource",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Voice file path"
                            }
                        },
                        "required": ["file_path"]
                    }
                }
            ]

        return help_info

    def help(self) -> Dict[str, Any]:
        """Return help information in JSON-RPC 2.0 format"""
        return {
            "jsonrpc": "2.0",
            "result": self.get_help_info(include_mcp=False),
            "id": int(time.time() * 1000)
        }

    def identify_voice(self, file_path: str) -> Dict[str, Any]:
        """Identify voice from file"""
        try:
            with open(file_path, "rb") as f:
                files = {'file': f}
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'accept': 'application/json'
                }
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    files=files
                )
                response.raise_for_status()
                result = response.json()
                return self.restructure_response(result)
        except Exception as e:
            return {"error": str(e)}

    def identify_voice_base64(self, base64_data: str) -> Dict[str, Any]:
        """Identify voice from base64 encoded data"""
        try:
            # Convert base64 to file-like object
            import io
            file_data = base64.b64decode(base64_data)
            file_obj = io.BytesIO(file_data)
            file_obj.name = 'audio.wav'  # Set a filename
            
            files = {'file': file_obj}
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'accept': 'application/json'
            }
            response = requests.post(
                self.api_url,
                headers=headers,
                files=files
            )
            response.raise_for_status()
            result = response.json()
            return self.restructure_response(result)
        except Exception as e:
            return {"error": str(e)}

    def extract_text(self, text: str) -> Dict[str, Any]:
        """Extract text"""
        try:
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"text": text}
            )
            response.raise_for_status()
            result = response.json()
            return self.restructure_response(result)
        except Exception as e:
            return {"error": str(e)}

    def voice_recognition_prompt(self, file_path: str) -> str:
        """Create a voice recognition prompt template"""
        return f"Please process this voice file: {file_path}"

    def voice_resource(self, file_path: str) -> str:
        """Provide voice file content as a resource"""
        try:
            with open(file_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except Exception as e:
            return {"error": str(e)} 
```