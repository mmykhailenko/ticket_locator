import json

class ServiceResponse:
    def __init__(self, response):
        self.response = response
        print(self.response)
        self.to_json()

    def to_json(self):
        return json.dumps(self.response)