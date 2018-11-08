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
		return client.get_database()

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
		self.user_collection = self.db['user']

	def create_user_account(self, user):
		self.user_collection.insert(user)

	def get_user(self, email_address):
		return self.user_collection.find_one({'email': email_address })


if __name__ == '__main__':
	user = Auth_Model()
	print(user.get_user('ochienged@gmail.com'))
	# user.create_user_account({'lastname': 'Ochieng', 'firstname': 'Edmund', 'password': 'pbkdf2:sha256:50000$l8WBC6tV$fc34765f759137dcd167aa44fc3fe629376322d96d782906cc6376366c10c7f3', 'email': 'ochienged@gmail.com'})
