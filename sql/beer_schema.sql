DROP SCHEMA IF EXISTS rate_beer CASCADE;
CREATE SCHEMA rate_beer;

DROP TABLE IF EXISTS rate_beer.beers;
CREATE TABLE rate_beer.beers (
  beer_id integer PRIMARY KEY,
  beer_name text,
  brewery_id integer,
  style_id integer,
  overall_rating real,
  mean_rating real,
  style_rating real,
  weighted_avg real,
  abv real,
  num_ratings integer,
  calories real,
  ibu real,
  retired boolean,
  seasonal text,
  tags text[],
  description text
);

DROP TABLE IF EXISTS rate_beer.styles;
CREATE TABLE rate_beer.styles (
  style_id integer PRIMARY KEY,
  style_name text 
);

DROP TABLE IF EXISTS rate_beer.users;
CREATE TABLE rate_beer.users (
  user_id SERIAL PRIMARY KEY,
  user_name text UNIQUE, 
  user_location text 
);

DROP TABLE IF EXISTS rate_beer.reviews;
CREATE TABLE rate_beer.reviews (
  beer_id integer,
  user_id integer,
  overall integer,
  appearance integer,
  aroma integer,
  taste integer,
  palate integer,
  review_date date,
  review_text text,
  PRIMARY KEY (beer_id, user_id)
);

DROP TABLE IF EXISTS rate_beer.breweries;
CREATE TABLE rate_beer.breweries (
  brewery_id integer PRIMARY KEY,
  brewery_name text,
  city text,
  country text,
  postal_code text, 
  state text,
  brewery_type text
);
