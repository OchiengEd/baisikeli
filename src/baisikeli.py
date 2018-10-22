from settings import Configuration
from stravalib import Client
from model import DataStore
from flask import Flask
import json, sys
import requests

class Strava:

    def __init__(self):
        self.api_client = Client()
        config = Configuration('baisikeli.conf')
        self.db = DataStore()
        self.app_data = json.loads(config.get_strava_app_data())
        self.access_code = None

    def get_authorization_url(self):
        return self.api_client.authorization_url(client_id=self.app_data['client_id'], redirect_uri=self.app_data['redirect_uri'])

    def get_access_token(self, code):
        return self.api_client.exchange_code_for_token(client_id=self.app_data['client_id'], client_secret=self.app_data['client_secret'], code=code)

    def get_cyclist_info(self, access_code, athlete_id = None):
        headers = {'Authorization': 'Bearer {}'.format(access_code)}
        url = 'https://www.strava.com/api/v3/athlete'
        if athlete_id is not None:
            url = ''.join([url, '/', access_code])

        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            self.db.add_strava_athlete(request.json())
            return request.json()

    def get_activities(self):
        pass


if __name__ == '__main__':
    strava = Strava()
