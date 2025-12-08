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
        Downloads and returns the actual SRT content since direct browser access is blocked.
        """
        url = f"https://images-api.nasa.gov/captions/{nasa_id}"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Get the SRT file location
        srt_url = data.get('location')
        
        if not srt_url:
            return {'error': f'No captions found for video: {nasa_id}'}
        
        # Download the actual SRT content (browser can't access directly)
        try:
            srt_response = requests.get(srt_url, timeout=15)
            srt_response.raise_for_status()
            srt_content = srt_response.text
            
            return {
                'nasa_id': nasa_id,
                'format': 'SRT',
                'srt_url': srt_url,
                'content_preview': srt_content[:1000],  # First 1000 chars
                'full_content': srt_content,
                'note': 'SRT content downloaded via API (direct browser access is blocked by NASA)'
            }
        except Exception as e:
            return {
                'nasa_id': nasa_id,
                'srt_url': srt_url,
                'error': f'Could not download SRT: {str(e)}',
                'note': 'URL is valid but download failed'
            }
    @mcp.tool()
    def get_video_details(nasa_id: str) -> dict:
        """
        Get video file information and metadata (NOT for images!).
        
        ⭐ Use ONLY for videos (media_type="video")
        For images, use get_image_details instead.
        
        ⭐ Use this tool when:
        - User asks for video details
        - User wants video file information
        - User says "show me video [NASA_ID]"
        - NASA ID is from a VIDEO search result
        
        ❌ DO NOT use for images - use get_image_details
        
        Note: Videos do NOT have /asset endpoint like images.
        This tool returns metadata which contains video information.
        
        Args:
            nasa_id: NASA ID of the VIDEO (e.g., "NHQ_2021_0222_VF_...")
            
        Returns:
            Video metadata and information
        """
        # Try metadata endpoint (videos don't have /asset endpoint)
        metadata_url = f"https://images-api.nasa.gov/metadata/{nasa_id}"
        
        try:
            response = requests.get(metadata_url, timeout=10)
            response.raise_for_status()
            
            metadata = response.json()
            
            return {
                'nasa_id': nasa_id,
                'media_type': 'video',
                'metadata_url': metadata_url,
                'metadata': metadata,
                'note': 'Videos do not have multiple file versions like images. Check NASA website for video player or download options.',
                'nasa_website': f'https://images.nasa.gov/details/{nasa_id}'
            }
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return {
                    'error': f'Video not found: {nasa_id}',
                    'note': 'This NASA ID does not exist or is not a video. Try searching for videos first.',
                    'status_code': 404
                }
            else:
                return {
                    'error': f'HTTP Error: {e}',
                    'status_code': e.response.status_code
                }
        except Exception as e:
            return {
                'error': f'Error retrieving video details: {str(e)}',
                'note': 'Check if the NASA ID is correct and is a video'
            }