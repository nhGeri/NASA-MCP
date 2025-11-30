"""
NASA Media Tools
Tools for accessing video captions and media-specific features
"""
import requests

def register_media_tools(mcp):
    """Register all media-related tools with the MCP server"""
    
    @mcp.tool()
    def get_captions(nasa_id: str) -> dict:
        """
        Get video caption/subtitle information.
        Returns SRT file URL if available.
        
        ⭐ Use this tool when:
        - User wants subtitles/captions for a NASA video
        - User asks for transcript of a video
        
        NOTE: Only works for videos, not images.
        
        Args:
            nasa_id: The NASA ID of the video
            
        Returns:
            Caption file URL and format information (usually SRT format)
        """
        url = f"https://images-api.nasa.gov/captions/{nasa_id}"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        items = data.get('collection', {}).get('items', [])
        
        if not items:
            return {'error': f'No captions found for video: {nasa_id}', 'note': 'Captions are only available for some videos'}
        
        captions = []
        for item in items:
            href = item.get('href', '')
            captions.append({
                'format': 'SRT' if '.srt' in href else 'Unknown',
                'url': href
            })
        
        return {
            'nasa_id': nasa_id,
            'captions': captions,
            'note': 'Caption URLs work via API/Python but may be blocked in browsers'
        }