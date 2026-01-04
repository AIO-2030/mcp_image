import os
import time
import base64
import json
import re
from typing import Dict, Any, Optional
import requests
from PIL import Image, ImageFilter, ImageEnhance
import io
import numpy as np

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

    def _extract_value_by_keyword(self, content: str, keyword: str) -> Optional[str]:
        """
        通过关键字key和字符串index+length来匹配提取值
        支持多种格式：key: "value", key: 'value', key: value, key="value"等
        优化版本：确保提取完整正确的值
        """
        # 查找关键字的位置，按优先级排序（更精确的模式优先）
        keyword_patterns = [
            f'"{keyword}":',  # "image_prompt":
            f"'{keyword}':",  # 'image_prompt':
            f'"{keyword}"',  # "image_prompt"
            f"'{keyword}'",  # 'image_prompt'
            f"{keyword}:",  # image_prompt:
            f"{keyword}=",  # image_prompt=
        ]
        
        for pattern in keyword_patterns:
            index = content.find(pattern)
            if index != -1:
                # 找到关键字后的位置
                start_pos = index + len(pattern)
                # 跳过空白字符
                while start_pos < len(content) and content[start_pos] in ' \t\n\r':
                    start_pos += 1
                
                if start_pos >= len(content):
                    continue
                
                # 如果下一个字符是引号，提取引号内的内容
                if content[start_pos] in ['"', "'"]:
                    quote_char = content[start_pos]
                    start_pos += 1  # 跳过开始引号
                    end_pos = start_pos
                    # 查找结束引号（考虑转义）
                    found_end = False
                    while end_pos < len(content):
                        if content[end_pos] == quote_char:
                            # 检查是否是转义的引号
                            escape_count = 0
                            check_pos = end_pos - 1
                            while check_pos >= 0 and content[check_pos] == '\\':
                                escape_count += 1
                                check_pos -= 1
                            # 如果是偶数个反斜杠，说明引号没有被转义
                            if escape_count % 2 == 0:
                                found_end = True
                                break
                        end_pos += 1
                    
                    if found_end:
                        # 提取值（使用index和length）
                        value = content[start_pos:end_pos]
                        # 处理转义字符
                        value = value.replace('\\"', '"').replace("\\'", "'").replace('\\n', '\n').replace('\\t', '\t').replace('\\\\', '\\')
                        # 清理值，移除异常信息关键词
                        if self._contains_error_info(value):
                            return None
                        return value.strip()
                else:
                    # 如果不是引号，提取到下一个分隔符
                    # 对于JSON格式，需要更智能地判断结束位置
                    end_pos = start_pos
                    bracket_count = 0
                    brace_count = 0
                    in_string = False
                    string_char = None
                    
                    while end_pos < len(content):
                        char = content[end_pos]
                        
                        # 处理字符串内的字符
                        if in_string:
                            if char == string_char:
                                # 检查是否是转义的引号
                                escape_count = 0
                                check_pos = end_pos - 1
                                while check_pos >= 0 and content[check_pos] == '\\':
                                    escape_count += 1
                                    check_pos -= 1
                                if escape_count % 2 == 0:
                                    in_string = False
                                    string_char = None
                            end_pos += 1
                            continue
                        
                        # 检查是否进入字符串
                        if char in ['"', "'"]:
                            in_string = True
                            string_char = char
                            end_pos += 1
                            continue
                        
                        # 处理括号和花括号
                        if char == '[':
                            bracket_count += 1
                        elif char == ']':
                            bracket_count -= 1
                        elif char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                        
                        # 如果遇到分隔符且不在嵌套结构中，结束提取
                        if char in [',', '\n', '\r'] and bracket_count == 0 and brace_count == 0:
                            break
                        
                        # 如果遇到结束括号且不在字符串中，可能是值的结束
                        if char in ['}', ']'] and bracket_count < 0 and brace_count < 0:
                            break
                        
                        end_pos += 1
                    
                    if end_pos > start_pos:
                        value = content[start_pos:end_pos].strip()
                        # 移除可能的尾随引号、逗号等
                        value = value.rstrip(',')
                        if value.endswith('"') or value.endswith("'"):
                            value = value[:-1].strip()
                        if value:
                            # 清理值，移除异常信息关键词
                            if self._contains_error_info(value):
                                return None
                            return value.strip()
        
        return None
    
    def _contains_error_info(self, text: str) -> bool:
        """检查文本是否包含异常信息或错误消息"""
        error_keywords = [
            "error",
            "exception",
            "failed",
            "parsing failed",
            "JSON parsing failed",
            "extracted by keyword",
            "traceback",
            "Traceback"
        ]
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in error_keywords)

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
            
            # Clean the content - remove markdown code blocks if present
            cleaned_content = llm_content.strip()
            if cleaned_content.startswith("```json"):
                cleaned_content = cleaned_content[7:]  # Remove ```json
            elif cleaned_content.startswith("```"):
                cleaned_content = cleaned_content[3:]  # Remove ```
            if cleaned_content.endswith("```"):
                cleaned_content = cleaned_content[:-3]  # Remove trailing ```
            cleaned_content = cleaned_content.strip()
            
            # Try to parse JSON response
            try:
                parsed_result = json.loads(cleaned_content)
                
                # Ensure parsed_result is a dictionary
                if not isinstance(parsed_result, dict):
                    raise ValueError("Parsed result is not a dictionary")
                
                return {
                    "success": True,
                    "user_input": user_input,
                    "llm_response": parsed_result,
                    "image_prompt": parsed_result.get("image_prompt", ""),
                    "intent_summary": parsed_result.get("intent_summary", ""),
                    "style": parsed_result.get("style", "pixel art, emoji-style"),
                    "notes": parsed_result.get("notes", "")
                }
            except (json.JSONDecodeError, ValueError) as e:
                # If JSON parsing fails, use keyword-based extraction with index+length
                # 使用关键字key和字符串index+length来匹配提取，无需强行修复格式
                extracted_image_prompt = self._extract_value_by_keyword(cleaned_content, "image_prompt")
                extracted_intent_summary = self._extract_value_by_keyword(cleaned_content, "intent_summary")
                extracted_style = self._extract_value_by_keyword(cleaned_content, "style")
                extracted_notes = self._extract_value_by_keyword(cleaned_content, "notes")
                
                # 如果所有解析尝试都失败，使用默认值，确保不包含异常信息
                # 检查 cleaned_content 是否包含异常信息
                safe_content = cleaned_content if cleaned_content and not self._contains_error_info(cleaned_content) else None
                
                return {
                    "success": True,
                    "user_input": user_input,
                    "llm_response": llm_content,
                    "image_prompt": extracted_image_prompt if extracted_image_prompt else (safe_content if safe_content else f"pixel art emoji of {user_input}"),
                    "intent_summary": extracted_intent_summary if extracted_intent_summary else f"Generated prompt for: {user_input}",
                    "style": extracted_style if extracted_style else "pixel art, emoji-style",
                    "notes": extracted_notes if extracted_notes else ""
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "user_input": user_input
            }

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
        """Generate pixel emoji style images"""
        # Step 1: Generate prompt using LLM
        prompt_result = self.generate_pixel_emoji_prompt(user_input, image_size)
        
        # Check if prompt_result is a dict and has success key
        if not isinstance(prompt_result, dict) or not prompt_result.get("success", False):
            return {
                "success": False,
                "error": f"Failed to generate prompt: {prompt_result.get('error', 'Unknown error')}",
                "user_input": user_input
            }
        
        # Step 2: Generate image using the generated prompt
        # Safely get style and image_prompt with defaults
        style = prompt_result.get("style", "pixel art, emoji-style")
        image_prompt_text = prompt_result.get("image_prompt", "")
        
        # If image_prompt is empty, try to extract from llm_response
        if not image_prompt_text:
            llm_response = prompt_result.get("llm_response", {})
            if isinstance(llm_response, dict):
                image_prompt_text = llm_response.get("image_prompt", "")
            elif isinstance(llm_response, str):
                # 如果 llm_response 是字符串，尝试从中提取 image_prompt，而不是直接使用
                # 避免将异常信息或错误消息放入 prompts
                if not self._contains_error_info(llm_response):
                    # 尝试提取 image_prompt
                    extracted = self._extract_value_by_keyword(llm_response, "image_prompt")
                    image_prompt_text = extracted if extracted else ""
                else:
                    image_prompt_text = ""
        
        # If still empty, use a default prompt
        if not image_prompt_text:
            image_prompt_text = f"pixel art emoji of {user_input}"
        
        image_prompt = f"{style}, {image_prompt_text}"
        
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
            
            # Step 3: Enhance the generated image
            # enhanced_image_base64 = self.enhance_pixel_emoji_image(
            #     image_result["image_base64"],
            #     enable_led_effect=True
            # )
            enhanced_image_base64 = image_result["image_base64"]

            
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
                        "led_effect": True
                    }
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