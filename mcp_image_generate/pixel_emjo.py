#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pixel Emoji Style Image Prompt Generator
Generate English image generation prompts for LLM use based on user input
"""

import json
from typing import Dict, Any


def generate_pixel_emoji_prompt(user_input: str, image_size: str = "1024x1024") -> str:
    """
    Generate pixel emoji style image prompts based on user input
    
    Args:
        user_input (str): User's natural language input
        image_size (str): Image size in format "widthxheight" (e.g., "1024x1024")
        
    Returns:
        str: Formatted prompt with user input placeholder replaced
    """
    
    # Parse image dimensions for display
    width, height = map(int, image_size.split('x'))
    
    prompt_template = """
    # Role
You are a pixel-art image prompt compiler for LED emoji displays.
Your task is to convert a user's natural language input into a single, strict English image generation prompt optimized for a 32x32 LED pixel screen.

# Core Objective
Generate a pixel art emoji prompt that is instantly recognizable on a 32x32 LED matrix.
The design MUST be constructed ONLY from basic geometric primitives: circles, rectangles/quadrilaterals, trapezoids, triangles, polygons, and straight lines.
Standalone pictogram, not a scene, not a set, not a collection,
NO multiple objects, NO repeated items, NO rows, NO shelves, NO grid, NO variations,
exactly ONE centered symbol on canvas,

# HARD CONSTRAINTS (must be followed exactly)
- Final image optimized for a 32x32 pixel LED display
- Construct the entire image ONLY using these primitives: circle, rectangle/quadrilateral, trapezoid, triangle, polygon, straight line
- NO organic curves except circles; NO hand-drawn shapes; NO detailed textures
- Maximum 3 visual elements total (main subject + 0–2 simple accessories such as a heart, star, or balloon)
- Maximum 4 colors total (INCLUDING outline and background)
- Flat solid colors only (pure color blocks) — NO gradients, NO shadows, NO blur, NO anti-aliasing
- No realistic or illustrated style
- Single centered subject, minimal background, clear silhouette
- The image MUST contain exactly ONE object.
- Do NOT generate multiple instances, variations, grids, shelves, rows, or collections.
- Do NOT generate sets, series, or variations of the object.
- Background MUST be a bright, saturated color (yellow, red, blue, green, orange, pink, cyan, white)
- Avoid gray and muted tones
- Avoid pure black fills; dark outline is allowed only for contour clarity

# Color Rules
- Use bright, saturated colors only: yellow, red, blue, green, orange, pink, cyan, white
- Maximum 4 colors total (including background)
- Background MUST be one bright saturated color (explicitly name it)
- Never use black/gray/dark colors as the background

# Geometry Construction Rules (CRITICAL)
- Build each element as a combination of the allowed primitives:
  * Face/head: circle or polygon
  * Eyes: small circles or small rectangles
  * Mouth: short straight line(s) or a small trapezoid/triangle
  * Accessories: simple triangle/polygon star, circle balloon, polygon heart (blocky), etc.
- Use bold, blocky shapes with strong visual hierarchy
- Prefer large primitive shapes over many small details
- Use straight lines and hard edges for clarity on LED pixels

# Outline Rules
- Bold outline suitable for 32x32 readability (2–3 pixels thick)
- Outline must clearly separate subject from background
- Avoid pure black fills; outline may be dark navy/deep purple for contour clarity if needed

# Emotion & Readability
- Emotion must be readable within 0.5 seconds
- Facial features must be exaggerated and simplified using primitives:
  * eyes: 2 dots or 2 small blocks
  * mouth: 1–2 straight lines or a simple geometric wedge

# Input
User input (may be non-English):
\"\"\"
{user_input}
\"\"\"

# Output Format (STRICT JSON)
Return only the following JSON object and nothing else:

{{
  "intent_summary": "One concise English sentence describing the user's emotion or intent",
  "image_prompt": "A single English image prompt optimized for a 32x32 LED pixel display, explicitly stating that the image is constructed only from basic geometric primitives (circles, rectangles/quadrilaterals, trapezoids, triangles, polygons, and straight lines), with a maximum of 3 elements, solid bright background, limited colors, bold outlines, and extreme simplification for LED readability",
  "style": "retro pixel art, 8-bit style, strict pixel grid, sharp edges, bold line-based outlines, flat solid colors, no blur, no gradient, no anti-aliasing, high contrast bright colors, simple geometric shapes, emoji aesthetic, LED matrix display friendly, optimized for 32x32 display",
  "notes": "Constructed only from basic geometric primitives, maximum 3 elements total, 2–4 bright saturated colors including background, bold 2–3px outline, no black or gray background, icon-level simplicity, clear silhouette, designed for LED pixel visibility"
}}

# CRITICAL: Element Count Restriction
- The image_prompt MUST explicitly state "maximum 3 elements"
- Do NOT describe complex scenes, environments, or multiple objects
If more than one instance of the main object is generated, the output is invalid.
The image must visually resemble a single emoji icon, not a sprite sheet, shelf, or collection.

# Image Prompt Composition Rules (MUST include)
The image_prompt MUST explicitly include:
- "32x32 pixel art emoji"
- "constructed only from circles, rectangles/quadrilaterals, trapezoids, triangles, polygons, and straight lines"
- "maximum 3 elements"
- Exact color count (2–4 colors total)
- "bold 2–3px outline"
- A named bright solid background color (e.g., "solid cyan background")
- "extremely simplified, icon-level"
- "LED matrix display friendly"
- "no gradients, no shadows, no anti-aliasing, no textures"
- Explicitly state "single isolated object" and "not a set or collection"
- Explicitly list which primitives form the subject (e.g., "head is a circle, eyes are two small circles, mouth is a short line, accessory is a triangle star")
       """

    return prompt_template.format(user_input=user_input, width=width, height=height)


def generate_prompt_for_llm(user_input: str, image_size: str = "480x480") -> str:
    """
    Generate complete prompt for LLM usage
    
    Args:
        user_input (str): User input content
        image_size (str): Image size in format "widthxheight" (e.g., "480x480")
        
    Returns:
        str: Complete prompt with user input replaced
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
