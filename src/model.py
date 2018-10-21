from pymongo import MongoClient

class DataStore:

	def __init__(self):
		self.db = self.connect()

	def connect(self):
		uri = 'mongodb://localhost:27017/'
		client = MongoClient(uri)
		return client['baisikeli']

	def add_strava_athlete(self, strava_athlete):
		athlete_collection = self.db['athlete']
		athlete_collection.insert(strava_athlete)

	def search_strava_athlete(self):
		athlete_collection = self.db['athlete']
		return athlete_collection.find({'':''})

	def show_collections(self):
		return self.db.list_collection_names()

def main():
	ds = DataStore()
	print(ds.show_collections())

if __name__ == '__main__':
	main()
