#!/usr/bin/env python3
"""
Example showing how a client should properly call the comic generation tool.
This demonstrates the correct way to send base64 image data.
"""

import base64
import io
from PIL import Image, ImageDraw

def create_sample_image():
    """Create a sample image for testing."""
    img = Image.new('RGB', (300, 300), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Add some content
    draw.rectangle([50, 50, 250, 250], fill='red', outline='black', width=3)
    draw.ellipse([100, 100, 200, 200], fill='yellow')
    draw.text((120, 140), "DOG", fill='black')
    
    return img

def encode_image_to_base64(image):
    """Encode image to base64 string."""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    image_bytes = buffer.getvalue()
    base64_string = base64.b64encode(image_bytes).decode('utf-8')
    return base64_string

def main():
    print("=== Client Example: How to Call the Comic Tool ===\n")
    
    # Create a sample image
    sample_image = create_sample_image()
    sample_image.save("sample_dog_image.png")
    print("✅ Created sample image: sample_dog_image.png")
    
    # Encode to base64
    base64_data = encode_image_to_base64(sample_image)
    
    print(f"\n📊 Base64 Data Statistics:")
    print(f"Length: {len(base64_data)} characters")
    print(f"Preview: {base64_data[:50]}...")
    print(f"Ends with: ...{base64_data[-20:]}")
    
    print(f"\n🎯 CORRECT Tool Call:")
    print(f"generate_comic_strip_tool(")
    print(f"    base_image_data='{base64_data}',")
    print(f"    story_guide='A silly comic about dogs',")
    print(f"    character_name='Ramesh'")
    print(f")")
    
    print(f"\n❌ INCORRECT Tool Call (what's happening now):")
    print(f"generate_comic_strip_tool(")
    print(f"    base_image_data='MXAENdal',  # This is invalid!")
    print(f"    story_guide='A silly comic about dogs',")
    print(f"    character_name='Ramesh'")
    print(f")")
    
    print(f"\n🔍 Key Differences:")
    print(f"✅ Valid base64: {len(base64_data)} characters, starts with 'iVBORw0KGgo'")
    print(f"❌ Invalid data: 8 characters, starts with 'MXAENdal'")
    
    print(f"\n💡 The client needs to send the FULL base64-encoded image data,")
    print(f"   not a truncated or placeholder string.")

if __name__ == "__main__":
    main() 