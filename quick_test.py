import sys
sys.path.append('C:/Users/nagyh/source/repos/NASA-MCP')
from mcp_server import search_nasa_images

# Keresés
results = search_nasa_images(query='apollo 11', page_size=3)
print(f'\n✅ Found {results["total_hits"]:,} images!\n')

for idx, item in enumerate(results['results'], 1):
    print(f'{idx}. {item["title"]}')
    print(f'   ID: {item["nasa_id"]}\n')
