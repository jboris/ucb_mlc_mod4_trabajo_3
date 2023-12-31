
import requests

from .service import Service


class KnowledgeGraphSearchService(Service):
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
        try:
            if "itemListElement" in data and len(data["itemListElement"]) > 0:
                result = data["itemListElement"][0]["result"]
                description = result["detailedDescription"]["articleBody"]
                return description
            else:
                if verbose:
                    print("No se encontraron resultados para la consulta.")
                return None
        except:
            if verbose:
                    print("No se encontraron resultados para la consulta.")
            return None
