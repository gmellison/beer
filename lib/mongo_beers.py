import pymongo
import ratebeer
import time
import scipy.stats

client = pymongo.MongoClient()
db = client['beer_db']
beer_collection = db['beers']

rb = ratebeer.RateBeer()

for i in range(443552):
    try:
        beer = rb.beer('/beer/{0}/'.format(i))
        beer['brewery'] = beer['brewery'].url
        beer_collection.insert_one(beer)

    except:
        continue

    # get sleep time from exponential distribution
    sleep_time = scipy.stats.expon.rvs() / 2.0

    # every once in a while, sleep longer (I want to be nice to their servers...).
    if i % 500 == 0:
        sleep_time = 60 + sleep_time
    time.sleep(sleep_time)
