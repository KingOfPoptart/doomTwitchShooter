import requests

class doomApiClient:
    def __init__(self, host="localhost", port=666):
        self.host = host
        self.port = port