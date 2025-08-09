#!/usr/bin/env python3
"""
Debug script to test the invalid base64 data that's causing the error.
"""

import base64
import io
from PIL import Image

def test_invalid_base64():
    """Test the exact invalid base64 data from the error."""
    invalid_data = "MXAENdal"  # This is the data from the error
    
    print(f"Testing invalid base64 data: '{invalid_data}'")
    print(f"Length: {len(invalid_data)}")
    
    try:
        # Try to decode
        decoded_bytes = base64.b64decode(invalid_data)
        print(f"✅ Base64 decode successful, bytes length: {len(decoded_bytes)}")
        print(f"First few bytes: {decoded_bytes[:10]}")
        
        # Try to open as image
        image = Image.open(io.BytesIO(decoded_bytes))
        print(f"✅ Image opened successfully: {image.size} {image.mode}")
        
    except Exception as e:
        print(f"❌ Failed: {e}")

def test_valid_base64():
    """Test with valid base64 data."""
    # Create a simple test image
    test_image = Image.new('RGB', (100, 100), color='red')
    
    # Convert to base64
    buffer = io.BytesIO()
    test_image.save(buffer, format='PNG')
    image_bytes = buffer.getvalue()
    valid_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    print(f"\nTesting valid base64 data:")
    print(f"Length: {len(valid_base64)}")
    print(f"Preview: {valid_base64[:50]}...")
    
    try:
        # Try to decode
        decoded_bytes = base64.b64decode(valid_base64)
        print(f"✅ Base64 decode successful, bytes length: {len(decoded_bytes)}")
        
        # Try to open as image
        image = Image.open(io.BytesIO(decoded_bytes))
        print(f"✅ Image opened successfully: {image.size} {image.mode}")
        
        return valid_base64
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        return None

def test_base64_padding():
    """Test if padding is the issue."""
    invalid_data = "MXAENdal"
    
    # Try with different padding
    padded_data = invalid_data + "=" * (4 - len(invalid_data) % 4)
    print(f"\nTesting with padding: '{padded_data}'")
    
    try:
        decoded_bytes = base64.b64decode(padded_data)
        print(f"✅ Padded decode successful, bytes length: {len(decoded_bytes)}")
        
        # Try to open as image
        image = Image.open(io.BytesIO(decoded_bytes))
        print(f"✅ Image opened successfully: {image.size} {image.mode}")
        
    except Exception as e:
        print(f"❌ Padded decode failed: {e}")

if __name__ == "__main__":
    print("=== Base64 Debug Test ===\n")
    
    # Test the invalid data
    test_invalid_base64()
    
    # Test padding
    test_base64_padding()
    
    # Test valid data
    valid_data = test_valid_base64()
    
    if valid_data:
        print(f"\n✅ Valid base64 data for testing:")
        print(f"Use this in your tool call: base_image_data='{valid_data}'")
    
    print("\n=== Debug Complete ===") 