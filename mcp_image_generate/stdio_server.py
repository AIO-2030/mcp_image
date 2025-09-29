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
        elif method == "pixel_image_generate":
            result = service.pixel_image_generate(
                user_input=params.get("user_input"),
                negative_prompt=params.get("negative_prompt", ""),
                num_inference_steps=params.get("num_inference_steps", 20),
                guidance_scale=params.get("guidance_scale", 7.5),
                seed=params.get("seed"),
                image_size=params.get("image_size", "1024x1024")
            )
            response = {
                "jsonrpc": "2.0",
                "output": {
                    "type": "pixel_emoji_image",
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