
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
    
