#!/usr/bin/env python3
"""
Generate a test image and base64 data for testing the comic generation tool.
"""

import base64
import io
from PIL import Image, ImageDraw

def create_test_image():
    """Create a test image with some content."""
    # Create a 300x300 image with a gradient background
    img = Image.new('RGB', (300, 300), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Add some shapes
    draw.rectangle([50, 50, 250, 250], fill='red', outline='black', width=3)
    draw.ellipse([100, 100, 200, 200], fill='yellow')
    draw.text((120, 140), "TEST", fill='black')
    
    return img

def encode_image_to_base64(image):
    """Encode image to base64 string."""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    image_bytes = buffer.getvalue()
    base64_string = base64.b64encode(image_bytes).decode('utf-8')
    return base64_string

def main():
    print("Creating test image...")
    test_image = create_test_image()
    
    print("Encoding to base64...")
    base64_data = encode_image_to_base64(test_image)
    
    print(f"✅ Generated valid base64 data:")
    print(f"Length: {len(base64_data)} characters")
    print(f"Preview: {base64_data[:100]}...")
    
    # Save the test image
    test_image.save("test_image.png")
    print("✅ Saved test image as 'test_image.png'")
    
    # Test decoding
    print("\nTesting base64 decoding...")
    try:
        decoded_bytes = base64.b64decode(base64_data)
        decoded_image = Image.open(io.BytesIO(decoded_bytes))
        print(f"✅ Successfully decoded: {decoded_image.size} {decoded_image.mode}")
    except Exception as e:
        print(f"❌ Decoding failed: {e}")
    
    print(f"\n🎯 Use this base64 data to test the comic generation tool:")
    print(f"base_image_data='{base64_data}'")
    
    print(f"\n📝 Example tool call:")
    print(f"generate_comic_strip_tool(")
    print(f"    base_image_data='{base64_data}',")
    print(f"    story_guide='A silly comic about dogs',")
    print(f"    character_name='Ramesh'")
    print(f")")

if __name__ == "__main__":
    main() 