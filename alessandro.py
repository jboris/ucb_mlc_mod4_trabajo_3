from services.content import ContentSafetyServie
from services.language import LanguageServie
from services.search import KnowledgeGraphSearchService
from services.speech import SpeechServie


class AlessandroBot:
    def __init__(self):
        self.services = {
            'content_safety': ContentSafetyServie(),
            'language': LanguageServie(),
            'search': KnowledgeGraphSearchService(),
            'speech': SpeechServie(),
        }
        
    def ask(self, verbose=False, started_cb=None, completed_cb=None):
        if verbose:
            print('listen')
        query = self.services['speech'].listen()
        if verbose:
            print('query:', query)
        answer = 'No te escuche bien, ¿me puedes repetir la consulta?'
        if query:
            if self.services['content_safety'].is_offensive(query):
                answer = 'Lo siento, no puedo ayudarte porque he detectado contenido ofensivo en tu pregunta'
            else:
                summarized = self.services['language'].extractive_summarization(query)
                person = self.services['language'].recognize_person(summarized)
                if person:
                    info = self.services['search'].search_person(person)
                    if info:
                        answer = info
                    else:
                        answer = f'Lo siento, no puedo ayudarte porque no tengo información sobre {person}'
                else:
                    answer = 'Lo siento, soy un asistente únicamente orientado a darte información sobre figuras públicas.'
        if verbose:
            print('answer:', answer)
        self.services['speech'].talk(answer, verbose, started_cb, completed_cb)

if __name__ == "__main__":
    ale_bot = AlessandroBot()
    ale_bot.ask(True)
