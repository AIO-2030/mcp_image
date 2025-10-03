import os
import time
import base64
import json
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
                },
                {
                    "name": "pixel_image_generate",
                    "description": "Generate pixel emoji style image from user input using LLM prompt generation",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "user_input": {
                                "type": "string",
                                "description": "User's natural language input (can be in any language)"
                            },
                            "negative_prompt": {
                                "type": "string",
                                "description": "Negative prompt",
                                "default": ""
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
                        "required": ["user_input"]
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
            "output": {
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
                    },
                    {
                        "name": "pixel_image_generate",
                        "description": "Generate pixel emoji style image from user input using LLM prompt generation",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "user_input": {
                                    "type": "string",
                                    "description": "User's natural language input (can be in any language)"
                                },
                                "negative_prompt": {
                                    "type": "string",
                                    "description": "Negative prompt",
                                    "default": ""
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
                            "required": ["user_input"]
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
        # Parse image dimensions
        width, height = map(int, image_size.split('x'))

        # Build request data
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

        # Send request to Silicon Flow API
        response = requests.post(self.api_url, headers=self.headers, json=data)
        response.raise_for_status()
        result = response.json()

        # Get image URL
        image_url = result["images"][0]["url"]
        
        # Download image and convert to base64
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        image_base64 = base64.b64encode(image_response.content).decode('utf-8')

        # Build AIO protocol format response
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

    def generate_pixel_emoji_prompt(self, user_input: str, image_size: str = "1024x1024") -> Dict[str, Any]:
        """Generate pixel emoji style image prompts using LLM"""
        llm_url = "https://api.siliconflow.cn/v1/chat/completions"
        
        # Import prompt template from pixel_emjo.py
        from pixel_emjo import generate_pixel_emoji_prompt
        prompt_template = generate_pixel_emoji_prompt(user_input, image_size)
        
        # Build LLM request
        llm_data = {
            "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
            "messages": [
                {
                    "role": "user",
                    "content": prompt_template
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            # Send request to LLM API
            llm_response = requests.post(llm_url, headers=self.headers, json=llm_data)
            llm_response.raise_for_status()
            llm_result = llm_response.json()
            
            # Extract generated prompt
            llm_content = llm_result["choices"][0]["message"]["content"]
            
            # Try to parse JSON response
            try:
                parsed_result = json.loads(llm_content)
                return {
                    "success": True,
                    "user_input": user_input,
                    "llm_response": parsed_result,
                    "image_prompt": parsed_result.get("image_prompt", ""),
                    "intent_summary": parsed_result.get("intent_summary", ""),
                    "style": parsed_result.get("style", "pixel art, emoji-style"),
                    "notes": parsed_result.get("notes", "")
                }
            except json.JSONDecodeError:
                # If JSON parsing fails, use raw content as image prompt
                return {
                    "success": True,
                    "user_input": user_input,
                    "llm_response": llm_content,
                    "image_prompt": llm_content,
                    "intent_summary": f"Generated prompt for: {user_input}",
                    "style": "pixel art, emoji-style",
                    "notes": "LLM generated prompt"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "user_input": user_input
            }

    def pixel_image_generate(
        self,
        user_input: str,
        negative_prompt: str = "",
        num_inference_steps: int = 20,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None,
        image_size: str = "1024x1024"
    ) -> Dict[str, Any]:
        """Generate pixel emoji style images"""
        # Step 1: Generate prompt using LLM
        prompt_result = self.generate_pixel_emoji_prompt(user_input, image_size)
        
        if not prompt_result["success"]:
            return {
                "success": False,
                "error": f"Failed to generate prompt: {prompt_result.get('error', 'Unknown error')}",
                "user_input": user_input
            }
        
        # Step 2: Generate image using the generated prompt
        image_prompt = prompt_result["style"] +","+ prompt_result["image_prompt"]
        
        try:
            # Call existing generate_image method
            image_result = self.generate_image(
                prompt=image_prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                seed=seed,
                image_size=image_size
            )
            
            # Merge results
            return {
                "success": True,
                "message": "Pixel emoji image generated successfully",
                "user_input": user_input,
                "generated_prompt": image_prompt,
                "prompt_metadata": {
                    "intent_summary": prompt_result.get("intent_summary", ""),
                    "style": prompt_result.get("style", ""),
                    "notes": prompt_result.get("notes", "")
                },
                "image_base64": image_result["image_base64"],
                "metadata": {
                    **image_result["metadata"],
                    "generation_type": "pixel_emoji",
                    "original_user_input": user_input
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate image: {str(e)}",
                "user_input": user_input,
                "generated_prompt": image_prompt,
                "prompt_metadata": prompt_result
            } 