from settings import Configuration
from urllib.parse import urlencode
from model import Strava_Model
from flask import Flask
import json, sys
import requests

class Strava:

    def __init__(self):
        config = Configuration('baisikeli.conf')
        self.db = Strava_Model()
        self.app_data = json.loads(config.get_strava_app_data())
        self.access_code = None

    def get_strava_authorization_url(self):
        params = urlencode({'client_id': self.app_data['client_id'],
                            'redirect_uri': self.app_data['redirect_uri'],
                            'approval_prompt': 'auto',
                            'response_type': 'code',
                            'scope': 'read'
                            })
        return 'https://www.strava.com/oauth/authorize?{}'.format(params)

    def get_strava_access_token(self, code, email_address):
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

            self.db.store_strava_token(token)

            return token['access_token']

    def refresh_access_token(self):
        pass

    def get_cyclist_info(self, access_code, athlete_id = None):
        headers = {'Authorization': 'Bearer {}'.format(access_code)}
        url = 'https://www.strava.com/api/v3/athlete'
        if athlete_id is not None:
            url = ''.join([url, '/', access_code])

        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            self.db.add_strava_athlete(request.json())
            return request.json()

    # name, start_date, average_speed, max_sped, athlete[id], average_heartrate, max_heartrate, timezone
    def get_activities(self, access_code, athlete_id = None):
        activities = []
        headers = {'Authorization': 'Bearer {}'.format(access_code)}
        url = 'https://www.strava.com/api/v3/activities'
        if athlete_id is not None:
            ''.join([url, '/', athlete_id])

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            for ride in response.json():
                ride_stats = {
                    'name': ride['name'],
                    'start_date': ride['start_date'],
                    'athlete_id': ride['athlete']['id'],
                    'average_speed': ride['average_speed'],
                    'max_speed': ride['max_speed'],
                    'timezone': ride['timezone']
                    }
                if 'average_heartrate' in ride.keys():
                    ride_stats['average_hr'] = ride['average_heartrate']
                    ride_stats['max_hr'] = ride['max_heartrate']
                activities.append(ride_stats)
        return { 'activities': activities }
