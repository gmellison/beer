import pymongo
import ratebeer
import time
import scipy.stats

client = pymongo.MongoClient()
db = client['beer_db']
beer_collection = db['beers']

rb = ratebeer.RateBeer()
e = 0
n = 0

for i in range(121952, 443552):
    try:
        beer = rb.beer('/beer/{0}/'.format(i))
        beer['brewery'] = beer['brewery'].url
        beer_collection.insert_one(beer)

    except:
        continue
        e += 1
    n += 1

    # get sleep time from exponential distribution
    sleep_time = scipy.stats.expon.rvs() * .75

    # every once in a while, sleep longer (I want to be nice to their servers...).
    if i % 500 == 0:
	print 'ingested {0} messages, time for a quick nap'.format(n - e)
        sleep_time = 40 + sleep_time
    time.sleep(sleep_time)
