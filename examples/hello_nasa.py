"""
NASA API egyszerű teszt
"""

import requests

def test_nasa_api():
    print("🚀 NASA API Teszt\n")
    
    try:
        response = requests.get(
            "https://images-api.nasa.gov/search",
            params={"q": "moon", "media_type": "image", "page_size": 3},
            timeout=10
        )
        
        response.raise_for_status()
        data = response.json()
        
        total = data['collection']['metadata']['total_hits']
        print(f"✅ Sikeres kapcsolat!")
        print(f"📊 Találatok: {total:,}\n")
        
        print("🖼️  Első 3 találat:")
        for idx, item in enumerate(data['collection']['items'], 1):
            title = item['data'][0]['title']
            nasa_id = item['data'][0]['nasa_id']
            print(f"{idx}. {title}")
            print(f"   ID: {nasa_id}\n")
        
    except Exception as e:
        print(f"❌ Hiba: {e}")

if __name__ == "__main__":
    test_nasa_api()
