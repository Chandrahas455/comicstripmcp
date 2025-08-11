import asyncio
from typing import Annotated
import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth.providers.bearer import BearerAuthProvider, RSAKeyPair
from mcp import ErrorData, McpError
from mcp.server.auth.provider import AccessToken
from mcp.types import TextContent, ImageContent, INVALID_PARAMS, INTERNAL_ERROR
from pydantic import BaseModel, Field, AnyUrl

import markdownify
import httpx
import readabilipy
import base64
import io
import time
from PIL import Image

# --- Load environment variables ---
load_dotenv()

TOKEN = os.environ.get("AUTH_TOKEN")
MY_NUMBER = os.environ.get("MY_NUMBER")

assert TOKEN is not None, "Please set AUTH_TOKEN in your .env file"
assert MY_NUMBER is not None, "Please set MY_NUMBER in your .env file"

# --- Auth Provider ---
class SimpleBearerAuthProvider(BearerAuthProvider):
    def __init__(self, token: str):
        k = RSAKeyPair.generate()
        super().__init__(public_key=k.public_key, jwks_uri=None, issuer=None, audience=None)
        self.token = token

    async def load_access_token(self, token: str) -> AccessToken | None:
        if token == self.token:
            return AccessToken(
                token=token,
                client_id="puch-client",
                scopes=["*"],
                expires_at=None,
            )
        return None

# --- Rich Tool Description model ---
class RichToolDescription(BaseModel):
    description: str
    use_when: str
    side_effects: str | None = None

# --- Fetch Utility Class ---
class Fetch:
    USER_AGENT = "Puch/1.0 (Autonomous)"

    @classmethod
    async def fetch_url(
        cls,
        url: str,
        user_agent: str,
        force_raw: bool = False,
    ) -> tuple[str, str]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url,
                    follow_redirects=True,
                    headers={"User-Agent": user_agent},
                    timeout=30,
                )
            except httpx.HTTPError as e:
                raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"Failed to fetch {url}: {e!r}"))

            if response.status_code >= 400:
                raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"Failed to fetch {url} - status code {response.status_code}"))

            page_raw = response.text

        content_type = response.headers.get("content-type", "")
        is_page_html = "text/html" in content_type

        if is_page_html and not force_raw:
            return cls.extract_content_from_html(page_raw), ""

        return (
            page_raw,
            f"Content type {content_type} cannot be simplified to markdown, but here is the raw content:\n",
        )

    @staticmethod
    def extract_content_from_html(html: str) -> str:
        """Extract and convert HTML content to Markdown format."""
        ret = readabilipy.simple_json.simple_json_from_html_string(html, use_readability=True)
        if not ret or not ret.get("content"):
            return "<error>Page failed to be simplified from HTML</error>"
        content = markdownify.markdownify(ret["content"], heading_style=markdownify.ATX)
        return content

    @staticmethod
    async def google_search_links(query: str, num_results: int = 5) -> list[str]:
        """
        Perform a scoped DuckDuckGo search and return a list of job posting URLs.
        (Using DuckDuckGo because Google blocks most programmatic scraping.)
        """
        ddg_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
        links = []

        async with httpx.AsyncClient() as client:
            resp = await client.get(ddg_url, headers={"User-Agent": Fetch.USER_AGENT})
            if resp.status_code != 200:
                return ["<error>Failed to perform search.</error>"]

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.find_all("a", class_="result__a", href=True):
            href = a["href"]
            if "http" in href:
                links.append(href)
            if len(links) >= num_results:
                break

        return links or ["<error>No results found.</error>"]

# --- MCP Server Setup ---
mcp = FastMCP(
    "Job Finder & Comic Generator MCP Server",
    auth=SimpleBearerAuthProvider(TOKEN),
)

# --- Tool: validate (required by Puch) ---
@mcp.tool
async def validate() -> str:
    return MY_NUMBER


# Comic Generation Tool
COMIC_GENERATION_DESCRIPTION = RichToolDescription(
    description="Generate a 3-panel comic strip from a base image and story guide using AI.",
    use_when="Use this tool when the user wants to create a comic strip from a image url with a specific story theme.",
    side_effects="Generates 3 comic panels and combines them into a final comic strip with text overlay.",
)

@mcp.tool(description=COMIC_GENERATION_DESCRIPTION.model_dump_json())
async def generate_comic_strip_tool(
    puch_image_data: Annotated[str, Field(description="Base64-encoded image ")],
    story_guide: Annotated[str, Field(description="Very descriptive Story theme or guide for the comic")] = "Jokes about hackathon",
    character_name: Annotated[str, Field(description="Name of the character in the comic")] = "Your Name",
    reference_style_data: Annotated[str | None, Field(description="Base64-encoded reference style image (optional)")] = None,
) -> list[TextContent | ImageContent]:
    """
    Generate a complete 3-panel comic strip from a base image with AI-generated panels and story.
    """
    import base64
    import io
    import tempfile
    import shutil
    from PIL import Image

    try:
        # Decode base image (following the same pattern as make_img_black_and_white)
        base_image_bytes = base64.b64decode(puch_image_data)
        base_image = Image.open(io.BytesIO(base_image_bytes))
        
        # Decode reference style image if provided
        reference_style_image = None
        if reference_style_data:
            ref_image_bytes = base64.b64decode(reference_style_data)
            reference_style_image = Image.open(io.BytesIO(ref_image_bytes))
        
        # Import comic generation modules
        from text_generation import generate_comic_story
        from image_generation import generate_comic_panels
        from layout_generation import generate_comic_strip
        from texture import apply_texture_overlay
        
        # Create temporary directory for processing
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Save base image to temp directory
            base_image_path = os.path.join(temp_dir, "base_image.jpg")
            base_image.save(base_image_path)
            
            # Handle reference style image
            if reference_style_image:
                reference_style_path = os.path.join(temp_dir, "reference_style.jpg")
                reference_style_image.save(reference_style_path)
            else:
                # Use default reference style if available
                default_ref_path = os.path.join(os.path.dirname(__file__), "Test_Images", "StyleReference.jpg")
                if os.path.exists(default_ref_path):
                    reference_style_path = default_ref_path
                else:
                    reference_style_path = base_image_path  # Use base image as reference
            
            # Generate comic panels
            panels_dir = os.path.join(temp_dir, "panels")
            generate_comic_panels(
                story_guide=story_guide,
                base_image_path=base_image_path,
                reference_style_path=reference_style_path,
                output_dir=panels_dir
            )
            
            # Get generated panel paths
            comic_images = [
                os.path.join(panels_dir, "comic_panel_1.png"),
                os.path.join(panels_dir, "comic_panel_2.png"),
                os.path.join(panels_dir, "comic_panel_3.png")
            ]
            
            # Generate story
            story = generate_comic_story(comic_images, character_name)
            
            # Load panel images for layout
            panel_images = [
                Image.open(comic_images[0]),
                Image.open(comic_images[1]),
                Image.open(comic_images[2])
            ]
            
            # Generate comic strip layout
            comic_strip_path = os.path.join(temp_dir, "comic_strip.png")
            generate_comic_strip(panel_images, story, output_path=comic_strip_path)
            
            # Apply texture overlay
            final_comic_path = os.path.join(temp_dir, "final_comic.png")
            apply_texture_overlay(comic_strip_path, output_path=final_comic_path)
            
            # Read final comic and convert to base64 (following the same pattern as make_img_black_and_white)
            with open(final_comic_path, "rb") as f:
                final_comic_bytes = f.read()
            
            final_comic_base64 = base64.b64encode(final_comic_bytes).decode("utf-8")
            
            # Create response with story and image
            story_text = f"**{story['title']}**\n\n1. {story['text1']}\n2. {story['text2']}\n3. {story['text3']}"
            
            return [
                TextContent(type="text", text=story_text),
                ImageContent(type="image", mimeType="image/png", data=final_comic_base64)
            ]
            
        finally:
            # Clean up temporary directory
            shutil.rmtree(temp_dir, ignore_errors=True)
            
    except Exception as e:
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=str(e)))

# --- Run MCP Server ---
async def main():
    port = int(os.environ.get("PORT", 8086))  # Railway sets PORT
    print(f"🚀 Starting MCP server on http://0.0.0.0:{port}")
    await mcp.run_async("streamable-http", host="0.0.0.0", port=port)


if __name__ == "__main__":
    asyncio.run(main())
