DROP TABLE IF EXISTS beers;
CREATE TABLE beers (
  beer_id integer,
  beer_name varchar(20),
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
  seasonal boolean,
  time_inserted timestamp,
  tags varchar(10)[],
  description text
);

DROP TABLE IF EXISTS styles;
CREATE TABLE STYLES (
  stlye_id integer,
  style_name varchar(15)
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  user_id integer,
  user_name varchar(20),
  user_location varchar(20)
);


DROP TABLE IF EXISTS reviews;
CREATE TABLE reviews (
  beer_id integer,
  user_id integer,
  overall integer,
  appearance integer,
  aroma integer,
  taste integer,
  review_date date,
  review_text text
);

DROP TABLE IF EXISTS breweries;
CREATE TABLE breweries (
  brewery_name varchar(30),
  brewery_id integer,
  city varchar(20),
  country varchar(15),
  postal_code varchar(15),
  state varchar(12),
  brewery_type varchar(10)
);
