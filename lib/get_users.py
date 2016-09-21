import bs4 as bs
import requests
import pymongo
import selenium.webdriver as webdriver
import time
from math import ceil
import scipy.stats
from pyvirtualdisplay import Display


def get_browser():
    browser = webdriver.Firefox()
    time.sleep(2)
    return browser


def get_user_reviews(user_i, browser):
    """returns a dict of user information including scores of rated beers
    """
    user = {'user_id': user_i,
            'ratings': []}
    base_url = 'http://www.ratebeer.com/user/{0}/'.format(user_i)

    # first get number of total beers rated for user i: need this to know how many pages of reviews to scrape (@ 50 reviews/page)
    soup = bs.BeautifulSoup(requests.get(base_url).content)
    nratings = soup.findAll('div', 'stat-value', 'beer-ratings')[0].text

    if nratings == 0:
        return None

    n_pages = int(ceil(int(nratings) / 50.0))

    def page_url(page_i):
        return base_url + 'beer-ratings/{0}/'.format(page_i)

    for i in range(1, n_pages):
        page = page_url(i)

        # wrap all browser stuff in a try except since the
        # selenium session dies with no recovery once in a while?
        # go to the statsTable on the rating page
        try:
            browser.get(page)
            table = browser.find_element_by_id('statsWindow').find_element_by_class_name('table')
            rows = table.find_elements_by_class_name('accordion-toggle')
        except:
            browser = get_browser()
            get_user_reviews(user_i, browser)

        for row in rows:
            beer_url = row.find_element_by_tag_name('a').get_attribute('href')
            beer_id = beer_url.split('/')[5]
            rating = row.find_element_by_tag_name('b').text
            user['ratings'].append({'beer': beer_id, 'rating': rating})
    return user

if __name__ == '__main__':
    
    display = Display(visible=0, size=(800, 600))
    display.start()

    client = pymongo.MongoClient()
    db = client['beer_db']
    user_collection = db['users']
    
    u = 0

    browser = get_browser()
     
    for user_id in range(1, 427405):

        sleep_time = scipy.stats.expon.rvs() * 3.0
        time.sleep(sleep_time)
        user_reviews = get_user_reviews(user_id, browser)

        user_collection.insert_one(user_reviews)
        u += 1
        if u % 500 == 0:
            print 'ingested {0} users'.format(u)



