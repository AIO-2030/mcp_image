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
CRITICAL: The image MUST contain EXACTLY ONE object, centered on the canvas. Standalone pictogram, not a scene, set, collection, grid, or multiple panels.
ABSOLUTELY FORBIDDEN: multiple objects, repeated items, rows, columns, shelves, grid layouts (2x2, 3x3, any grid), multiple panels, variations, or multiple instances.

# HARD CONSTRAINTS (must be followed exactly)
- Final image optimized for a 32x32 pixel LED display
- Construct the entire image ONLY using these primitives: circle, rectangle/quadrilateral, trapezoid, triangle, polygon, straight line
- NO organic curves except circles; NO hand-drawn shapes; NO detailed textures
- Maximum 3 visual elements total (main subject + 0–2 simple accessories such as a heart, star, or balloon)
- Maximum 4 colors total
- Flat solid colors only (pure color blocks) — NO gradients, NO shadows, NO blur, NO anti-aliasing
- No realistic or illustrated style
- Single centered subject, minimal background, clear silhouette
- Clean, minimal design: NO decorative lines, internal stripes, patterns, or unnecessary details. Only essential features for recognition.

# CRITICAL SINGLE OBJECT RULE (HIGHEST PRIORITY)
- The image MUST contain EXACTLY ONE object, centered and isolated. ABSOLUTELY FORBIDDEN: multiple objects, instances, grids, panels, rows, columns, or any multi-object layout.
- If input mentions "a cat" or "yellow cat", generate ONE cat only. Never interpret plural forms as permission for multiple objects.
- The image must be a single emoji icon, not a sprite sheet, grid, or multiple panels.

# Background Rules (CRITICAL: Background is separate from outline)
- Background: MUST be white or light color (white #FFFFFF, light cyan, light yellow, light pink, etc.) filling the entire frame, flat and uniform
- ABSOLUTELY FORBIDDEN: black, dark gray, or any dark colors as background. Background must be bright and light.
- No gradient, transparent background, or vignette. The background is a solid bright/light color field filling the entire canvas behind the subject

# Color Rules
- Use bright, saturated, vibrant colors only: yellow, red, blue, green, orange, pink, cyan, white
- Maximum 4 colors total (including background)
- The outline should use bright/vibrant colors that create strong visual contrast with the subject
- Rich color palette with high saturation for maximum visual impact

# Geometry Construction Rules (CRITICAL)
- Build each element as a combination of the allowed primitives:
  * Face/head: circle or polygon
  * Eyes: small circles or small rectangles
  * Mouth: short straight line(s) or a small trapezoid/triangle
  * Accessories: simple triangle/polygon star, circle balloon, polygon heart (blocky), etc.
- Use bold, blocky shapes with strong visual hierarchy
- Prefer large primitive shapes over many small details
- Use straight lines and hard edges for clarity on LED pixels

# Simplicity & Clean Design Rules (CRITICAL: Avoid unnecessary lines)
- Keep the design extremely simple and clean. Focus on the main subject only.
- ABSOLUTELY FORBIDDEN: decorative lines, internal stripes, patterns, horizontal/vertical lines across the face, unnecessary internal details, or any lines that don't serve a clear purpose (eyes, mouth, outline).
- Only include essential features: basic shape, eyes, mouth (if needed), and outline. NO decorative elements.
- The subject should be clean and minimal - avoid any internal decorative lines, stripes, or patterns.
- If a feature can be removed without losing recognition, remove it. Less is more.

# Outline Rules (CRITICAL: Outline is part of the subject, NOT the background)
- Bold outline (2–3 pixels thick) applied only to the subject's edges for 32x32 readability
- Outline MUST be bright/vibrant colors (white, bright yellow, bright cyan, bright pink, bright orange, bright green, etc.) that create strong contrast with the subject
- The outline should use rich, saturated colors that stand out against both the subject and the light background
- The outline belongs to the subject itself, defines its boundary, and is visually part of the subject (not the background)
- NEVER use dark colors (black, dark navy, dark gray) for the outline. Use bright, vibrant colors only.

# Emotion & Readability
- Emotion must be readable within 0.5 seconds
- Facial features must be exaggerated and simplified using primitives:
  * eyes: 2 dots or 2 small blocks (simple, no internal details)
  * mouth: 1–2 straight lines or a simple geometric wedge (minimal)
- NO decorative lines, stripes, or patterns inside the face or body
- Keep facial features minimal - only what's necessary for recognition

# Input
User input (may be non-English):
\"\"\"
{user_input}
\"\"\"

# CRITICAL INPUT INTERPRETATION RULE
- Regardless of input, generate a prompt for EXACTLY ONE object. If input is "A yellow cat" or "cat", generate ONE cat only.
- If input uses plural forms, interpret as ONE representative object. NEVER generate grids, multiple panels, rows, columns, or layouts showing more than one object.

# Output Format (STRICT JSON)
Return only the following JSON object and nothing else:

{{
  "intent_summary": "One concise English sentence describing the user's emotion or intent",
  "image_prompt": "A single English image prompt optimized for a 32x32 LED pixel display. MUST explicitly state: 'exactly ONE object', 'single isolated object', 'not a grid', 'not multiple objects', 'not a collection'. State that the image is constructed only from basic geometric primitives (circles, rectangles/quadrilaterals, trapezoids, triangles, polygons, and straight lines), with maximum 3 elements, limited colors, and extreme simplification for LED readability. The design must be clean and minimal - NO decorative lines, internal stripes, patterns, or unnecessary details. Only include essential features (basic shape, eyes, mouth if needed, outline). Separately specify: (1) solid white or light color background (NOT black or dark) filling entire canvas, (2) bold bright/vibrant colored outlines (white, bright yellow, bright cyan, bright pink, etc.) belonging to the subject that create strong contrast with both the subject and background. Explicitly forbid grids, multiple panels, rows, columns, decorative lines, internal patterns, or any multi-object layout.",
  "style": "retro pixel art, 8-bit style, strict pixel grid, sharp edges, bold line-based outlines, flat solid colors, no blur, no gradient, no anti-aliasing, clear silhouette, bright colors, strong subject-background separation, simple geometric shapes, clean minimal design, no decorative lines or patterns, emoji aesthetic, LED matrix display friendly, optimized for 32x32 display",
  "notes": "EXACTLY ONE object only, no grids, multiple objects, or panels. Constructed from basic geometric primitives, maximum 3 elements within single object, icon-level simplicity, clear silhouette, LED pixel visibility. Clean and minimal design - NO decorative lines, internal stripes, patterns, or unnecessary details. Only essential features (shape, eyes, mouth if needed, outline). Background: solid white or light color (NOT black or dark) filling entire canvas. Outline: bold 2–3px bright/vibrant colored stroke (white, bright yellow, bright cyan, bright pink, etc.) belonging to subject (not background), creating strong contrast with both subject and background, applied only to subject edges"
}}

# Image Prompt Composition Rules (MUST include)
The image_prompt MUST explicitly include:
- "32x32 pixel art emoji"
- "exactly ONE object" (MANDATORY) - "single isolated object", "not a grid", "not multiple objects", "not multiple panels"
- "constructed only from circles, rectangles/quadrilaterals, trapezoids, triangles, polygons, and straight lines"
- "maximum 3 elements" (within single object, not multiple objects)
- Exact color count (2–4 colors total)
- "extremely simplified, icon-level", "LED matrix display friendly"
- "clean and minimal design", "NO decorative lines, internal stripes, patterns, or unnecessary details"
- "only essential features" (basic shape, eyes, mouth if needed, outline)
- "no gradients, shadows, anti-aliasing, or textures"
- Explicitly list which primitives form the subject (e.g., "head is a circle, eyes are two small circles, mouth is a short line, accessory is a triangle star")

# Background & Outline Specification (describe separately)
- Background: named bright/light solid color (e.g., "solid white background", "light cyan background") filling entire canvas uniformly. MUST be white or light color, NOT black or dark.
- Outline: "bold 2–3px bright/vibrant colored outline" (white, bright yellow, bright cyan, bright pink, bright orange, etc.) belonging to the subject, creating strong contrast with both the subject and background. Part of subject's visual design, not background. NEVER use dark colors for outline.
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
