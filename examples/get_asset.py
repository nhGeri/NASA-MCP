"""
NASA API - Asset Manifest példa
Lekéri egy kép összes elérhető verzióját
"""

import requests

def get_asset_manifest(nasa_id):
    """
    Lekéri egy kép/videó asset manifest-jét
    
    Args:
        nasa_id: NASA azonosító (pl. "as11-40-5903")
    """
    print(f"🔍 Asset manifest lekérése: {nasa_id}\n")
    
    try:
        # API hívás
        response = requests.get(
            f"https://images-api.nasa.gov/asset/{nasa_id}",
            timeout=10
        )
        
        response.raise_for_status()
        data = response.json()
        
        # Elérhető fájlok
        items = data['collection']['items']
        
        print(f"✅ Elérhető fájlok: {len(items)}\n")
        
        # Kiírás
        for idx, item in enumerate(items, 1):
            url = item['href']
            filename = url.split('/')[-1]
            
            # Méret megállapítása a fájlnévből
            if 'orig' in filename:
                size = "Eredeti (nagy)"
            elif 'large' in filename:
                size = "Nagy"
            elif 'medium' in filename:
                size = "Közepes"
            elif 'small' in filename:
                size = "Kicsi"
            elif 'thumb' in filename:
                size = "Thumbnail"
            else:
                size = "Egyéb"
            
            print(f"{idx}. [{size}] {filename}")
            print(f"   URL: {url}\n")
        
        return data
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Hiba: {e}")
        print(f"   Status kód: {e.response.status_code}")
    except requests.exceptions.Timeout:
        print("❌ Timeout: A szerver nem válaszolt 10 másodpercen belül")
    except Exception as e:
        print(f"❌ Hiba: {e}")
        return None


def demo_with_search():
    """
    Teljes demo: Keresés + Asset lekérés
    """
    print("=" * 60)
    print("NASA API - ASSET MANIFEST DEMO")
    print("=" * 60 + "\n")
    
    # 1. Először keresünk egy képet
    print("1️⃣ Keresés 'apollo 11' képekre...\n")
    
    search_response = requests.get(
        "https://images-api.nasa.gov/search",
        params={"q": "apollo 11", "media_type": "image", "page_size": 1}
    )
    search_data = search_response.json()
    
    # Első találat
    first_item = search_data['collection']['items'][0]
    nasa_id = first_item['data'][0]['nasa_id']
    title = first_item['data'][0]['title']
    
    print(f"✅ Találat: {title}")
    print(f"   NASA ID: {nasa_id}\n")
    print("-" * 60 + "\n")
    
    # 2. Asset manifest lekérése
    print("2️⃣ Asset manifest lekérése...\n")
    asset_data = get_asset_manifest(nasa_id)
    
    # 3. Választás és letöltés (opcionális)
    if asset_data:
        print("-" * 60 + "\n")
        print("3️⃣ Letöltés példa:\n")
        
        # Thumbnail letöltése
        items = asset_data['collection']['items']
        thumb_url = None
        
        for item in items:
            if 'thumb' in item['href']:
                thumb_url = item['href']
                break
        
        if thumb_url:
            print(f"📥 Thumbnail letöltése...")
            img_response = requests.get(thumb_url)
            
            filename = f"{nasa_id}_thumb.jpg"
            with open(filename, "wb") as f:
                f.write(img_response.content)
            
            print(f"✅ Letöltve: {filename}")
        else:
            print("❌ Thumbnail nem található")


if __name__ == "__main__":
    # Válassz:
    
    # Opció 1: Csak asset lekérés ismert ID-val
    # get_asset_manifest("as11-40-5903")
    
    # Opció 2: Teljes demo (search + asset)
    demo_with_search()