Project Path: mcp_image

Source Tree:

```txt
mcp_image
├── LICENSE
├── README.md
└── mcp_image_generate
    ├── README.md
    ├── build.py
    ├── build_exec.sh
    ├── image_service.py
    ├── mcp_server.py
    ├── requirements.txt
    ├── stdio_server.py
    ├── test_generate.sh
    ├── test_generate_exec.sh
    └── test_help.sh

```

`mcp_image/LICENSE`:

```
MIT License

Copyright (c) 2025 AIO-2030

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

`mcp_image/README.md`:

```md
# mcp_image
```

`mcp_image/mcp_image_generate/README.md`:

```md
# Image Generation Service

This service provides image generation capabilities using Silicon Flow's API. It supports both stdio and MCP modes.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Set the following environment variables:
- `API_KEY`: Your Silicon Flow API key

## Usage

### stdio Mode

In stdio mode, the service accepts JSON-RPC 2.0 requests through stdin and returns responses through stdout.

#### Build stdio Mode Executable

```bash
python build.py
# or
./build_exec.sh
```

#### JSON-RPC Request Format

1. Help Method:
```json
{
    "jsonrpc": "2.0",
    "method": "help",
    "params": {},
    "id": 1
}
```

2. Generate Image Method:
```json
{
    "jsonrpc": "2.0",
    "method": "generate_image",
    "params": {
        "prompt": "an island near sea, with seagulls, moon shining over the sea, light house, boats in the background, fish flying over the sea",
        "negative_prompt": "blurry, low quality",
        "num_inference_steps": 20,
        "guidance_scale": 7.5,
        "seed": 4999999999,
        "image_size": "1024x1024"
    },
    "id": 1
}
```

Parameters:
- `prompt` (required): Image generation prompt
- `negative_prompt` (optional): Negative prompt
- `num_inference_steps` (optional, default: 20): Number of inference steps
- `guidance_scale` (optional, default: 7.5): Guidance scale
- `seed` (optional): Random seed
- `image_size` (optional, default: "1024x1024"): Image size

#### Response Format

1. Help Response:
```json
{
    "jsonrpc": "2.0",
    "result": {
        "type": "image_service",
        "description": "This service provides image generation capabilities using Silicon Flow's API",
        "author": "AIO-2030",
        "version": "1.0.0",
        "github": "https://github.com/AIO-2030/mcp_image_generate",
        "transport": ["stdio"],
        "methods": [
            {
                "name": "help",
                "description": "Show this help information."
            },
            {
                "name": "generate_image",
                "description": "Generate image from text prompt",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "Image generation prompt"
                        },
                        "negative_prompt": {
                            "type": "string",
                            "description": "Negative prompt"
                        },
                        "num_inference_steps": {
                            "type": "integer",
                            "description": "Number of inference steps",
                            "default": 20
                        },
                        "guidance_scale": {
                            "type": "number",
                            "description": "Guidance scale",
                            "default": 7.5
                        },
                        "seed": {
                            "type": "integer",
                            "description": "Random seed"
                        },
                        "image_size": {
                            "type": "string",
                            "description": "Image size (e.g., '1024x1024')",
                            "default": "1024x1024"
                        }
                    },
                    "required": ["prompt"]
                },
                "outputSchema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Success message"
                        },
                        "image_base64": {
                            "type": "string",
                            "description": "Base64 encoded image data"
                        },
                        "metadata": {
                            "type": "object",
                            "properties": {
                                "model": {
                                    "type": "string",
                                    "description": "Model name used for generation"
                                },
                                "prompt": {
                                    "type": "string",
                                    "description": "Input prompt used"
                                },
                                "negative_prompt": {
                                    "type": "string",
                                    "description": "Negative prompt used"
                                },
                                "num_inference_steps": {
                                    "type": "integer",
                                    "description": "Number of inference steps used"
                                },
                                "guidance_scale": {
                                    "type": "number",
                                    "description": "Guidance scale used"
                                },
                                "seed": {
                                    "type": "integer",
                                    "description": "Random seed used"
                                },
                                "timings": {
                                    "type": "object",
                                    "properties": {
                                        "inference": {
                                            "type": "number",
                                            "description": "Inference time in seconds"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "required": ["message", "image_base64", "metadata"]
                }
            }
        ]
    },
    "id": 1
}
```

2. Generate Image Response:
```json
{
    "jsonrpc": "2.0",
    "output": {
        "type": "image",
        "message": "Image generated successfully",
        "image_base64": "base64_encoded_image_string",
        "metadata": {
            "model": "Kwai-Kolors/Kolors",
            "prompt": "your prompt",
            "negative_prompt": "your negative prompt",
            "num_inference_steps": 20,
            "guidance_scale": 7.5,
            "seed": 4999999999,
            "timings": {
                "inference": 123
            }
        }
    },
    "id": 1
}
```

#### Error Response Format
```json
{
    "jsonrpc": "2.0",
    "error": {
        "code": -32000,
        "message": "error message"
    },
    "id": 1
}
```

### MCP Mode

In MCP mode, the service provides a set of tools that can be called through the MCP protocol.

#### Build MCP Mode Executable

```bash
python build.py mcp
# or
./build_exec.sh mcp
```

#### Available Tools

1. `help()`: Show help information
2. `generate_image(prompt: str, negative_prompt: str = "", num_inference_steps: int = 20, guidance_scale: float = 7.5, seed: int = None, image_size: str = "1024x1024")`: Generate image from text prompt
3. `image_generation_prompt(prompt: str)`: Create an image generation prompt template
4. `image_resource(image_path: str)`: Provide image file content as a resource

#### Example Usage

```python
from mcp.client import Client

async with Client() as client:
    # Get help information
    help_info = await client.call("help")
    
    # Generate image
    result = await client.call("generate_image", {
        "prompt": "an island near sea, with seagulls, moon shining over the sea, light house, boats in the background, fish flying over the sea",
        "negative_prompt": "blurry, low quality",
        "num_inference_steps": 20,
        "guidance_scale": 7.5,
        "seed": 4999999999,
        "image_size": "1024x1024"
    })
    
    # The result will contain the base64 encoded image and metadata
    image_base64 = result["image_base64"]
    metadata = result["metadata"]
```

## Testing

### Test Help Method
```bash
./test_help.sh
```

### Test Image Generation
```bash
./test_generate.sh
```

## License

MIT 
```

`mcp_image/mcp_image_generate/build.py`:

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
        '--name=image_stdio',
        '--onefile',
        '--clean',
        '--noconfirm',
        '--add-data=.env:.',
        '--hidden-import=image_service'
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
        '--name=image_mcp',
        '--onefile',
        '--clean',
        '--noconfirm',
        '--add-data=.env:.',
        '--hidden-import=image_service',
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

`mcp_image/mcp_image_generate/build_exec.sh`:

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
```

`mcp_image/mcp_image_generate/image_service.py`:

```py
import os
import time
import base64
from typing import Dict, Any, Optional
import requests
from PIL import Image
import io

class ImageService:
    def __init__(self, api_url: str, api_key: str):
        self.name = "Image Generation Service"
        self.version = "1.0.0"
        self.author = "AIO-2030"
        self.github = "https://github.com/AIO-2030/mcp_image_generate"
        
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def get_help_info(self, include_mcp: bool = True) -> Dict[str, Any]:
        """Return help information"""
        help_info = {
            "type": "image_service",
            "description": "This service provides image generation capabilities using Silicon Flow's API",
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
                    "name": "generate_image",
                    "description": "Generate image from text prompt",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "Image generation prompt"
                            },
                            "negative_prompt": {
                                "type": "string",
                                "description": "Negative prompt"
                            },
                            "num_inference_steps": {
                                "type": "integer",
                                "description": "Number of inference steps",
                                "default": 20
                            },
                            "guidance_scale": {
                                "type": "number",
                                "description": "Guidance scale",
                                "default": 7.5
                            },
                            "seed": {
                                "type": "integer",
                                "description": "Random seed"
                            },
                            "image_size": {
                                "type": "string",
                                "description": "Image size (e.g., '1024x1024')",
                                "default": "1024x1024"
                            }
                        },
                        "required": ["prompt"]
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
                    "name": "image_generation_prompt",
                    "description": "Create an image generation prompt template",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "Image generation prompt"
                            }
                        },
                        "required": ["prompt"]
                    }
                }
            ]
            help_info["resources"] = [
                {
                    "name": "image_resource",
                    "description": "Provide image file content as a resource",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "image_path": {
                                "type": "string",
                                "description": "Image file path"
                            }
                        },
                        "required": ["image_path"]
                    }
                }
            ]

        return help_info

    def help(self) -> Dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "result": {
                "type": "image_service",
                "description": """This MCP module is built on top of the `Kwai-Kolors/Kolors` image processing and enhancement library. It enables AI agents to programmatically apply rich color manipulations, visual filters, and artistic transformations to images. The module supports functions such as color grading, tone adjustment, hue shifts, and preset-based visual styles. It is particularly useful for generative image post-processing, photo style transfer, and aesthetic enhancement pipelines in both static and dynamic workflows.

Core features:
- Apply predefined color filters (vintage, cinematic, warm/cool tone, etc.)
- Dynamically adjust brightness, contrast, saturation, exposure
- Transform image color palettes via Kolors' manipulation engine
- Support batch or single-image processing
- Compatible with prompt-based visual aesthetic agents

Typical input:
- Base64-encoded or URL-based image input
- Optional JSON-based instruction set for desired transformations (e.g. `{ "filter": "cinematic", "brightness": 1.1 }`)

Expected output:
- Transformed image (base64-encoded)
- Metadata describing applied transformation parameters

Recommended use cases:
- Enhancing AI-generated images for branding/design
- Post-processing aesthetic agents
- Integrating visual effect chains in creative pipelines""",
                "author": "AIO-2030",
                "version": "1.0.0",
                "github": "https://github.com/AIO-2030/mcp_image_generate",
                "transport": ["stdio"],
                "methods": [
                    {
                        "name": "help",
                        "description": "Show this help information."
                    },
                    {
                        "name": "generate_image",
                        "description": "Generate image from text prompt",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "prompt": {
                                    "type": "string",
                                    "description": "Image generation prompt"
                                },
                                "negative_prompt": {
                                    "type": "string",
                                    "description": "Negative prompt"
                                },
                                "num_inference_steps": {
                                    "type": "integer",
                                    "description": "Number of inference steps",
                                    "default": 20
                                },
                                "guidance_scale": {
                                    "type": "number",
                                    "description": "Guidance scale",
                                    "default": 7.5
                                },
                                "seed": {
                                    "type": "integer",
                                    "description": "Random seed"
                                },
                                "image_size": {
                                    "type": "string",
                                    "description": "Image size (e.g., '1024x1024')",
                                    "default": "1024x1024"
                                }
                            },
                            "required": ["prompt"]
                        }
                    }
                ]
            },
            "id": 1
        }

    def generate_image(
        self,
        prompt: str,
        negative_prompt: str = "",
        num_inference_steps: int = 20,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None,
        image_size: str = "1024x1024"
    ) -> Dict[str, Any]:
        # 解析图像尺寸
        width, height = map(int, image_size.split('x'))

        # 构建请求数据
        data = {
            "model": "Kwai-Kolors/Kolors",
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "width": width,
            "height": height,
            "batch_size": 1
        }
        if seed is not None:
            data["seed"] = seed

        # 发送请求到硅基 API
        response = requests.post(self.api_url, headers=self.headers, json=data)
        response.raise_for_status()
        result = response.json()

        # 获取图像 URL
        image_url = result["images"][0]["url"]
        
        # 下载图像并转换为 base64
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        image_base64 = base64.b64encode(image_response.content).decode('utf-8')

        # 构建 AIO 协议格式的响应
        return {
            "message": "Image generated successfully",
            "image_base64": image_base64,
            "metadata": {
                "model": "Kwai-Kolors/Kolors",
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "seed": result.get("seed"),
                "timings": result.get("timings", {})
            }
        }

    def image_generation_prompt(self, prompt: str) -> str:
        """Create an image generation prompt template"""
        return f"Please generate an image based on the following prompt: {prompt}"

    def image_resource(self, image_path: str) -> str:
        """Provide image file content as a resource"""
        try:
            with open(image_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except Exception as e:
            return {"error": str(e)} 
```

`mcp_image/mcp_image_generate/mcp_server.py`:

```py
import asyncio
import time
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.fastmcp.tools import Tool
from image_service import ImageService

# Create MCP server instance
mcp = Server("Image Generation MCP")

# Initialize ImageService
service = ImageService(
    api_url="https://api.siliconflow.cn/v1/images/generations",  # Silicon Flow API URL
    api_key="your_api_key_here"  # Replace with actual API key
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
async def generate_image(prompt: str, negative_prompt: str = "", num_inference_steps: int = 20,
                        guidance_scale: float = 7.5, seed: int = None, image_size: str = "1024x1024") -> dict:
    """Generate image from text prompt using Silicon Flow's API"""
    return service.generate_image(prompt, negative_prompt, num_inference_steps, guidance_scale, seed, image_size)

@Tool.from_function
def image_generation_prompt(prompt: str) -> str:
    """Create an image generation prompt template"""
    return service.image_generation_prompt(prompt)

@Tool.from_function
async def image_resource(image_path: str) -> str:
    """Provide image file content as a resource"""
    return service.image_resource(image_path)

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await mcp.run(read_stream, write_stream, {})

if __name__ == "__main__":
    asyncio.run(main()) 
```

`mcp_image/mcp_image_generate/requirements.txt`:

```txt
python-dotenv>=1.0.1,<2.0.0
requests>=2.26.0,<3.0.0
pydantic>=2.10.6,<3.0.0
mcp==1.6.0
PyInstaller>=4.5.1,<5.0.0
pytest>=6.2.5,<7.0.0
pillow>=9.2.0,<11.0.0
modelcontextprotocol>=0.1.0,<1.0.0
python-multipart>=0.0.5,<1.0.0 
```

`mcp_image/mcp_image_generate/stdio_server.py`:

```py
import json
import sys
from image_service import ImageService

def main():
    service = ImageService(
        api_url="https://api.siliconflow.cn/v1/images/generations",  # Silicon Flow API URL
        api_key="sk-sizdciquzgledafoqeguebohudunufoztppywmclondftwij"  # Replace with actual API key
    )
    
    try:
        # Read all input from stdin
        request_data = sys.stdin.read()
        
        # Parse JSON-RPC request
        request = json.loads(request_data)
        
        # Get method and params
        method = request.get("method")
        params = request.get("params", {})
        
        # Handle different methods
        if method == "help":
            response = service.help()
        elif method == "generate_image":
            result = service.generate_image(
                prompt=params.get("prompt"),
                negative_prompt=params.get("negative_prompt", ""),
                num_inference_steps=params.get("num_inference_steps", 20),
                guidance_scale=params.get("guidance_scale", 7.5),
                seed=params.get("seed"),
                image_size=params.get("image_size", "1024x1024")
            )
            response = {
                "jsonrpc": "2.0",
                "output": {
                    "type": "image",
                    **result
                },
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

`mcp_image/mcp_image_generate/test_generate.sh`:

```sh
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
```

`mcp_image/mcp_image_generate/test_generate_exec.sh`:

```sh
#!/bin/bash

# 测试图像生成功能
echo "测试图像生成功能..."

# 确保在正确的目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 检查可执行文件是否存在
if [ ! -f "dist/image_stdio" ]; then
    echo "错误：找不到 image_stdio 可执行文件"
    echo "请先运行 python build.py 构建可执行文件"
    exit 1
fi

# 构建测试请求
REQUEST='{
    "jsonrpc": "2.0",
    "method": "generate_image",
    "params": {
        "prompt": "an island near sea, with seagulls, moon shining over the sea, light house, boats in the background, fish flying over the sea",
        "negative_prompt": "blurry, low quality",
        "num_inference_steps": 20,
        "guidance_scale": 7.5,
        "seed": 4999999999,
        "image_size": "1024x1024"
    },
    "id": 1
}'

# 发送请求到 stdio 服务器
echo "$REQUEST" | ./dist/image_stdio

# 检查退出状态
if [ $? -eq 0 ]; then
    echo "测试成功完成"
else
    echo "测试失败"
    exit 1
fi 
```

`mcp_image/mcp_image_generate/test_help.sh`:

```sh
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
```