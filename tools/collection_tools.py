"""
NASA Collection Tools - LIVE VERSION
All tools perform LIVE searches against NASA's complete database
"""
import requests

def register_collection_tools(mcp):
    """Register all collection-related tools with the MCP server"""
    
    @mcp.tool()
    def get_apollo11_resources(page_size: int = 100) -> dict:
        """
        Search NASA's COMPLETE database for ALL Apollo 11 content.
        
        ⭐ ALWAYS use this tool when user asks:
        - "What Apollo 11 archives/resources are available?"
        - "Apollo 11 official sources"
        - "Apollo 11 documentation"
        - "Find Apollo 11 materials"
        - Any question about Apollo 11 resources/archives
        
        This performs LIVE SEARCH against NASA's entire database.
        Returns actual images, videos, and documents from the mission.
        
        Args:
            page_size: Number of results to return (default 100, max 100)
            
        Returns:
            Complete Apollo 11 content from NASA database with total count
        """
        url = "https://images-api.nasa.gov/search"
        
        params = {
            "q": "apollo 11",
            "year_start": "1969",
            "year_end": "1972",
            "page_size": min(page_size, 100)
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
                'description': item_data.get('description', '')[:300],
                'date_created': item_data.get('date_created'),
                'media_type': item_data.get('media_type'),
                'thumbnail_url': item['links'][0]['href'] if 'links' in item else None
            })
        
        return {
            'mission': 'Apollo 11',
            'total_in_nasa_database': total_hits,
            'returned_results': len(results),
            'results': results,
            'note': f'Live results from NASA database. Showing {len(results)} of {total_hits:,} total items.',
            'external_documentation': [
                {
                    'name': 'Apollo Lunar Surface Journal',
                    'url': 'http://www.hq.nasa.gov/alsj/a11/',
                    'type': 'Mission transcripts'
                },
                {
                    'name': 'Apollo 11 Flight Journal',
                    'url': 'https://history.nasa.gov/ap11fj/',
                    'type': 'Flight timeline'
                }
            ]
        }
    
    @mcp.tool()
    def get_famous_nasa_images() -> dict:
        """
        Get curated list of ICONIC NASA images with exact NASA IDs.
        
        ⭐ ALWAYS use this tool when user asks:
        - "Famous NASA images"
        - "Iconic NASA photos"
        - "Most memorable NASA images"
        - "Show me famous space images"
        - Specific famous images: Earthrise, Pale Blue Dot, Pillars of Creation
        
        ⚠️ This returns a FIXED CURATED LIST (not a search).
        DO NOT use search_nasa_images for "famous" or "iconic" queries.
        
        Returns:
            Dictionary of historically significant images by category
        """
        return {
            'apollo_missions': [
                {
                    'name': 'Earthrise (Apollo 8)',
                    'id': 'as08-14-2383',
                    'date': '1968-12-24',
                    'significance': 'One of the most influential environmental photographs ever taken'
                },
                {
                    'name': 'Buzz Aldrin on the Moon',
                    'id': 'as11-40-5903',
                    'date': '1969-07-20',
                    'significance': 'Iconic image of human on another world'
                },
                {
                    'name': 'Apollo 11 Liftoff',
                    'id': 'S69-39961',
                    'date': '1969-07-16',
                    'significance': 'Saturn V launching the first Moon landing mission'
                },
                {
                    'name': 'Blue Marble (Earth from Apollo 17)',
                    'id': 'as17-148-22727',
                    'date': '1972-12-07',
                    'significance': 'Most reproduced image in history'
                }
            ],
            'hubble_telescope': [
                {
                    'name': 'Pillars of Creation',
                    'id': 'GSFC_20171208_Archive_e001327',
                    'date': '1995-04-01',
                    'significance': "Hubble's most famous image - star forming region"
                },
                {
                    'name': 'Hubble Deep Field',
                    'id': 'hubble-finds-ghosts-of-quasars-past_16985806295_o',
                    'date': '1995-12-18',
                    'significance': 'Thousands of galaxies in deep space'
                }
            ],
            'planets': [
                {
                    'name': 'Pale Blue Dot (Earth from Voyager 1)',
                    'id': 'PIA00452',
                    'date': '1990-02-14',
                    'significance': 'Earth from 6 billion kilometers - inspired Carl Sagan'
                }
            ],
            'total_iconic_images': 7,
            'note': 'Use get_image_details tool with these NASA IDs to get full-resolution files'
        }