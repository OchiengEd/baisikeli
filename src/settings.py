from configparser import ConfigParser
import json

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

        default_config.add_section('mongo')
        default_config.set('mongo', 'username', 'baisikeli')
        default_config.set('mongo', 'password', 'baisikelipasswd')
        default_config.set('mongo', 'host', '127.0.0.1')
        default_config.set('mongo', 'port', '27017')
        default_config.set('database', 'baisikeli')

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

    def get_db_connection_string(self):
        app_data = self.app_config
        app_data.read(self.config_file)
        db_uri = "mongodb://%s:%s@%s:%s" % (
                app_data['mongo']['username'],
                app_data['mongo']['password'],
                app_data['mongo']['host'],
                app_data['mongo']['port']
                )
        return json.dumps({ 'connection_string': db_uri, 'db': app_data['mongo']['database'] })
