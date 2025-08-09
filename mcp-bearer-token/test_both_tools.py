#!/usr/bin/env python3
"""
Test script to compare how both tools handle the same base64 data.
"""

import asyncio
import base64
import io
from PIL import Image, ImageDraw

def create_test_image():
    """Create a test image."""
    img = Image.new('RGB', (200, 200), color='lightblue')
    draw = ImageDraw.Draw(img)
    draw.rectangle([50, 50, 150, 150], fill='red', outline='black', width=3)
    draw.ellipse([75, 75, 125, 125], fill='yellow')
    return img

def encode_image_to_base64(image):
    """Encode image to base64 string."""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    image_bytes = buffer.getvalue()
    base64_string = base64.b64encode(image_bytes).decode('utf-8')
    return base64_string

async def test_both_tools():
    """Test both tools with the same valid data."""
    
    # Create test image and encode to base64
    test_image = create_test_image()
    base64_data = encode_image_to_base64(test_image)
    
    print(f"✅ Generated valid base64 data:")
    print(f"Length: {len(base64_data)} characters")
    print(f"Preview: {base64_data[:50]}...")
    
    # Import the tools
    from mcp_starter import make_img_black_and_white, generate_comic_strip_tool
    
    print("\n🧪 Testing make_img_black_and_white tool...")
    try:
        result = await make_img_black_and_white(puch_image_data=base64_data)
        print(f"✅ Black and white tool successful!")
        print(f"Result type: {type(result)}")
        print(f"Number of content items: {len(result)}")
        for i, content in enumerate(result):
            print(f"  Content {i+1}: {content.type}")
            if content.type == "image":
                print(f"    Image data length: {len(content.data)} characters")
    except Exception as e:
        print(f"❌ Black and white tool failed: {e}")
    
    print("\n🧪 Testing generate_comic_strip_tool...")
    try:
        result = await generate_comic_strip_tool(
            base_image_data=base64_data,
            story_guide="A silly comic about dogs",
            character_name="Ramesh"
        )
        print(f"✅ Comic generation tool successful!")
        print(f"Result type: {type(result)}")
        print(f"Number of content items: {len(result)}")
        for i, content in enumerate(result):
            print(f"  Content {i+1}: {content.type}")
            if content.type == "text":
                print(f"    Text preview: {content.text[:100]}...")
            elif content.type == "image":
                print(f"    Image data length: {len(content.data)} characters")
    except Exception as e:
        print(f"❌ Comic generation tool failed: {e}")

def test_invalid_data():
    """Test with the invalid data from the error."""
    invalid_data = "MXAENdal"
    
    print(f"\n🧪 Testing with invalid data: '{invalid_data}'")
    
    try:
        # Test base64 decode
        decoded_bytes = base64.b64decode(invalid_data)
        print(f"✅ Base64 decode successful, bytes length: {len(decoded_bytes)}")
        
        # Test PIL open
        image = Image.open(io.BytesIO(decoded_bytes))
        print(f"✅ PIL open successful: {image.size} {image.mode}")
        
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    print("=== Tool Comparison Test ===\n")
    
    # Test with invalid data first
    test_invalid_data()
    
    # Test both tools with valid data
    asyncio.run(test_both_tools())
    
    print("\n=== Test Complete ===") 