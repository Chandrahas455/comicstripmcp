#!/usr/bin/env python3
"""
Test with the exact same data that works for the black and white tool.
"""

import base64
import io
from PIL import Image

def test_base64_image_string():
    """Test the exact string 'Base64 Image' that works for the black and white tool."""
    test_data = "Base64 Image"
    
    print(f"Testing with: '{test_data}'")
    print(f"Length: {len(test_data)}")
    
    try:
        # Try to decode
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

def test_mxaendal_string():
    """Test the string that fails for the comic tool."""
    test_data = "MXAENdal"
    
    print(f"\nTesting with: '{test_data}'")
    print(f"Length: {len(test_data)}")
    
    try:
        # Try to decode
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

def test_valid_image():
    """Test with a real valid image."""
    # Create a simple test image
    test_image = Image.new('RGB', (100, 100), color='red')
    
    # Convert to base64
    buffer = io.BytesIO()
    test_image.save(buffer, format='PNG')
    image_bytes = buffer.getvalue()
    valid_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    print(f"\nTesting with valid image base64:")
    print(f"Length: {len(valid_base64)}")
    print(f"Preview: {valid_base64[:50]}...")
    
    try:
        # Try to decode
        decoded_bytes = base64.b64decode(valid_base64)
        print(f"✅ Base64 decode successful, bytes length: {len(decoded_bytes)}")
        
        # Try to open as image
        image = Image.open(io.BytesIO(decoded_bytes))
        print(f"✅ Image opened successfully: {image.size} {image.mode}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Exact Data ===\n")
    
    # Test the data that works for black and white tool
    base64_image_works = test_base64_image_string()
    
    # Test the data that fails for comic tool
    mxaendal_works = test_mxaendal_string()
    
    # Test with real valid data
    valid_works = test_valid_image()
    
    print(f"\n=== Results ===")
    print(f"'Base64 Image' works: {base64_image_works}")
    print(f"'MXAENdal' works: {mxaendal_works}")
    print(f"Real base64 works: {valid_works}")
    
    if base64_image_works and not mxaendal_works:
        print(f"\n🎯 The issue is clear: 'Base64 Image' is valid data, 'MXAENdal' is not!")
        print(f"The client is sending different data to different tools.") 