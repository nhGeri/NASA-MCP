"""
NASA API - Metadata példa
Lekéri egy kép részletes metaadatait
"""

import requests

def get_metadata(nasa_id):
    """
    Lekéri egy kép/videó metaadatait
    
    Args:
        nasa_id: NASA azonosító
    """
    print(f"📋 Metadata lekérése: {nasa_id}\n")
    
    try:
        # API hívás
        response = requests.get(
            f"https://images-api.nasa.gov/metadata/{nasa_id}",
            timeout=10
        )
        
        response.raise_for_status()
        data = response.json()
        
        # Metadata URL
        metadata_url = data.get('location')
        
        if metadata_url:
            print(f"✅ Metadata URL: {metadata_url}\n")
            
            # Metadata tartalom lekérése
            print("📥 Metadata tartalom letöltése...\n")
            metadata_response = requests.get(metadata_url, timeout=10)
            metadata_content = metadata_response.json()
            
            # Kiírás
            print("📊 Metadata információk:")
            print("-" * 60)
            
            # EXIF adatok (ha vannak)
            if 'AVAIL:EXIF' in metadata_content:
                exif = metadata_content['AVAIL:EXIF']
                print("\n🔧 EXIF Adatok:")
                for key, value in exif.items():
                    print(f"  {key}: {value}")
            
            # XMP adatok (ha vannak)
            if 'XMP' in metadata_content:
                xmp = metadata_content['XMP']
                print("\n📸 XMP Adatok:")
                for key, value in xmp.items():
                    if isinstance(value, dict):
                        print(f"  {key}:")
                        for k, v in value.items():
                            print(f"    {k}: {v}")
                    else:
                        print(f"  {key}: {value}")
            
            return metadata_content
        else:
            print("❌ Metadata URL nem található")
            return None
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Hiba: {e}")
        print(f"   Status kód: {e.response.status_code}")
    except Exception as e:
        print(f"❌ Hiba: {e}")
        return None


def demo_full_info():
    """
    Teljes információ egy képről: Search + Asset + Metadata
    """
    print("=" * 60)
    print("NASA API - TELJES INFORMÁCIÓ DEMO")
    print("=" * 60 + "\n")
    
    # 1. Keresés
    print("1️⃣ Keresés...\n")
    search_response = requests.get(
        "https://images-api.nasa.gov/search",
        params={"q": "apollo 11", "media_type": "image", "page_size": 1}
    )
    search_data = search_response.json()
    
    item = search_data['collection']['items'][0]
    data = item['data'][0]
    
    nasa_id = data['nasa_id']
    title = data['title']
    description = data.get('description', 'N/A')
    date_created = data.get('date_created', 'N/A')
    
    print(f"📷 Cím: {title}")
    print(f"🆔 ID: {nasa_id}")
    print(f"📅 Dátum: {date_created}")
    print(f"📝 Leírás: {description[:100]}...")
    print("\n" + "-" * 60 + "\n")
    
    # 2. Asset
    print("2️⃣ Asset fájlok...\n")
    asset_response = requests.get(
        f"https://images-api.nasa.gov/asset/{nasa_id}"
    )
    asset_data = asset_response.json()
    asset_count = len(asset_data['collection']['items'])
    
    print(f"✅ {asset_count} féle verzió elérhető")
    print("\n" + "-" * 60 + "\n")
    
    # 3. Metadata
    print("3️⃣ Részletes metadata...\n")
    get_metadata(nasa_id)


if __name__ == "__main__":
    # Válassz:
    
    # Opció 1: Csak metadata
    # get_metadata("as11-40-5903")
    
    # Opció 2: Teljes info
    demo_full_info()