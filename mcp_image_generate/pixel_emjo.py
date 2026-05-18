#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pixel LED-matrix style prompt template.
Builds the full English prompt string for the image model from user input (no LLM).
"""

def generate_pixel_emoji_prompt(user_input: str, image_size: str = "1024x1024") -> str:
    """
    Generate pixel emoji style image prompts based on user input

    Args:
        user_input (str): User's natural language input
        image_size (str): Image size in format "widthxheight" (e.g., "1024x1024"); reserved for callers, not embedded in this template.

    Returns:
        str: Formatted prompt with user input substituted into [SUBJECT]
    """
    _ = image_size  # 保留参数以兼容 image_service 等调用方

    prompt_template = """Generate a pure pixel-art sprite image for LED matrix sampling.

[CANVAS]
- Output image only
- Transparent or solid black background
- No mug
- No cup
- No product mockup
- No LED display device
- No environment
- No shadows
- No reflections
- No perspective
- No 3D rendering
- No photo-realistic style

[PIXEL ART REQUIREMENTS]
- The image must be a flat 2D pixel-art icon
- Low-resolution pixel grid style
- Designed for a 32 x 16 LED matrix
- Very simple silhouette
- High contrast
- Maximum 3 main colors
- Centered composition
- Clear edges
- Large blocky pixels
- No tiny details

[SUBJECT]
{{USER_INPUT}}

[STYLE]
Flat 2D pixel art sprite, retro LED matrix icon, clean, minimal, front-facing.

[OUTPUT]
Only generate the pixel-art image itself."""

    return prompt_template.replace("{{USER_INPUT}}", user_input.strip())


def generate_prompt_for_llm(user_input: str, image_size: str = "480x480") -> str:
    """
    生成可直接用于文生图模型的完整提示词（与 generate_pixel_emoji_prompt 相同）。

    Args:
        user_input (str): User input content
        image_size (str): Image size in format "widthxheight" (e.g., "480x480")

    Returns:
        str: Full prompt with [SUBJECT] filled from user input
    """
    return generate_pixel_emoji_prompt(user_input, image_size)


def test_prompt_generator():
    """Test function to demonstrate how to use the prompt generator"""
    test_inputs = [
        "我今天好累",
        "好开心！",
        "生气的猫",
        "I want a cute dog",
        "想要一个可爱的熊猫"
    ]
    
    print("=== Pixel Emoji Prompt Generator Test ===\n")
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"Test {i}: User Input = '{user_input}'")
        prompt = generate_prompt_for_llm(user_input)
        print("Generated Prompt:")
        print("-" * 50)
        print(prompt)
        print("=" * 80)
        print()


if __name__ == "__main__":
    # Run tests
    test_prompt_generator()
    
    # Interactive usage example
    print("\n=== Interactive Test ===")
    print("Please enter your input (type 'quit' to exit):")
    
    while True:
        user_input = input("\nUser Input: ").strip()
        if user_input.lower() == 'quit':
            break
        
        if user_input:
            prompt = generate_prompt_for_llm(user_input)
            print("\nGenerated LLM Prompt:")
            print("-" * 50)
            print(prompt)
        else:
            print("Please enter valid content")
