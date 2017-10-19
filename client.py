import datetime
import requests
import jwt

class RoutesClient:
    def __init__(self, base_url, key_path, client_id):
        self.base_url = base_url
        self.key_path = key_path
        self.params = self.get_params(client_id)
        self.headers = self.get_headers()

    def get_routes(self):
        response = requests.get(
            self.base_url + '/routes',
            headers=self.headers,
            params=self.params
        )
        return response.json()

    def status(self, message):
        response = requests.post(
            self.base_url + '/status',
            json=message,
            headers=self.headers,
            params=self.params
        )
        return response.json()

    def walk(self, message):
        response = requests.post(
            self.base_url + '/walk',
            json=message,
            headers=self.headers,
            params=self.params
        )
        return response.json()

    def get_params(self, client_id):
        return {'client_id': client_id}

    def get_headers(self):
        token = self.get_token()
        return {'Authorization': 'Bearer ' + token.decode('utf-8')}

    def get_token(self):
        key = self.get_key()
        expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=7200)
        body = {'exp': expiration}
        return jwt.encode(body, key, algorithm='RS256')

    def get_key(self):
        key_file = open(self.key_path, 'r')
        return key_file.read()
