from pymongo import MongoClient
from pymongo.errors import OperationFailure
from settings import Configuration
import json

class DataStore:

	def __init__(self):
		self.configs = Configuration('baisikeli.conf')
		self.db = self.connect()

	def connect(self):
		try:
			database = json.loads(self.configs.get_db_connection_string())
			client = MongoClient(database['connection_string'])
			return client.get_database()
		except OperationFailure:
			print("Error connecting to database. \nPlease check credentials in config file")

class Strava_Model(DataStore):

	def __init__(self):
		super().__init__()
		self.tokens_collection = self.db['tokens']
		self.activities_collection = self.db['activities']

	def store_strava_athlete_token(self, athlete_token):
		self.tokens_collection.insert(athlete_token)

	def get_strava_athlete_token(self, email_address):
		return self.tokens_collection.find_one({'athlete_id': email_address })

	def update_strava_athlete_token(self, token):
		data = {'expires_at': token['expires_at'], 'refresh_token': token['refresh_token'], 'access_token': token['access_token']}
		self.tokens_collection.update_one({'athlete_id': token['athlete_id'] }, {'$set': data})

	def store_activities(self, activities):
		self.activities_collection.insert_many(activities['activities'])

	def get_athlete_activities(self, email_address):
		return self.activities_collection.find({'athlete_id', email_address})

class Auth_Model(DataStore):

	def __init__(self):
		super().__init__()
		self.user_collection = self.db['users']

	def create_user_account(self, user):
		self.user_collection.insert(user)

	def get_user(self, email_address):
		return self.user_collection.find_one({'email': email_address })

	def set_strava_token(self, athlete):
		self.user_collection.update_one({'email': athlete['email']}, {'$set' : {'strava_token': athlete['token']}}, upsert=False)
