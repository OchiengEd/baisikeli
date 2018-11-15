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
		self.athletes_collection = self.db['athletes']
		self.activities_collection = self.db['activities']

	def add_strava_athlete(self, strava_athlete):
		self.athletes_collection.insert(strava_athlete)

	def search_strava_athlete(self, email_address):
		return self.athletes_collection.find({'email': email_address })

	def store_activities(self, activities):
		self.activities_collection.insert_many(activities['activities'])

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


if __name__ == '__main__':
	user = Auth_Model()
	print(user.get_user('ochienged@gmail.com'))
	# user.create_user_account({'lastname': 'Ochieng', 'firstname': 'Edmund', 'password': 'pbkdf2:sha256:50000$l8WBC6tV$fc34765f759137dcd167aa44fc3fe629376322d96d782906cc6376366c10c7f3', 'email': 'ochienged@gmail.com'})
