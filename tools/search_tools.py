"""
NASA Search Tools
All tools related to searching NASA's image/video library
"""
import requests
from typing import Optional

def register_search_tools(mcp):
    """Register all search-related tools with the MCP server"""
    
    @mcp.tool()
    def search_nasa_images(
        query: str,
        media_type: str = "image",
        year_start: str = "",
        year_end: str = "",
        page_size: int = 10
    ) -> dict:
        """
        Search NASA's COMPLETE image and video library by ANY keywords.
        
        ⭐ Use this tool when user wants to SEARCH for:
        - Any space topic: Mars, Jupiter, Saturn, nebulae, etc.
        - Specific missions: Voyager, Cassini, New Horizons, etc.
        - Celestial objects: planets, stars, galaxies, asteroids
        - Space phenomena: supernovas, black holes, eclipses
        - Any keyword search request
        
        ⚠️ DO NOT use this tool when:
        - User asks about "famous" or "iconic" images → use get_famous_nasa_images
        - User asks specifically about "Apollo 11 archives" → use get_apollo11_resources
        - User provides a specific NASA ID → use get_image_details
        
        This searches NASA's ENTIRE database (millions of items).
        
        Args:
            query: Search keywords (e.g., "mars rover", "jupiter", "hubble")
            media_type: Type - "image", "video", or "audio"
            year_start: Optional start year (e.g., "2000")
            year_end: Optional end year (e.g., "2024")
            page_size: Number of results (1-100, default 10)
            
        Returns:
            Live search results from NASA's complete database
        """
        url = "https://images-api.nasa.gov/search"
        
        params = {
            "q": query,
            "media_type": media_type,
            "page_size": min(page_size, 100)
        }
        
        if year_start:
            params["year_start"] = year_start
        if year_end:
            params["year_end"] = year_end
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        items = data['collection']['items']
        total_hits = data['collection']['metadata']['total_hits']
        
        results = []
        for item in items:
            item_data = item['data'][0]
            results.append({
                'title': item_data.get('title', 'Untitled'),
                'nasa_id': item_data.get('nasa_id'),
                'description': item_data.get('description', ''),
                'date_created': item_data.get('date_created', ''),
                'media_type': item_data.get('media_type', 'image'),
                'thumbnail_url': item['links'][0]['href'] if 'links' in item else None
            })
        
        return {
            'query': query,
            'total_hits': total_hits,
            'returned_results': len(results),
            'results': results,
            'note': f'Searched NASA\'s complete database. Found {total_hits:,} total items.'
        }
    
    @mcp.tool()
    def search_apollo11_specific(
        query: str = "",
        page_size: int = 10
    ) -> dict:
        """
        Quick search focused on Apollo 11 mission images.
        
        ⭐ Use this tool when user wants:
        - Quick Apollo 11 image search with keywords
        - "Search for Apollo 11 moon landing"
        - "Find Apollo 11 photos of [specific thing]"
        
        For comprehensive Apollo 11 archives, use get_apollo11_resources instead.
        For general space searches, use search_nasa_images.
        
        Args:
            query: Additional keywords (optional, e.g., "lunar module", "armstrong")
            page_size: Number of results (default 10, max 100)
            
        Returns:
            Apollo 11 specific search results (1969-1972)
        """
        search_query = f"apollo 11 {query}".strip()
        
        return search_nasa_images(
            query=search_query,
            media_type="image",
            year_start="1969",
            year_end="1972",
            page_size=page_size
        )