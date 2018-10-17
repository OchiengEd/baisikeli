import requests
from configparser import ConfigParser

class Strava:

    def __init__(self):
        self.strava_api_config = 'baisikeli.conf'
        strava_conf = ConfigParser()
        

    def default_strava_api_config(self):
        default_conf = ConfigParser()
        default_conf.add_section('strava')
        default_conf.set('strava', 'client_id', '1234')
        default_conf.set('strava', 'redirect_uri', 'http://www.domain.com/strava/authorization')
        with open(self.strava_api_config, 'w') as config:
            default_conf.write(config)

    def get_cyclist_info(self):
        pass

    def get_activities(self):
        pass


if __name__ == '__main__':
    strava = Strava()
    strava.default_strava_api_config()
