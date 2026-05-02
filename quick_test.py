import sys
sys.path.append('C:/Users/nagyh/source/repos/NASA-MCP')
from mcp_server import search_nasa_images

# Keresés
# Keresés
results = search_nasa_images(query='apollo 11', page_size=2)
print(results)
