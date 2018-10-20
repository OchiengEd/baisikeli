from configparser import ConfigParser
from stravalib import Client
from flask import Flask
import json, sys
import requests

class Configuration:
    def __init__(self, config_file):
        self.config_file = config_file
        self.app_config = ConfigParser()
        self.config_check()

    def config_check(self):
        try:
            f = open(self.config_file, 'r')
        except FileNotFoundError:
            self.create_basic_config()
            print("New config created at %s. Update with app settings before retrying" % self.config_file)
            sys.exit(1)

    def create_basic_config(self):
        default_config = self.app_config
        default_config.add_section('strava')
        default_config.set('strava', 'client_id', '1234')
        default_config.set('strava', 'client_secret', 'rand0mstr1ng')
        default_config.set('strava', 'redirect_uri', 'http://www.yourdomain.com/authorization')
        with open(self.config_file, 'w') as application_config:
            default_config.write(application_config)

    def get_strava_app_data(self):
        app_data = self.app_config
        app_data.read(self.config_file)
        return json.dumps({
                'client_id': app_data['strava']['client_id'],
                'client_secret': app_data['strava']['client_secret'],
                'redirect_uri': app_data['strava']['redirect_uri']
                })


class Strava:

    def __init__(self):
        self.api_client = Client()
        config = Configuration('baisikeli.conf')
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
            return request.json()



    def get_activities(self):
        pass


if __name__ == '__main__':
    strava = Strava()
