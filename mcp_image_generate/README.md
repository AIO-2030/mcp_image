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