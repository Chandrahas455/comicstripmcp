#!/usr/bin/env python3
"""
Test script to demonstrate proper image encoding for the comic generation tool.
This script shows how to properly encode an image to base64 format.
"""

import base64
import io
from PIL import Image
import os

def create_test_image():
    """Create a simple test image."""
    # Create a 200x200 test image with some colors
    img = Image.new('RGB', (200, 200), color='lightblue')
    
    # Add some simple shapes for testing
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.rectangle([50, 50, 150, 150], fill='red', outline='black', width=3)
    draw.ellipse([75, 75, 125, 125], fill='yellow')
    
    return img

def encode_image_to_base64(image):
    """Encode a PIL Image to base64 string."""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    image_bytes = buffer.getvalue()
    base64_string = base64.b64encode(image_bytes).decode('utf-8')
    return base64_string

def test_base64_encoding():
    """Test base64 encoding and decoding."""
    print("Creating test image...")
    test_image = create_test_image()
    
    print("Encoding image to base64...")
    base64_data = encode_image_to_base64(test_image)
    
    print(f"Base64 data length: {len(base64_data)} characters")
    print(f"Base64 data preview: {base64_data[:50]}...")
    
    # Test decoding
    print("\nTesting base64 decoding...")
    try:
        decoded_bytes = base64.b64decode(base64_data)
        decoded_image = Image.open(io.BytesIO(decoded_bytes))
        print(f"✅ Successfully decoded image: {decoded_image.size} {decoded_image.mode}")
        
        # Save the decoded image to verify
        decoded_image.save("test_decoded.png")
        print("✅ Saved decoded image as 'test_decoded.png'")
        
        return base64_data
        
    except Exception as e:
        print(f"❌ Failed to decode base64 data: {e}")
        return None

def test_invalid_base64():
    """Test with invalid base64 data."""
    print("\nTesting invalid base64 data...")
    invalid_data = "MXAENdal"  # This is the invalid data from the error
    
    try:
        decoded_bytes = base64.b64decode(invalid_data)
        print(f"Decoded bytes length: {len(decoded_bytes)}")
        
        # Try to open as image
        decoded_image = Image.open(io.BytesIO(decoded_bytes))
        print(f"Image opened: {decoded_image.size}")
        
    except Exception as e:
        print(f"❌ Invalid base64 data failed as expected: {e}")

if __name__ == "__main__":
    print("=== Image Base64 Encoding Test ===\n")
    
    # Test valid encoding
    valid_base64 = test_base64_encoding()
    
    # Test invalid encoding
    test_invalid_base64()
    
    if valid_base64:
        print(f"\n✅ Valid base64 data for testing:")
        print(f"Length: {len(valid_base64)} characters")
        print(f"Preview: {valid_base64[:100]}...")
        
        print(f"\nYou can use this base64 data to test the comic generation tool:")
        print(f"base_image_data='{valid_base64[:50]}...'")
    
    print("\n=== Test Complete ===") 