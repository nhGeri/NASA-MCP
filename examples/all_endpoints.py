"""
NASA API - Összes Endpoint Demo
Bemutatja mind a 4 végpontot
"""

import requests
import json

def search(query, media_type="image"):
    """1. Search endpoint"""
    print(f"\n🔍 SEARCH: '{query}' ({media_type})")
    print("-" * 60)
    
    response = requests.get(
        "https://images-api.nasa.gov/search",
        params={"q": query, "media_type": media_type, "page_size": 3}
    )
    data = response.json()
    
    total = data['collection']['metadata']['total_hits']
    items = data['collection']['items']
    
    print(f"✅ Találatok: {total:,}")
    print(f"📋 Megjelenítve: {len(items)}\n")
    
    for idx, item in enumerate(items, 1):
        nasa_id = item['data'][0]['nasa_id']
        title = item['data'][0]['title']
        print(f"{idx}. {title}")
        print(f"   ID: {nasa_id}")
    
    return items[0]['data'][0]['nasa_id'] if items else None


def asset(nasa_id):
    """2. Asset endpoint"""
    print(f"\n📦 ASSET: {nasa_id}")
    print("-" * 60)
    
    response = requests.get(
        f"https://images-api.nasa.gov/asset/{nasa_id}"
    )
    data = response.json()
    
    items = data['collection']['items']
    print(f"✅ Elérhető fájlok: {len(items)}\n")
    
    for idx, item in enumerate(items, 1):
        url = item['href']
        filename = url.split('/')[-1]
        print(f"{idx}. {filename}")


def metadata(nasa_id):
    """3. Metadata endpoint"""
    print(f"\n📋 METADATA: {nasa_id}")
    print("-" * 60)
    
    response = requests.get(
        f"https://images-api.nasa.gov/metadata/{nasa_id}"
    )
    data = response.json()
    
    metadata_url = data.get('location')
    
    if metadata_url:
        print(f"✅ Metadata URL létezik")
        print(f"   {metadata_url[:60]}...")
    else:
        print("❌ Nincs metadata")


def captions(nasa_id):
    """4. Captions endpoint"""
    print(f"\n📝 CAPTIONS: {nasa_id}")
    print("-" * 60)
    
    try:
        response = requests.get(
            f"https://images-api.nasa.gov/captions/{nasa_id}"
        )
        response.raise_for_status()
        data = response.json()
        
        caption_url = data.get('location')
        
        if caption_url:
            print(f"✅ Caption URL létezik")
            print(f"   {caption_url[:60]}...")
        else:
            print("❌ Nincs caption")
    except requests.exceptions.HTTPError:
        print("❌ Nincs caption (Csak videókhoz van)")


def main():
    """Főprogram - Mind a 4 endpoint bemutatása"""
    print("=" * 60)
    print("NASA API - MIND A 4 ENDPOINT DEMO")
    print("=" * 60)
    
    # 1. Search (kép)
    nasa_id = search("apollo 11", "image")
    
    if nasa_id:
        # 2. Asset
        asset(nasa_id)
        
        # 3. Metadata
        metadata(nasa_id)
        
        # 4. Captions (nem lesz, mert kép)
        captions(nasa_id)
    
    # Videó példa
    print("\n" + "=" * 60)
    print("VIDEÓ PÉLDA")
    print("=" * 60)
    
    video_id = search("moon landing", "video")
    
    if video_id:
        asset(video_id)
        captions(video_id)
    
    print("\n" + "=" * 60)
    print("✅ DEMO BEFEJEZVE")
    print("=" * 60)


if __name__ == "__main__":
    main()