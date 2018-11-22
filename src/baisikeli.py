from settings import Configuration
from urllib.parse import urlencode
from model import Strava_Model
from flask import Flask
from time import time
import json, sys
import requests

class Strava:

    def __init__(self):
        config = Configuration('baisikeli.conf')
        self.db = Strava_Model()
        self.app_data = json.loads(config.get_strava_app_data())
        self.access_token = None

    def get_current_time_in_epoch(self):
        return int(time())

    def get_strava_authorization_url(self):
        params = urlencode({'client_id': self.app_data['client_id'],
                            'redirect_uri': self.app_data['redirect_uri'],
                            'approval_prompt': 'auto',
                            'response_type': 'code',
                            'scope': 'activity:read'
                            })
        return 'https://www.strava.com/oauth/authorize?{}'.format(params)

    def get_strava_access_token(self, code, email_address):
        token = None
        params = {
                'client_id': self.app_data['client_id'],
                'client_secret': self.app_data['client_secret'],
                'code': code,
                'grant_type': 'authorization_code'
                }

        response = requests.post('https://www.strava.com/oauth/token', data=params)
        if response.status_code == 200:
            strava_user = response.json()
            token = {
                'expires_at': strava_user['expires_at'],
                'refresh_token': strava_user['refresh_token'],
                'access_token': strava_user['access_token'],
                'strava_id': strava_user['athlete']['id'],
                'athlete_id': email_address
                }

            self.db.store_strava_athlete_token(token)

            return token

    def renew_strava_access_token(self, email):
        stored_token = self.db.get_strava_athlete_token(email)

        params = {
                'client_id': self.app_data['client_id'],
                'client_secret': self.app_data['client_secret'],
                'refresh_token': stored_token['refresh_token'],
                'grant_type': 'refresh_token'
                }

        response = requests.post('https://www.strava.com/oauth/token', data=params)
        if response.status_code == 200:
            new_token = response.json()
            new_token['athlete_id'] = email
            self.db.update_strava_athlete_token(new_token)
            return new_token

    def is_access_token_expired(self, email):
        token = self.db.get_strava_athlete_token(email)
        if token is None:
            return False
        else:
            return True if self.get_current_time_in_epoch() > token['expires_at'] else False

    def get_strava_access_token_from_db(self, email):
        if self.is_access_token_expired(email):
            return self.renew_strava_access_token(email)
        else:
            return self.db.get_strava_athlete_token(email)

    # def get_cyclist_info(self, access_token, athlete_id = None):
    def get_cyclist_info(self, email):
        token = self.get_strava_access_token_from_db(email)

        headers = {'Authorization': 'Bearer {}'.format(token['access_token'])}
        url = 'https://www.strava.com/api/v3/athlete'

        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            # self.db.add_strava_athlete(request.json())
            return request.json()

    # name, start_date, average_speed, max_sped, athlete[id], average_heartrate, max_heartrate, timezone
    def get_activities(self, email):
        token = self.get_strava_access_token_from_db(email)
        print(token)

        activities = []
        headers = {'Authorization': 'Bearer {}'.format(token['access_token'])}
        url = 'https://www.strava.com/api/v3/activities'
        if token['strava_id'] is not None:
            ''.join([url, '/', str(token['strava_id']) ])

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            for ride in response.json():
                ride_stats = {
                    'name': ride['name'],
                    'start_date': ride['start_date'],
                    'strava_id': ride['athlete']['id'],
                    'average_speed': ride['average_speed'],
                    'max_speed': ride['max_speed'],
                    'timezone': ride['timezone'],
                    'athlete_id': email
                    }
                if 'average_heartrate' in ride.keys():
                    ride_stats['average_hr'] = ride['average_heartrate']
                    ride_stats['max_hr'] = ride['max_heartrate']
                activities.append(ride_stats)
        return { 'activities': activities }
