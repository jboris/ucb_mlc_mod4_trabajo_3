import configparser
import azure.cognitiveservices.speech as speechsdk

from service import Service


class SpeechServie(Service):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        key = config.get('Speech', 'key')
        endpoint = config.get('Speech', 'endpoint')
        region = config.get('Speech', 'region')
        super().__init__(key, endpoint, region)
        self.config = speechsdk.SpeechConfig(subscription=self.key, endpoint=endpoint)

    def from_mic(self):
        print("Speak into your microphone.")
        recognizer = speechsdk.SpeechRecognizer(speech_config=self.config, language="es-BO")
        result = recognizer.recognize_once()
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(result.text))
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
