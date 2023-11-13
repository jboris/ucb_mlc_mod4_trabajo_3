
import requests

from .service import Service


class KnowledgeGraphSearchServie(Service):
    def __init__(self):
        super().__init__('GoogleKnowledgeGraphSearch')

    def search_person(self, name, limit=1, verbose=False):
        params = {
            "query": name,
            "key": self.key,
            "limit": limit,
            "languages": "es"
        }
        response = requests.get(self.endpoint, params=params)
        data = response.json()
        if "itemListElement" in data and len(data["itemListElement"]) > 0:
            result = data["itemListElement"][0]["result"]
            description = result["detailedDescription"]["articleBody"]
            return description
        elif verbose:
            print("No se encontraron resultados para la consulta.")
