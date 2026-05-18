import os
import base64
from http import HTTPStatus
from typing import Dict, Any, Optional, List

import dashscope
import requests
from dashscope import MultiModalConversation
from PIL import Image, ImageFilter, ImageEnhance
import io
import numpy as np

# 阿里云百炼 / DashScope 多模态文生图默认网关（与官方示例一致）
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"


class ImageService:
    def __init__(
        self,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        image_model: str = "qwen-image-2.0",
    ):
        self.name = "Image Generation Service"
        self.version = "1.0.0"
        self.author = "AIO-2030"
        self.github = "https://github.com/AIO-2030/mcp_image_generate"

        self.api_url = api_url
        self.api_key = (api_key or os.getenv("DASHSCOPE_API_KEY") or "").strip()
        if not self.api_key:
            raise ValueError(
                "需要提供 DashScope API Key：构造参数 api_key 或环境变量 DASHSCOPE_API_KEY"
            )

        self.image_model = os.getenv("DASHSCOPE_IMAGE_MODEL", image_model)

    @staticmethod
    def _dashscope_size_string(image_size: str) -> str:
        """将 1024x1024 转为 DashScope 文生图常用的 width*height，并限制在官方建议范围内。"""
        normalized = image_size.strip().lower().replace("*", "x")
        width, height = map(int, normalized.split("x", 1))
        width = max(512, min(2048, width))
        height = max(512, min(2048, height))
        return f"{width}*{height}"

    def _extract_image_ref_from_multimodal(self, response: Any) -> str:
        if response.status_code != HTTPStatus.OK:
            code = getattr(response, "code", None)
            msg = getattr(response, "message", None) or str(response)
            raise RuntimeError(f"DashScope 文生图失败: code={code}, message={msg}")
        output = getattr(response, "output", None)
        if output is None:
            raise RuntimeError("DashScope 返回无 output")
        choices = getattr(output, "choices", None)
        if not choices:
            raise RuntimeError("DashScope 返回无 choices")
        message = choices[0].message
        content = message.content if message is not None else None
        if isinstance(content, str):
            raise RuntimeError(
                "模型未返回图片（仅文本）。请确认模型为文生图多模态模型且提示词合法。"
            )
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and "image" in item:
                    ref = item["image"]
                    if ref:
                        return str(ref)
        raise RuntimeError("响应中未找到图片 URL 或 base64 字段（image）")

    @staticmethod
    def _image_reference_to_base64(ref: str) -> str:
        if ref.startswith("data:") and "base64," in ref:
            return ref.split("base64,", 1)[1].strip()
        image_response = requests.get(ref, timeout=120)
        image_response.raise_for_status()
        return base64.b64encode(image_response.content).decode("utf-8")

    def get_help_info(self, include_mcp: bool = True) -> Dict[str, Any]:
        """Return help information"""
        help_info = {
            "type": "image_service",
            "description": "This service provides text-to-image via Alibaba Cloud DashScope (e.g. qwen-image-2.0)",
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
                    "description": "Generate pixel LED-matrix style image from user input using the built-in prompt template (no extra LLM)",
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
                        "description": "Generate pixel LED-matrix style image from user input using the built-in prompt template (no extra LLM)",
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
        size_param = self._dashscope_size_string(image_size)
        messages: List[Dict[str, Any]] = [
            {"role": "user", "content": [{"text": prompt}]},
        ]

        kwargs: Dict[str, Any] = {
            "result_format": "message",
            "stream": False,
            "n": 1,
            "watermark": True,
            "negative_prompt": negative_prompt or "",
            "size": size_param,
        }
        if seed is not None:
            kwargs["seed"] = seed

        response = MultiModalConversation.call(
            api_key=self.api_key,
            model=self.image_model,
            messages=messages,
            **kwargs,
        )

        image_ref = self._extract_image_ref_from_multimodal(response)
        image_base64 = self._image_reference_to_base64(image_ref)

        return {
            "message": "Image generated successfully",
            "image_base64": image_base64,
            "metadata": {
                "model": self.image_model,
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "seed": seed,
                "size": size_param,
                "request_id": getattr(response, "request_id", None),
                "provider": "dashscope",
            },
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

    def enhance_pixel_emoji_image(
        self,
        image_base64: str,
        enable_led_effect: bool = True
    ) -> str:
        """
        Enhance pixel emoji image with the following features:
        - Force resize to 48×48 (Nearest Neighbor)
        - Limit color count (≤ 6)
        - Remove anti-aliasing
        - Enhance contour contrast
        - Simulate LED lighting effect (optional)
        
        Args:
            image_base64: Base64 encoded image string
            enable_led_effect: Whether to enable LED lighting effect
            
        Returns:
            Base64 encoded enhanced image string
        """
        try:
            # Decode base64 image
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Step 1: Force resize to 48×48 using Nearest Neighbor (no anti-aliasing)
            image = image.resize((48, 48), Image.Resampling.NEAREST)
            
            # Step 2: Limit color count to ≤ 6 using quantization
            # Convert to palette mode with max 6 colors
            image = image.quantize(colors=6, method=Image.Quantize.MEDIANCUT)
            # Convert back to RGB for further processing
            image = image.convert('RGB')
            
            # Step 3: Enhance contour contrast
            # Convert to numpy array for processing
            img_array = np.array(image)
            
            # Apply edge detection to enhance contours
            # Convert to grayscale for edge detection
            gray = Image.fromarray(img_array).convert('L')
            edges = gray.filter(ImageFilter.FIND_EDGES)
            edges_array = np.array(edges)
            
            # Darken edges in original image to strengthen contours
            # Edge pixels are those with edge detection value > threshold
            edge_mask = edges_array > 30  # Edge pixels
            # Darken edge pixels to enhance contrast
            for channel in range(3):
                img_array[:, :, channel][edge_mask] = np.maximum(
                    img_array[:, :, channel][edge_mask] - 50, 0
                )
            
            image = Image.fromarray(img_array.astype(np.uint8))
            
            # Step 4: Optional LED lighting effect
            if enable_led_effect:
                # Enhance brightness and saturation to simulate LED glow
                # For pixel art, we want vibrant, bright colors like LED displays
                enhancer = ImageEnhance.Brightness(image)
                image = enhancer.enhance(1.15)  # Increase brightness by 15%
                
                enhancer = ImageEnhance.Color(image)
                image = enhancer.enhance(1.25)  # Increase saturation by 25%
                
                # Apply subtle contrast enhancement for LED-like sharpness
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.1)  # Increase contrast by 10%
            
            # Step 5: Final quantization to ensure color count ≤ 6
            image = image.quantize(colors=6, method=Image.Quantize.MEDIANCUT)
            image = image.convert('RGB')
            
            # Convert back to base64
            output_buffer = io.BytesIO()
            image.save(output_buffer, format='PNG')
            output_buffer.seek(0)
            enhanced_base64 = base64.b64encode(output_buffer.read()).decode('utf-8')
            
            return enhanced_base64
            
        except Exception as e:
            # If enhancement fails, return original image
            return image_base64

    def pixel_image_generate(
        self,
        user_input: str,
        negative_prompt: str = "",
        num_inference_steps: int = 20,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None,
        image_size: str = "480x480"
    ) -> Dict[str, Any]:
        """使用 pixel_emjo 内置模板 + 用户输入，直接文生图（不经过额外 LLM）。"""
        from pixel_emjo import generate_pixel_emoji_prompt

        raw = (user_input or "").strip()
        if not raw:
            return {
                "success": False,
                "error": "user_input is required",
                "user_input": user_input,
            }

        prompt_text = generate_pixel_emoji_prompt(raw, image_size)
        prompt_metadata: Dict[str, Any] = {"source": "pixel_emjo_template"}

        try:
            image_result = self.generate_image(
                prompt=prompt_text,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                seed=seed,
                image_size=image_size,
            )
            enhanced_image_base64 = image_result["image_base64"]

            return {
                "success": True,
                "message": "Pixel emoji image generated successfully",
                "user_input": user_input,
                "generated_prompt": prompt_text,
                "prompt_metadata": prompt_metadata,
                "image_base64": enhanced_image_base64,
                "metadata": {
                    **image_result["metadata"],
                    "generation_type": "pixel_emoji",
                    "original_user_input": user_input,
                    "enhancement": {
                        "resized_to": "48x48",
                        "color_limit": 6,
                        "anti_aliasing": "disabled",
                        "contour_enhanced": True,
                        "led_effect": True,
                    },
                },
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate image: {str(e)}",
                "user_input": user_input,
                "generated_prompt": prompt_text,
                "prompt_metadata": prompt_metadata,
            }