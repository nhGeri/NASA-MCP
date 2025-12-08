"""
NASA Collection Tools - FIXED VERSION
Anti-loop protection added
"""
import requests

def register_collection_tools(mcp):
    """Register all collection-related tools with the MCP server"""
    
    @mcp.tool()
    def get_apollo11_resources(page_size: int = 10) -> dict:
        """
        Get Apollo 11 content from NASA database.
        
        ⚠️ STOP: Call this tool ONLY ONCE. After receiving results, 
        show them to the user. Do NOT call again.
        
        Args:
            page_size: Number of results (default 10, max 50)
            
        Returns:
            Apollo 11 images and videos - USE THESE RESULTS IMMEDIATELY
        """
        url = "https://images-api.nasa.gov/search"
        
        # Limit max to 50 to prevent overwhelming the model
        actual_size = min(page_size, 50)
        
        params = {
            "q": "apollo 11",
            "year_start": "1969",
            "year_end": "1972",
            "page_size": actual_size
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        items = data['collection']['items']
        total_hits = data['collection']['metadata']['total_hits']
        
        results = []
        for item in items:
            item_data = item['data'][0]
            results.append({
                'title': item_data.get('title'),
                'nasa_id': item_data.get('nasa_id'),
                'date_created': item_data.get('date_created'),
                'media_type': item_data.get('media_type')
            })
        
        return {
            'status': 'SUCCESS - Display these results now, do not call again',
            'total_in_database': total_hits,
            'returned': len(results),
            'results': results
        }
    
    @mcp.tool()
    def get_famous_nasa_images() -> dict:
        """
        Get list of iconic NASA images.
        
        ⚠️ STOP: Call ONLY ONCE. Show results immediately. Do NOT repeat.
        
        Returns:
            Famous NASA images with IDs - USE IMMEDIATELY
        """
        return {
            'status': 'SUCCESS - Display now, do not call again',
            'images': [
                {'name': 'Earthrise', 'id': 'as08-14-2383', 'year': 1968},
                {'name': 'Buzz Aldrin on Moon', 'id': 'as11-40-5903', 'year': 1969},
                {'name': 'Blue Marble', 'id': 'as17-148-22727', 'year': 1972},
                {'name': 'Pillars of Creation', 'id': 'GSFC_20171208_Archive_e001327', 'year': 1995},
                {'name': 'Pale Blue Dot', 'id': 'PIA00452', 'year': 1990}
            ],
            'note': 'Use get_image_details with any ID for full resolution'
        }