from pymongo import MongoClient
from settings import Configuration
import json

class DataStore:

	def __init__(self):
		self.configs = Configuration('baisikeli.conf')
		self.db = self.connect()

	def connect(self):
		database = json.loads(self.configs.get_db_connection_string())
		client = MongoClient(database['connection_string'])
		return client[database['db']]

	def add_strava_athlete(self, strava_athlete):
		athlete_collection = self.db['athletes']
		athlete_collection.insert(strava_athlete)

	def search_strava_athlete(self, strava_username):
		athlete_collection = self.db['athletes']
		return athlete_collection.find({'username': strava_username })

	def show_collections(self):
		return self.db.list_collection_names()

	def store_activities(self, activities):
		activities_collection = self.db['activities']
		activities_collection.insert_many(activities['activities'])

class Auth_Model(DataStore):

	def __init__(self):
		super().__init__()
		user_collection = self.db['user']

	def create_user_account(self, user):
		user_collection.insert(user)

	def authenticate_user(self, user):
		input_password = user['password']
		user_collection.find({'username': user['username'] })
