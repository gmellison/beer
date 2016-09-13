import pymongo
import numpy as np
import pandas as pd
from collections import Counter

beers = pymongo.MongoClient()['beer_db']['beers']
beer_features = ['_id',
                 'style',
                 'abv',
                 'brewery',
                 'calories',
                 'ibu',
                 'mean_rating',
                 'num_ratings',
                 'overall_rating',
                 'style_rating',
                 'seasonal',
                 'tags',
                 'weighted_avg',
                 'url']


# sample a dataframe from the beers collection
df = pd.DataFrame(list(beers.find(limit = 10000,
                                  projection = beer_features)))


# get some information about categorical features -- tags and styles


styles = beers.find(projection = ['style']).distinct('style')
style_counts = Counter(styles)
seasonal_counts = Counter(df['seasonal'])

pd.get_dummies(df['seasonal'], prefix = 'seasonal_')
pd.get_dummies(df['style'], prefix = 'style_'])

def get_tags_dummies(df, tags):
    """makes the dummy matrix for the tags feature -- or more generally
       a feature whose elements are lists
    """
    tag_counts = Counter([t for tags in df.tags for t in tags])
    common_tags = set([tag for tag in tag_counts if tag_counts[tag] > 0.0025 * df.shape[0]])

    map(lambda tag: 1 if tag in df['tags'][100] else 0, common_tags)
    



pd.get_dummies(df['tags'], prefix = 'tag_')





def clean_urls(url):
    url.split('/')[2]

df.brewery_url = df.brewery
df.brewery = map(clean_urls, df.brewery_url)
df.beer_id = map(clean_urls, df.url)
