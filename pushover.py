import http.client
import json

class PushoverError(Exception):
    def __init__(self, message):
        self.message = message

class Pushover:
    def __init__(self, application_token, user_key, api_version=1):
        self.application_token = application_token
        self.user_key = user_key
        self.api_version = api_version

    def send(self, message=None, title=None):
        if not message:
            raise PushoverError('Message cannot be empty!')

        conn = http.client.HTTPSConnection('api.pushover.net')

        request = {
            'token': self.application_token,
            'user': self.user_key,
            'title': title,
            'message': message
        }

        request_json = json.dumps(request)
        headers = { 'Content-Type': 'application/json'  }
        conn.request('POST', f'/{self.api_version}/messages.json', request_json, headers)

        response = conn.getresponse()
        print(response.read().decode())
