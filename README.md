# 🚀 NASA-MCP - Image and Video Library API

NASA Image and Video Library API használata Python-ban.

## 📋 Projekt Célja

A NASA nyilvános képtárának programozási felületen való elérése és használata.

## 🔧 Technológiák

- Python 3.8+
- Requests library
- REST API

## 📚 API Információk

**Base URL**: `https://images-api.nasa.gov`

**Végpontok**:
- `/search` - Keresés
- `/asset/{nasa_id}` - Asset manifest
- `/metadata/{nasa_id}` - Metadata

## 🚀 Használat
```python
import requests

response = requests.get(
    "https://images-api.nasa.gov/search",
    params={"q": "moon", "media_type": "image"}
)

data = response.json()
print(f"Találatok: {data['collection']['metadata']['total_hits']}")
```

## 📁 Struktúra
```
NASA-MCP/
├── src/           # Forráskód
├── docs/          # Dokumentáció
├── examples/      # Példák
├── tests/         # Tesztek
└── README.md
```

## 🎓 Projekt Info

Készítette: Nagy-Horváth Gergő  
Dátum: 2025  
Cél: NASA API technikai megismerése