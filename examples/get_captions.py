"""
NASA API - Captions példa
Lekéri egy videó feliratait
"""

import requests

def get_captions(nasa_id):
    """
    Lekéri egy videó feliratait (captions)
    
    Args:
        nasa_id: NASA videó azonosító
    """
    print(f"📝 Captions lekérése: {nasa_id}\n")
    
    try:
        # API hívás
        response = requests.get(
            f"https://images-api.nasa.gov/captions/{nasa_id}",
            timeout=10
        )
        
        response.raise_for_status()
        data = response.json()
        
        # Caption URL
        caption_url = data.get('location')
        
        if caption_url:
            print(f"✅ Caption URL: {caption_url}\n")
            
            # Caption tartalom letöltése
            print("📥 Caption tartalom letöltése...\n")
            caption_response = requests.get(caption_url, timeout=10)
            
            print("📝 Caption tartalom:")
            print("-" * 60)
            print(caption_response.text[:500])  # Első 500 karakter
            print("...")
            print("-" * 60)
            
            return caption_response.text
        else:
            print("❌ Caption URL nem található")
            return None
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("❌ Ez a média nem rendelkezik felirattal")
            print("   (Csak videókhoz van caption)")
        else:
            print(f"❌ HTTP Hiba: {e}")
    except Exception as e:
        print(f"❌ Hiba: {e}")
        return None


def demo_video_search():
    """
    Videó keresés és caption lekérés
    """
    print("=" * 60)
    print("NASA API - VIDEO CAPTIONS DEMO")
    print("=" * 60 + "\n")
    
    # 1. Videó keresés
    print("1️⃣ Videók keresése...\n")
    
    search_response = requests.get(
        "https://images-api.nasa.gov/search",
        params={"q": "moon landing", "media_type": "video", "page_size": 3}
    )
    search_data = search_response.json()
    
    items = search_data['collection']['items']
    
    if not items:
        print("❌ Nincs videó találat")
        return
    
    print(f"✅ {len(items)} videó találat:\n")
    
    for idx, item in enumerate(items, 1):
        data = item['data'][0]
        nasa_id = data['nasa_id']
        title = data['title']
        
        print(f"{idx}. {title}")
        print(f"   ID: {nasa_id}\n")
    
    print("-" * 60 + "\n")
    
    # 2. Első videó caption-jének lekérése
    print("2️⃣ Első videó caption-je...\n")
    first_video_id = items[0]['data'][0]['nasa_id']
    get_captions(first_video_id)


if __name__ == "__main__":
    # Válassz:
    
    # Opció 1: Ismert videó ID
    # get_captions("NHQ_2019_0311_Go Forward to the Moon")
    
    # Opció 2: Videó keresés + captions
    demo_video_search()