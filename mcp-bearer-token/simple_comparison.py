#!/usr/bin/env python3
"""
Simple comparison of the exact code patterns in both tools.
"""

import base64
import io
from PIL import Image

def simulate_black_white_tool(data):
    """Simulate the exact code from the black and white tool."""
    print(f"🧪 Simulating black and white tool with: '{data}'")
    
    try:
        image_bytes = base64.b64decode(data)
        image = Image.open(io.BytesIO(image_bytes))

        bw_image = image.convert("L")

        buf = io.BytesIO()
        bw_image.save(buf, format="PNG")
        bw_bytes = buf.getvalue()
        bw_base64 = base64.b64encode(bw_bytes).decode("utf-8")

        print(f"✅ Black and white tool would return: {len(bw_base64)} characters")
        return True
    except Exception as e:
        print(f"❌ Black and white tool would fail: {e}")
        return False

def simulate_comic_tool(data):
    """Simulate the exact code from the comic tool."""
    print(f"🧪 Simulating comic tool with: '{data}'")
    
    try:
        # Decode base image (following the same pattern as make_img_black_and_white)
        try:
            base_image_bytes = base64.b64decode(data)
        except Exception as e:
            print(f"❌ Comic tool base64 error: {e}")
            return False
        
        try:
            base_image = Image.open(io.BytesIO(base_image_bytes))
        except Exception as e:
            print(f"❌ Comic tool image error: {e}")
            return False
        
        print(f"✅ Comic tool would proceed with image: {base_image.size} {base_image.mode}")
        return True
    except Exception as e:
        print(f"❌ Comic tool would fail: {e}")
        return False

def main():
    print("=== Tool Code Pattern Comparison ===\n")
    
    # Test with the data that supposedly works for black and white
    test_data = "Base64 Image"
    
    print(f"Testing with: '{test_data}'")
    print(f"Length: {len(test_data)}")
    
    # Test both tool patterns
    bw_works = simulate_black_white_tool(test_data)
    print()
    comic_works = simulate_comic_tool(test_data)
    
    print(f"\n=== Results ===")
    print(f"Black and white pattern works: {bw_works}")
    print(f"Comic pattern works: {comic_works}")
    
    if bw_works and not comic_works:
        print(f"\n🎯 The difference is in the error handling!")
        print(f"Black and white tool: Single try-catch, returns INTERNAL_ERROR")
        print(f"Comic tool: Specific try-catch, returns INVALID_PARAMS")
    
    elif not bw_works and not comic_works:
        print(f"\n🤔 Both tools would fail with this data.")
        print(f"This suggests the client might be sending different data to different tools.")

if __name__ == "__main__":
    main() 