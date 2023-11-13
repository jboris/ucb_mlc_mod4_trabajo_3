import configparser

class Service:
    def __init__(self, name):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.key = config.get(name, 'key')
        self.endpoint = config.get(name, 'endpoint')
        self.region = config.get(name, 'region')

