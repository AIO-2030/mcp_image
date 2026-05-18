import asyncio
import os
import time
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.fastmcp.tools import Tool
from image_service import ImageService

# Create MCP server instance
mcp = Server("Image Generation MCP")

# Initialize ImageService（阿里云 DashScope，密钥见环境变量 DASHSCOPE_API_KEY）
service = ImageService(
    api_url=None,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
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
    """Generate image from text prompt using Alibaba Cloud DashScope"""
    return service.generate_image(prompt, negative_prompt, num_inference_steps, guidance_scale, seed, image_size)

@Tool.from_function
def image_generation_prompt(prompt: str) -> str:
    """Create an image generation prompt template"""
    return service.image_generation_prompt(prompt)

@Tool.from_function
async def image_resource(image_path: str) -> str:
    """Provide image file content as a resource"""
    return service.image_resource(image_path)

@Tool.from_function
async def pixel_image_generate(user_input: str, negative_prompt: str = "", num_inference_steps: int = 20,
                             guidance_scale: float = 7.5, seed: int = None, image_size: str = "1024x1024") -> dict:
    """Generate pixel LED-matrix style image using the built-in template (no extra LLM)"""
    return service.pixel_image_generate(user_input, negative_prompt, num_inference_steps, guidance_scale, seed, image_size)

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await mcp.run(read_stream, write_stream, {})

if __name__ == "__main__":
    asyncio.run(main()) 