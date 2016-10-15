import ratebeer as rb
import scipy
import pymongo
import re
from unidecode import unidecode
import time 

db = pymongo.MongoClient()['beer_db']['reviews']

ratebeer = rb.RateBeer()
max_beer = 443552

n_ratings = 0


for beer_id in range(4, max_beer + 1):
    
    try:
	beer_props = ratebeer.beer('/beer/{0}/'.format(beer_id))
	beer_name = unidecode(beer_props['name'])
	beer_name_nice = re.sub('[()%.,/\'#\"]', '', beer_name.lower().replace(' ', '-'))

        beer = ratebeer.get_beer('/beer/{0}/{1}/'.format(beer_name_nice, beer_id))
        reviews = beer.get_reviews()
        
        for r in reviews:
            r_dict = {'beer_id': beer_id,
			'appearance': r.appearance,
			'aroma': r.aroma,
  			'date': r.date.strftime('%Y-%m-%d'),
			'overall': r.overall,
			'palate': r.palate,
			'rating': r.rating,
			'taste': r.taste,
			'user_location': r.user_location,
			'user_name': r.user_name}
            db.insert_one(r_dict)
            n_ratings += 1 
            if n_ratings % 1000 == 0:
                print 'ingested {0} ratings so far'.format(n_ratings) 

    except:
	pass

    sleep_time = scipy.random.exponential(2.5)

    if beer_id % 500 == 0:
        sleep_time = sleep_time * 10
	print "on beer number {0}, taking a quick nap".format(beer_id)

    time.sleep(sleep_time)
