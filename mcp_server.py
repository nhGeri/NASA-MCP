"""
NASA Image Library MCP Server - Main Entry Point
This server connects NASA's public image and video library to AI applications
through the Model Context Protocol (MCP).

ALL SEARCHES ARE LIVE - Direct API calls to NASA's complete database.
"""
import sys
from fastmcp import FastMCP

# Import all tool registration functions
from tools.search_tools import register_search_tools
from tools.metadata_tools import register_metadata_tools
from tools.media_tools import register_media_tools
from tools.collection_tools import register_collection_tools

def main():
    """Initialize and start the MCP server."""
    
    # Create the FastMCP server instance
    mcp = FastMCP(
        name="NASA-Image-Library",
        instructions="""
You have access to tools for exploring NASA's COMPLETE public image and video library.

🔴 IMPORTANT: ALL searches are LIVE - they query NASA's entire database in real-time.

Available tool categories:

1. Search Tools - Find ANY space content (LIVE API searches)
   - search_nasa_images: Search for ANYTHING (Mars, Jupiter, Hubble, etc.)
     * Use for: Mars, planets, missions, celestial objects, phenomena
     * Searches NASA's ENTIRE database (millions of items)
   
   - search_apollo11_specific: Quick Apollo 11 image search
     * Use for: Quick Apollo 11 photo searches with keywords

2. Collection Tools - Comprehensive mission resources
   - get_apollo11_resources: ALL Apollo 11 content from NASA database
     * Use when: User asks "What Apollo 11 archives/resources exist?"
     * Returns: LIVE search of complete Apollo 11 database (1,500+ items)
   
   - get_famous_nasa_images: Curated iconic images (fixed list)
     * Use when: User asks about "famous" or "iconic" NASA images
     * Returns: 7 historically significant images with NASA IDs

3. Metadata Tools - Get detailed information
   - get_image_details: All available file versions and URLs
   - get_metadata: Technical metadata (EXIF, camera info)

4. Media Tools - Access video features
   - get_captions: Download video subtitles (SRT format)

Data source: https://images.nasa.gov
API endpoint: https://images-api.nasa.gov

🎯 Tool Selection Guide:
- "Search for [anything]" → search_nasa_images
- "Apollo 11 archives?" → get_apollo11_resources
- "Famous NASA images?" → get_famous_nasa_images
- "Get details for [nasa_id]" → get_image_details

All searches return LIVE results from NASA's complete database!
        """
    )
    
    # Register all tool modules
    print("Registering NASA MCP tools...", file=sys.stderr)
    print("  - Search tools (LIVE NASA API)", file=sys.stderr)
    register_search_tools(mcp)
    
    print("  - Metadata tools (LIVE NASA API)", file=sys.stderr)
    register_metadata_tools(mcp)
    
    print("  - Media tools (LIVE NASA API)", file=sys.stderr)
    register_media_tools(mcp)
    
    print("  - Collection tools (LIVE NASA API)", file=sys.stderr)
    register_collection_tools(mcp)
    
    # Start the server
    print("\n[OK] All tools registered successfully!", file=sys.stderr)
    print("All searches are LIVE - querying NASA's complete database", file=sys.stderr)
    print("Starting NASA MCP Server...", file=sys.stderr)
    print("Listening for connections on stdio transport...", file=sys.stderr)
    
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.", file=sys.stderr)
    except Exception as e:
        print(f"\n\nError running server: {e}", file=sys.stderr)
        raise

if __name__ == "__main__":
    main()