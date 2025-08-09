#!/usr/bin/env python3
"""
Test script for the comic generation MCP tool.
This script tests the generate_comic_strip_tool function directly.
"""

import asyncio
import base64
import os
from PIL import Image
import io

# Import the MCP tool function
from mcp_starter import generate_comic_strip_tool

async def test_comic_generation():
    """Test the comic generation tool with a sample image."""
    
    # Create a more interesting test image
    test_image = Image.new('RGB', (200, 200), color='lightblue')
    
    # Add some simple shapes for testing
    from PIL import ImageDraw
    draw = ImageDraw.Draw(test_image)
    draw.rectangle([50, 50, 150, 150], fill='red', outline='black', width=3)
    draw.ellipse([75, 75, 125, 125], fill='yellow')
    
    # Convert to base64
    buffer = io.BytesIO()
    test_image.save(buffer, format='PNG')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    print("Testing comic generation tool...")
    
    try:
        # Test the tool
        result = await generate_comic_strip_tool(
            base_image_data=image_base64,
            story_guide="Make jokes about programming",
            character_name="CodeMaster"
        )
        
        print("✅ Comic generation successful!")
        print(f"Result type: {type(result)}")
        print(f"Number of content items: {len(result)}")
        
        for i, content in enumerate(result):
            print(f"Content {i+1}: {content.type}")
            if content.type == "text":
                print(f"Text content: {content.text[:100]}...")
            elif content.type == "image":
                print(f"Image data length: {len(content.data)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Comic generation failed: {e}")
        return False

if __name__ == "__main__":
    # Set up environment variables if needed
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  GEMINI_API_KEY not set. Please set it in your environment.")
        print("You can set it by running: export GEMINI_API_KEY='your_api_key_here'")
    
    if not os.getenv("AUTH_TOKEN"):
        print("⚠️  AUTH_TOKEN not set. Please set it in your environment.")
        print("You can set it by running: export AUTH_TOKEN='your_auth_token_here'")
    
    # Run the test
    success = asyncio.run(test_comic_generation())
    
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed!") 