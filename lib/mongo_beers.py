import pymongo
import ratebeer
import time
import scipy.stats

client = pymongo.MongoClient()
db = client['beer_db']
beer_collection = db['beers']

rb = ratebeer.RateBeer()
s = 0
e = 0

for i in range(443552):
    try:
        beer = rb.beer('/beer/{0}/'.format(i))
        beer['brewery'] = beer['brewery'].url
        beer_collection.insert_one(beer)

    except:
        # count the exception
        e += 1
        continue

    # get sleep time from exponential distribution
    sleep_time = scipy.stats.expon.rvs() * 3.0

    # every once in a while, sleep longer (I want to be nice to their servers...).
    if i % 100 == 0:
        sleep_time = 60 + sleep_time
        print('ingested {0} messages, time for a quick nap. \n'.format(i - e))
        print('{0} elapsed so far'.format(s))

    time.sleep(sleep_time)
    s += sleep_time


# find max beer id
m = 0
for beer in beers.find():
    url = beer['url']
    bid = int(url[6:len(url) - 1])
    if bid > m:
        m = bid
