
from azure.ai.textanalytics import ExtractiveSummaryAction, TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

from .service import Service


class LanguageServie(Service):
    def __init__(self):
        super().__init__('Language')
        self.client = text_analytics_client = TextAnalyticsClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.key))

    def extractive_summarization(self, document, verbose=False):
        poller = self.client.begin_analyze_actions(
            [document],
            actions=[
                ExtractiveSummaryAction(max_sentence_count=1)
            ],
        )
        document_results = poller.result()
        for result in document_results:
            extract_summary_result = result[0]
            if not extract_summary_result.is_error:
                summarization = " ".join([sentence.text.strip() for sentence in extract_summary_result.sentences])
                return ' '.join(summarization.split())
            elif verbose:
                print("Error: '{}' - Mensaje: '{}'".format(
                    extract_summary_result.code, extract_summary_result.message
                ))
    
    def recognize_person(self, document, verbose=False):
        persons = []
        try:
            entities = self.client.recognize_entities(documents=[document])[0].entities
            for entity in entities:
                if entity.category == 'Person':
                    persons.append([entity.confidence_score, entity.text])
        except Exception as err:
            if verbose:
                print("Encountered exception. {}".format(err))
        if persons:
            persons = sorted(persons)
            return persons[-1][1]
        return None
        
