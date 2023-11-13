
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

from .service import Service


class ContentSafetyServie(Service):
    def __init__(self):
        super().__init__('ContentSafety')
        self.client = ContentSafetyClient(self.endpoint, AzureKeyCredential(self.key))

    def analyze_text(self, text, verbose=False):
        request = AnalyzeTextOptions(text=text)
        try:
            response = self.client.analyze_text(request)
        except HttpResponseError as e:
            if verbose:
                print("Analyze text failed.")
                if e.error:
                    print(f"Error code: {e.error.code}")
                    print(f"Error message: {e.error.message}")
                    raise
                print(e)
                raise
        return {
            'hate': response.hate_result.severity,
            'self_harm': response.self_harm_result.severity,
            'sexual': response.sexual_result.severity,
            'violence': response.violence_result.severity
        }
        
    def is_offensive(self, text, verbose=False):
        analysis = self.analyze_text(text, verbose)
        return sum(analysis.values()) > 0
        
