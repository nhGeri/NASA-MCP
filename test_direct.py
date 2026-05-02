import requests

def test_search_nasa_images(query, media_type="image", year_start="", year_end="", page_size=10):
    url = "https://images-api.nasa.gov/search"
    params = {
        "q": query,
        "media_type": media_type,
        "page_size": min(page_size, 100)
    }
    
    if year_start:
        params["year_start"] = year_start
    if year_end:
        params["year_end"] = year_end
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    items = data['collection']['items']
    total_hits = data['collection']['metadata']['total_hits']
    
    markdown_results = [f"Searched NASA's complete database. Found {total_hits:,} total items for query '{query}'.\n"]
    for item in items:
        item_data = item['data'][0]
        title = item_data.get('title', 'Untitled')
        description = item_data.get('description', '')
        image_url = item['links'][0]['href'] if 'links' in item else ''
        
        if image_url:
            markdown_results.append(f"### {title}\n\n![NASA Image]({image_url})\n\n{description}\n---")
        else:
            markdown_results.append(f"### {title}\n\n{description}\n---")
            
    if len(markdown_results) == 1:
        return "No results found."
        
    return "\n\n".join(markdown_results)

if __name__ == "__main__":
    print("Tesztelés indítása: 'apollo 11' kifejezésre (2 találat)...\n")
    eredmeny = test_search_nasa_images("apollo 11", page_size=2)
    print(eredmeny)
