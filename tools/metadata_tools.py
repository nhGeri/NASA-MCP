"""
NASA Metadata Tools
Tools for retrieving metadata and asset information
"""
import requests

def register_metadata_tools(mcp):
    """Register all metadata-related tools with the MCP server"""
    
    @mcp.tool()
    def get_image_details(nasa_id: str) -> dict:
        """
        Get detailed file information for a specific NASA media asset.
        Returns all available file versions (original, large, medium, small, thumbnail).
        
        ⭐ Use this tool when:
        - User asks "Get details for image [NASA_ID]"
        - User wants to download/access specific image files
        - User has a NASA ID and wants all available versions
        
        Args:
            nasa_id: The NASA ID of the media (e.g., "as11-40-5903")
            
        Returns:
            Dictionary with all available file URLs and types
        """
        url = f"https://images-api.nasa.gov/asset/{nasa_id}"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        items = data.get('collection', {}).get('items', [])
        
        if not items:
            return {'error': f'No files found for NASA ID: {nasa_id}'}
        
        files = []
        for item in items:
            href = item.get('href', '')
            filename = href.split('/')[-1]
            
            # Determine file type
            if '~orig' in href:
                file_type = 'Original'
            elif '~large' in href:
                file_type = 'Large'
            elif '~medium' in href:
                file_type = 'Medium'
            elif '~small' in href:
                file_type = 'Small'
            elif '~thumb' in href:
                file_type = 'Thumbnail'
            elif '.json' in href:
                file_type = 'Metadata'
            else:
                file_type = 'Other'
            
            files.append({
                'type': file_type,
                'filename': filename,
                'url': href
            })
        
        return {
            'nasa_id': nasa_id,
            'total_files': len(files),
            'files': files,
            'note': 'Use these URLs to download or display the image'
        }
    
    @mcp.tool()
    def get_metadata(nasa_id: str) -> dict:
        """
        Get technical metadata for a NASA media asset.
        
        ⭐ Use this tool when:
        - User wants technical/EXIF data for an image
        - User asks about camera settings, location, technical details
        
        Args:
            nasa_id: The NASA ID of the media
            
        Returns:
            Metadata information including EXIF data, camera info, GPS coordinates, etc.
        """
        url = f"https://images-api.nasa.gov/metadata/{nasa_id}"
        
        response = requests.get(url)
        response.raise_for_status()
        
        return response.json()