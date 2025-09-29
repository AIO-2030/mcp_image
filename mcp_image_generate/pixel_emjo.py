#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pixel Emoji Style Image Prompt Generator
Generate English image generation prompts for LLM use based on user input
"""

import json
from typing import Dict, Any


def generate_pixel_emoji_prompt(user_input: str) -> str:
    """
    Generate pixel emoji style image prompts based on user input
    
    Args:
        user_input (str): User's natural language input
        
    Returns:
        str: Formatted prompt with user input placeholder replaced
    """
    
    prompt_template = """# Role
You are an expert emoji-style image prompt generator.
Your job is to analyze the user's natural language input, understand their emotional and semantic intent, and output a precise English prompt suitable for generating a simple, clear, pixel-friendly image (like a meme or emoji-style sticker).

# Goals
1. Parse the intent of the user's input.
2. Convert the intent into a concise, clear English image generation prompt.
3. The image prompt should:
   - Accurately reflect the user's intent and emotion.
   - Be simple in composition, easily recognizable.
   - Be suitable for pixel art or emoji-style rendering.
4. If the user input is **not in English**, automatically translate it before generating the English prompt.
5. Keep the final prompt **fully in English**.

# Input
User input (natural language, possibly in non-English):
\"\"\"
{user_input}
\"\"\"

# Output format
Return a structured JSON object:

{{
  "intent_summary": "<one-sentence summary of user intent in English>",
  "image_prompt": "<final English prompt suitable for image generation>",
  "style": "pixel art, emoji-style, simple composition, clear expression",
  "notes": "Focus on the core idea, minimal background, easy to recognize"
}}

# Examples

## Example 1
User input: "我今天好累"
Output:
{{
  "intent_summary": "Feeling tired and exhausted",
  "image_prompt": "A sleepy cartoon face with droopy eyes and a pillow, pixel art emoji style",
  "style": "pixel art, emoji-style, simple composition, clear expression",
  "notes": "Minimal background, focus on sleepy face"
}}

## Example 2
User input: "好开心！"
Output:
{{
  "intent_summary": "Feeling very happy and joyful",
  "image_prompt": "A smiling cartoon face with stars around, expressing happiness, pixel art emoji style",
  "style": "pixel art, emoji-style, simple composition, clear expression",
  "notes": "Focus on joy and bright colors"
}}

## Example 3
User input: "生气的猫"
Output:
{{
  "intent_summary": "An angry cat",
  "image_prompt": "A cartoon angry cat with fur standing up and narrowed eyes, pixel art emoji style",
  "style": "pixel art, emoji-style, simple composition, clear expression",
  "notes": "Keep background plain"
}}

# Instructions
Now, read the user input and output the JSON strictly following the format above."""

    return prompt_template.format(user_input=user_input)


def generate_prompt_for_llm(user_input: str) -> str:
    """
    Generate complete prompt for LLM usage
    
    Args:
        user_input (str): User input content
        
    Returns:
        str: Complete prompt with user input replaced
    """
    return generate_pixel_emoji_prompt(user_input)


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
