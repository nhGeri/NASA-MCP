"""
NASA API MCP Server
Fast MCP implementation for LM Studio
"""

from fastmcp import FastMCP
import requests
from typing import Optional

# MCP server inicializálása
mcp = FastMCP("NASA Image Library API")


@mcp.tool()
def search_nasa_images(
    query: str,
    media_type: Optional[str] = "image",
    year_start: Optional[int] = None,
    year_end: Optional[int] = None,
    page_size: int = 5
) -> dict:
    """
    Keresés a NASA Image and Video Library-ban.
    
    Args:
        query: Keresési kifejezés (pl. "apollo 11", "mars", "hubble")
        media_type: Média típus - "image", "video", vagy "audio" (alapértelmezett: "image")
        year_start: Kezdő év szűréshez (opcionális)
        year_end: Befejező év szűréshez (opcionális)
        page_size: Hány találatot mutasson (1-100, alapértelmezett: 5)
    
    Returns:
        Dictionary a találatokkal, beleértve címeket, NASA ID-ket, leírásokat és dátumokat
    
    Examples:
        - search_nasa_images("apollo 11")
        - search_nasa_images("mars rover", year_start=2020)
        - search_nasa_images("moon landing", media_type="video")
    """
    try:
        params = {
            "q": query,
            "media_type": media_type,
            "page_size": min(page_size, 100)
        }
        
        if year_start:
            params["year_start"] = year_start
        if year_end:
            params["year_end"] = year_end
        
        response = requests.get(
            "https://images-api.nasa.gov/search",
            params=params,
            timeout=15
        )
        response.raise_for_status()
        
        data = response.json()
        items = data['collection']['items']
        total_hits = data['collection']['metadata']['total_hits']
        
        # Eredmények formázása
        results = []
        for item in items:
            item_data = item['data'][0]
            results.append({
                "nasa_id": item_data['nasa_id'],
                "title": item_data['title'],
                "description": item_data.get('description', 'Nincs leírás'),
                "date_created": item_data.get('date_created', 'N/A'),
                "media_type": item_data['media_type'],
                "keywords": item_data.get('keywords', []),
                "thumbnail_url": item['links'][0]['href'] if 'links' in item else None
            })
        
        return {
            "total_hits": total_hits,
            "returned_results": len(results),
            "results": results
        }
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_image_details(nasa_id: str) -> dict:
    """
    Egy kép/videó részletes információinak lekérése NASA ID alapján.
    Tartalmazza az összes elérhető fájl URL-jét (különböző méretekben).
    
    Args:
        nasa_id: NASA azonosító (pl. "as11-40-5903")
    
    Returns:
        Dictionary az elérhető fájlokkal és URL-ekkel
    
    Examples:
        - get_image_details("as11-40-5903")
        - get_image_details("jsc2007e034221")
    """
    try:
        # Asset manifest
        asset_response = requests.get(
            f"https://images-api.nasa.gov/asset/{nasa_id}",
            timeout=10
        )
        asset_response.raise_for_status()
        asset_data = asset_response.json()
        
        files = []
        for item in asset_data['collection']['items']:
            url = item['href']
            filename = url.split('/')[-1]
            
            # Típus meghatározása
            if 'orig' in filename:
                file_type = "original"
            elif 'large' in filename:
                file_type = "large"
            elif 'medium' in filename:
                file_type = "medium"
            elif 'small' in filename:
                file_type = "small"
            elif 'thumb' in filename:
                file_type = "thumbnail"
            elif filename.endswith('.srt'):
                file_type = "captions"
            elif filename == 'metadata.json':
                file_type = "metadata"
            else:
                file_type = "other"
            
            files.append({
                "type": file_type,
                "filename": filename,
                "url": url
            })
        
        return {
            "nasa_id": nasa_id,
            "total_files": len(files),
            "files": files
        }
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_metadata(nasa_id: str) -> dict:
    """
    Egy kép/videó részletes metaadatainak lekérése.
    
    Args:
        nasa_id: NASA azonosító
    
    Returns:
        Dictionary a metadata URL-lel
    
    Examples:
        - get_metadata("as11-40-5903")
    """
    try:
        response = requests.get(
            f"https://images-api.nasa.gov/metadata/{nasa_id}",
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        metadata_url = data.get('location')
        
        if metadata_url:
            # Metadata tartalom lekérése
            metadata_response = requests.get(metadata_url, timeout=10)
            metadata_content = metadata_response.json()
            
            return {
                "nasa_id": nasa_id,
                "metadata_url": metadata_url,
                "metadata": metadata_content
            }
        else:
            return {"error": "Nincs elérhető metadata"}
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_popular_collections() -> dict:
    """
    Népszerű NASA gyűjtemények és témák listája.
    Hasznos kiindulópont a kereséshez.
    
    Returns:
        Dictionary népszerű témákkal és javasolt keresési kifejezésekkel
    """
    return {
        "popular_topics": [
            {
                "category": "Apollo Program",
                "keywords": ["apollo 11", "apollo 13", "moon landing", "lunar module"],
                "description": "Az Apollo program holdutazásai (1960-70-es évek)"
            },
            {
                "category": "Mars Exploration",
                "keywords": ["mars rover", "curiosity", "perseverance", "mars surface"],
                "description": "Mars bolygó felfedezése és roverek"
            },
            {
                "category": "Hubble Space Telescope",
                "keywords": ["hubble", "nebula", "galaxy", "deep space"],
                "description": "Hubble űrtávcső lenyűgöző felvételei"
            },
            {
                "category": "International Space Station",
                "keywords": ["ISS", "space station", "astronaut", "spacewalk"],
                "description": "Nemzetközi Űrállomás és űrsétálók"
            },
            {
                "category": "Earth from Space",
                "keywords": ["earth", "planet earth", "blue marble", "earth observation"],
                "description": "Földünk az űrből nézve"
            },
            {
                "category": "Space Shuttle",
                "keywords": ["space shuttle", "shuttle launch", "atlantis", "discovery"],
                "description": "Space Shuttle program (1981-2011)"
            }
        ],
        "usage_tip": "Használd a 'keywords' listát a search_nasa_images() függvényben!"
    }

@mcp.tool()
def get_apollo11_resources() -> dict:
    """
    Apollo 11 specializált források és képek listája.
    Hivatalos NASA gyűjtemények és archívumok az Apollo 11 küldetésről (1969. július).
    
    Returns:
        Dictionary a legjobb Apollo 11 forrásokkal, keresési tippekkel és letöltési linkekkel
    
    Examples:
        - get_apollo11_resources()
    """
    return {
        "mission_info": {
            "name": "Apollo 11",
            "date": "July 16-24, 1969",
            "crew": ["Neil Armstrong", "Buzz Aldrin", "Michael Collins"],
            "landing_site": "Mare Tranquillitatis (0°N, 23.5°E)",
            "first_steps": "July 20, 1969, 20:17 UTC"
        },
        "official_archives": [
            {
                "name": "NASA Photojournal",
                "url": "https://photojournal.jpl.nasa.gov",
                "description": "Official NASA archive of spaceflight imagery",
                "search_tips": "Search 'Apollo 11' → filter by 'Mission: Apollo 11'",
                "image_quality": "Up to 4K resolution JPEGs",
                "download": "Available - use 'Download' button for original resolution"
            },
            {
                "name": "Apollo Lunar Surface Journal (ALSJ)",
                "url": "http://www.hq.nasa.gov/alsj/a11/",
                "description": "Narrative log + photo thumbnails for each EVA",
                "search_tips": "Navigate to 'EVA 1 & 2' sections",
                "special_features": "Mission timestamps, captions, context for each photo"
            },
            {
                "name": "Digital Apollo Archive",
                "url": "https://apollo.jpl.nasa.gov/",
                "description": "Curated set of 1,200+ images with metadata",
                "search_tips": "Browse by mission or use search bar",
                "special_features": "High-quality metadata and detailed captions"
            },
            {
                "name": "Google Arts & Culture - Apollo 11",
                "url": "https://artsandculture.google.com/partner/nasa-apollo-11",
                "description": "Interactive gallery with zoomable images",
                "special_features": "Contextual audio, interactive exploration"
            },
            {
                "name": "LROC Web Map Client",
                "url": "https://lroc.sese.asu.edu/webmap",
                "description": "High-resolution maps of Moon, including landing site",
                "search_tips": "Search 'Apollo 11 landing site' or coordinates 0°N, 23.5°E",
                "special_features": "Toggle layers: LOLA Terrain + LROC Narrow Angle"
            }
        ],
        "curated_collections": [
            {
                "name": "Apollo 11 - Lunar Surface",
                "url": "https://apollo.jpl.nasa.gov/mission/apollo-11/lunar-surface",
                "images": "300+ images from EVA 1 & 2 with captions"
            },
            {
                "name": "Moon Landing Photos",
                "url": "https://www.nasa.gov/image-feature/moon-landing-photos",
                "images": "Classic images including the famous Earthrise"
            },
            {
                "name": "Apollo 11 - The First Steps",
                "url": "https://artsandculture.google.com/partner/nasa-apollo-11",
                "images": "Focus on first steps and footprints"
            }
        ],
        "download_tips": [
            "High-res: NASA Photojournal offers JPEGs up to ~4K resolution",
            "For raw data: Look for 'RAW' or 'TIFF' links",
            "Batch download: Use browser extensions like DownThemAll! or Bulk Image Downloader",
            "Metadata: JSON/XML files contain mission time, camera type, and more"
        ],
        "famous_images": [
            {
                "name": "Buzz Aldrin on the Moon",
                "nasa_id": "as11-40-5903",
                "description": "Iconic photo of Buzz Aldrin with Neil Armstrong reflected in visor"
            },
            {
                "name": "First Footprint",
                "nasa_id": "as11-40-5877",
                "description": "The first human footprint on lunar surface"
            },
            {
                "name": "Eagle Lunar Module",
                "nasa_id": "as11-44-6642",
                "description": "The Eagle on the Moon's surface"
            },
            {
                "name": "Earthrise from Moon",
                "nasa_id": "as11-44-6550",
                "description": "Earth rising above lunar horizon"
            }
        ],
        "quick_search_guide": {
            "photojournal": {
                "step1": "Go to https://photojournal.jpl.nasa.gov",
                "step2": "Type 'Apollo 11' in search bar",
                "step3": "Use filters: Mission: Apollo 11, Content Type: Image",
                "step4": "Click thumbnail → Download button for full resolution"
            },
            "lroc_map": {
                "step1": "Visit https://lroc.sese.asu.edu/webmap",
                "step2": "Search 'Apollo 11 landing site'",
                "step3": "Map jumps to 0°N, 23.5°E",
                "step4": "Toggle layers for high-res images"
            },
            "alsj": {
                "step1": "Go to http://www.hq.nasa.gov/alsj/a11/",
                "step2": "Select EVA 1 or EVA 2",
                "step3": "Browse photo gallery with captions and timestamps"
            }
        }
    }


@mcp.tool()
def search_apollo11_specific(
    category: str = "all"
) -> dict:
    """
    Apollo 11 specifikus keresés a NASA API-ban.
    Előre definiált kategóriák alapján keres Apollo 11 tartalmakat.
    
    Args:
        category: Kategória - "all", "lunar_surface", "crew", "launch", "landing", "eva", "earthrise"
    
    Returns:
        Dictionary az Apollo 11 képekkel a választott kategóriából
    
    Examples:
        - search_apollo11_specific("lunar_surface")
        - search_apollo11_specific("crew")
        - search_apollo11_specific("earthrise")
    """
    try:
        # Kategória specifikus keresési kifejezések
        search_queries = {
            "all": "apollo 11",
            "lunar_surface": "apollo 11 lunar surface moon",
            "crew": "apollo 11 armstrong aldrin collins crew",
            "launch": "apollo 11 launch saturn v",
            "landing": "apollo 11 landing eagle lunar module",
            "eva": "apollo 11 eva spacewalk moonwalk",
            "earthrise": "apollo 11 earth earthrise blue marble"
        }
        
        query = search_queries.get(category, "apollo 11")
        
        # NASA API hívás
        response = requests.get(
            "https://images-api.nasa.gov/search",
            params={
                "q": query,
                "media_type": "image",
                "year_start": 1969,
                "year_end": 1969,
                "page_size": 10
            },
            timeout=15
        )
        response.raise_for_status()
        
        data = response.json()
        items = data['collection']['items']
        total = data['collection']['metadata']['total_hits']
        
        results = []
        for item in items:
            item_data = item['data'][0]
            results.append({
                "nasa_id": item_data['nasa_id'],
                "title": item_data['title'],
                "description": item_data.get('description', 'No description')[:200],
                "date_created": item_data.get('date_created', 'N/A'),
                "keywords": item_data.get('keywords', [])[:5],
                "thumbnail": item['links'][0]['href'] if 'links' in item else None
            })
        
        return {
            "category": category,
            "search_query": query,
            "total_hits": total,
            "returned_results": len(results),
            "results": results,
            "tip": f"Try other categories: {', '.join(search_queries.keys())}"
        }
        
    except Exception as e:
        return {"error": str(e)}
@mcp.tool()
def help_search_instructions() -> dict:
    """
    Útmutató a NASA képek kereséséhez.
    MINDIG ezt a tool-t használd először NASA képek kereséséhez!
    
    Returns:
        Utasítások a helyes kereséshez
    """
    return {
        "important": "ALWAYS use search_nasa_images() tool for NASA image searches!",
        "never_do": [
            "Never generate fake NASA URLs",
            "Never create image links from memory",
            "Never use placeholder links"
        ],
        "always_do": [
            "Use search_nasa_images() for any NASA image query",
            "Use get_image_details() to get real download URLs",
            "Return actual NASA IDs (like 'as11-40-5903')",
            "Provide real links from API responses only"
        ],
        "example_workflow": {
            "user_asks": "Find Hubble images",
            "step1": "Call search_nasa_images('hubble telescope')",
            "step2": "Get results with real NASA IDs",
            "step3": "Optionally call get_image_details(nasa_id) for download links",
            "step4": "Present results with REAL data from API"
        }
    }
if __name__ == "__main__":
    # MCP szerver indítása
    mcp.run()