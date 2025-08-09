# Comic Generation MCP Tool

This MCP server now includes a powerful comic generation tool that can create 3-panel comic strips from any base image using AI.

## Features

- **AI-Powered Panel Generation**: Uses Google Gemini to generate 3 comic panels from a base image
- **Story Generation**: Automatically creates funny, coherent stories for the comic panels
- **Customizable Themes**: Specify story themes like "GitHub jokes", "Office humor", etc.
- **Style Reference**: Optionally provide a reference image for consistent comic style
- **Texture Overlay**: Applies paper texture to the final comic for authentic look
- **Character Naming**: Customize the character name in the generated story

## How to Use

### 1. Start the MCP Server

```bash
cd hack/mcp-starter/mcp-bearer-token
python mcp_starter.py
```

The server will start on `http://0.0.0.0:8086`

### 2. Environment Variables

Make sure you have these environment variables set:

```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
export AUTH_TOKEN="your_auth_token_here"
export MY_NUMBER="your_phone_number_here"
```

### 3. Using the Comic Tool

The comic generation tool accepts the following parameters:

- **`base_image_data`** (required): Base64-encoded image data to use as the base for comic generation
- **`story_guide`** (optional): Story theme or guide for the comic (e.g., "Make jokes about GitHub", "Office humor")
- **`character_name`** (optional): Name of the character in the comic (default: "Your Name")
- **`reference_style_data`** (optional): Base64-encoded reference style image for consistent comic style

### 4. Example Usage

```python
# Example MCP client call
result = await client.call_tool(
    "generate_comic_strip_tool",
    {
        "base_image_data": "base64_encoded_image_data",
        "story_guide": "Make jokes about programming",
        "character_name": "CodeMaster"
    }
)
```

### 5. Response Format

The tool returns a list containing:
1. **Text Content**: The generated story with title and panel descriptions
2. **Image Content**: The final comic strip as a base64-encoded PNG image

## Testing

Run the test script to verify the tool works:

```bash
cd hack/mcp-starter/mcp-bearer-token
python test_comic_tool.py
```

## Dependencies

The comic generation tool requires:
- `google-genai`: For AI-powered image and text generation
- `pillow`: For image processing
- `fastmcp`: For MCP server functionality
- `python-dotenv`: For environment variable management

## How It Works

1. **Image Processing**: Takes a base image and optionally a reference style image
2. **Panel Generation**: Uses Gemini AI to generate 3 comic panels with consistent style
3. **Story Creation**: Analyzes the generated panels and creates a coherent, funny story
4. **Layout Assembly**: Combines panels with text into a comic strip layout
5. **Texture Application**: Applies paper texture overlay for authentic comic look
6. **Output**: Returns both the story text and the final comic image

## File Structure

```
mcp-bearer-token/
├── mcp_starter.py          # Main MCP server with comic tool
├── text_generation.py      # Story generation module
├── image_generation.py     # Panel generation module
├── layout_generation.py    # Comic strip layout module
├── texture.py             # Texture overlay module
├── test_comic_tool.py     # Test script
├── Fonts/                 # Font files for text overlay
├── Textures/              # Texture files
└── Test_Images/           # Sample images for testing
```

## Troubleshooting

- **Missing API Key**: Ensure `GEMINI_API_KEY` is set in your environment
- **Missing Fonts**: The tool will fall back to default fonts if custom fonts are missing
- **Image Processing Errors**: Check that input images are valid and not corrupted
- **Memory Issues**: Large images may cause memory issues; consider resizing before processing
- **Invalid Base64 Data**: If you get "cannot identify image file" errors, the base64 data is invalid. Use the test scripts to generate valid data.

## Testing with Valid Data

To test the tool with valid base64 data:

```bash
# Generate a test image and valid base64 data
python generate_test_image.py

# Debug base64 issues
python debug_base64.py

# Test the comic tool directly
python test_comic_tool.py
```

The `generate_test_image.py` script will create a valid test image and provide the base64 data you can use for testing.

## Customization

You can customize the comic generation by:
- Modifying prompts in `text_generation.py` and `image_generation.py`
- Adding new fonts to the `Fonts/` directory
- Adding new textures to the `Textures/` directory
- Adjusting layout parameters in `layout_generation.py` 