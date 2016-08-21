import pymongo.MongoClient
import ratebeer


client = pymongo.MongoClient()
db = client['beer_db']
db_beers = db['beers']

rb = ratebeer.RateBeer()

for i in range(500000):
    beer = rb.beer('/beer/{0}/'.format(i))
