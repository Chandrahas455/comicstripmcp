#!/usr/bin/env python3
"""
Direct test of the black and white tool with the exact data that supposedly works.
"""

import asyncio
import base64
import io
from PIL import Image

async def test_black_white_tool():
    """Test the black and white tool with 'Base64 Image'."""
    
    # Import the tool
    from mcp_starter import make_img_black_and_white
    
    test_data = "Base64 Image"
    print(f"Testing black and white tool with: '{test_data}'")
    
    try:
        result = await make_img_black_and_white(puch_image_data=test_data)
        print(f"✅ Black and white tool successful!")
        print(f"Result type: {type(result)}")
        print(f"Number of content items: {len(result)}")
        for i, content in enumerate(result):
            print(f"  Content {i+1}: {content.type}")
            if content.type == "image":
                print(f"    Image data length: {len(content.data)} characters")
        return True
    except Exception as e:
        print(f"❌ Black and white tool failed: {e}")
        return False

def test_base64_decode():
    """Test what happens when we decode 'Base64 Image'."""
    test_data = "Base64 Image"
    print(f"\nTesting base64 decode of: '{test_data}'")
    
    try:
        decoded_bytes = base64.b64decode(test_data)
        print(f"✅ Base64 decode successful, bytes length: {len(decoded_bytes)}")
        print(f"First few bytes: {decoded_bytes[:10]}")
        
        # Try to open as image
        image = Image.open(io.BytesIO(decoded_bytes))
        print(f"✅ Image opened successfully: {image.size} {image.mode}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def test_with_padding():
    """Test with padding added."""
    test_data = "Base64 Image"
    # Add padding
    padded_data = test_data + "=" * (4 - len(test_data) % 4)
    print(f"\nTesting with padding: '{padded_data}'")
    
    try:
        decoded_bytes = base64.b64decode(padded_data)
        print(f"✅ Base64 decode successful, bytes length: {len(decoded_bytes)}")
        print(f"First few bytes: {decoded_bytes[:10]}")
        
        # Try to open as image
        image = Image.open(io.BytesIO(decoded_bytes))
        print(f"✅ Image opened successfully: {image.size} {image.mode}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Direct Black and White Tool Test ===\n")
    
    # Test base64 decode
    decode_works = test_base64_decode()
    
    # Test with padding
    padding_works = test_with_padding()
    
    # Test the actual tool
    tool_works = asyncio.run(test_black_white_tool())
    
    print(f"\n=== Results ===")
    print(f"Base64 decode works: {decode_works}")
    print(f"With padding works: {padding_works}")
    print(f"Tool works: {tool_works}")
    
    if not decode_works and tool_works:
        print(f"\n🤔 Interesting! The tool works but base64 decode fails.")
        print(f"This suggests the tool might be handling the error differently.") 