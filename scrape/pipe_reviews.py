import ratebeer as rb
import re
from unidecode import unidecode
import time 
import psycopg2 as ps

ratebeer = rb.RateBeer()

def connect_beer_db():
    dbcon = ps.connect(dbname = 'greg', user = 'greg', password = 'ohhello')
    cur = dbcon.cursor()
    return dbcon

def get_beer(beer_id):
    beer_props = ratebeer.beer('/beer/{0}/'.format(beer_id))
    beer_name = unidecode(beer_props['name'])
    beer_name_nice = re.sub('[()%.,/\'#\"]', '', beer_name.lower().replace(' ', '-'))

    beer = ratebeer.get_beer('/beer/{0}/{1}/'.format(beer_name_nice, beer_id))
    beer.beer_name = beer_name_nice
    beer.beer_id = beer_id
    beer.brewery_id = int(beer.brewery.url.split('/')[3])
    beer.style_id = int(beer.style_url.split('/')[3]) 

    return beer    

def insert_beer(dbcon, beer):
    cur = dbcon.cursor()
    try:
        cur.execute("""insert into rate_beer.beers (
            beer_id,
            beer_name,
            brewery_id, 
            style_id,
            overall_rating,
            mean_rating,
            style_rating,
            weighted_avg,
            num_ratings,
            calories,
            ibu,
            abv,
            retired,
            seasonal,
            tags,
            description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (beer.beer_id,
             beer.beer_name, 
             beer.brewery_id, 
             beer.style_id,
             beer.overall_rating,
             beer.mean_rating,
             beer.style_rating,
             beer.weighted_avg,
             beer.num_ratings,
             beer.calories,
             beer.ibu,
             beer.abv,
             beer.retired,
             beer.seasonal,
             beer.tags if beer.tags else None,
             beer.description.encode('utf-8') if 'description' in beer.__dict__ else None))
        dbcon.commit() 

    except ps.IntegrityError:
        dbcon.rollback()
        pass 

    cur.close()
    return None

def insert_brewery(dbcon, brewery):
    cur = dbcon.cursor()

    brewery_id = int(brewery.url.split('/')[3])
    try:
        cur.execute("""insert into rate_beer.breweries 
           (brewery_id,
            brewery_name,
            city, 
            country,
            postal_code, 
            state, 
            brewery_type) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (brewery_id,
             brewery.name,
             brewery.city, 
             brewery.country,
             brewery.postal_code,
             brewery.state,
             brewery.type))
        dbcon.commit()
    except ps.IntegrityError:
        dbcon.rollback()
        pass

    cur.close()
    return None


def get_brewery(beer):
    brewery = beer.brewery
    brewery_name = unidecode(brewery.name)
    brewery_name_nice = re.sub('[()%.,/\'#\"]', '', brewery_name.lower().replace(' ', '-'))
    brewery.name = brewery_name_nice
    return brewery


def get_style(beer):
    style = beer.style
    style_id = int(beer.style_url.split('/')[3])
    return (style_id, style)

def insert_style(dbcon, style_tuple):
    cur = dbcon.cursor()
    try:
        cur.execute("""insert into rate_beer.styles (
                style_id, style_name) values (%s, %s)""",
                style_tuple)
           
        dbcon.commit()

    except ps.IntegrityError:
        dbcon.rollback()
        pass

    cur.close()
    return None

def insert_review(dbcon, review, beer_id):
     
    # make that cursor
    cur = dbcon.cursor()

    # get user information to make sure it's in the db
    user_name = review.user_name
    user_location = review.user_location
    
    # put it in the db, and keep user_id for later ;)
    try:
        cur.execute("""INSERT INTO rate_beer.users (user_name, user_location) VALUES (%s, %s)""",
                    (user_name, user_location))
        dbcon.commit()
    except ps.IntegrityError:
        dbcon.rollback()
        pass

    cur.execute("SELECT user_id from rate_beer.users WHERE user_name = %s", (user_name, ))
    user_id = cur.fetchone()[0]

    # put review info into the db 
    try:
        cur.execute("""INSERT INTO rate_beer.reviews (
            beer_id, 
            user_id,
            overall,
            appearance,
            aroma,
            taste,
            palate,
            review_date,
            review_text) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (beer_id, 
             user_id,
             review.overall,
             review.appearance,
             review.aroma,
             review.taste,
             review.palate,
             review.date,
             review.text))
     
        dbcon.commit()
    except ps.IntegrityError:
        dbcon.rollback()
        pass

    cur.close()

    return None

if __name__ == '__main__':

    print "getting started"
    max_beer = 450000
    
    n_ratings = 0

    dbcon = connect_beer_db()
    cur = dbcon.cursor()
    cur.execute("select max(beer_id) from rate_beer.beers;")    
    start_id = cur.fetchone()[0]
    cur.close()
    
    print("starting at beer #{0}".format(start_id))

    for beer_id in range(start_id, max_beer + 1):
    
        try:
            beer = get_beer(beer_id)
        except:
	    continue
 
        brewery = get_brewery(beer)
        style = get_style(beer)
        reviews = beer.get_reviews()
        
        insert_beer(dbcon, beer)
        insert_brewery(dbcon, brewery)
        insert_style(dbcon, style)

        for r in reviews:
            insert_review(dbcon, r, beer_id)
            n_ratings += 1
            if n_ratings % 10000 == 0:
                print "ingested {0} ratings so far".format(n_ratings)
            time.sleep(0.15)



        if beer_id % 500 == 0:
	    print "on beer number {0}, taking a quick nap".format(beer_id)

        sleep_time = time.sleep(1)

   
