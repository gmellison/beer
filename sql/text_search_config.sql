CREATE TEXT SEARCH CONFIGURATION rate_beer.btc (COPY = pg_catalog.english);

CREATE TEXT SEARCH DICTIONARY rate_beer.all_stop_dict (
  TEMPLATE = pg_catalog.simple,
  STOPWORDS = all_stopwords
);

ALTER TEXT SEARCH CONFIGURATION rate_beer.btc 
  DROP MAPPING FOR numword, int, float, sfloat, email, url, hword_part;

ALTER TEXT SEARCH CONFIGURATION rate_beer.btc 
  ALTER MAPPING FOR asciiword WITH english_stem, 
    german_stem,
    norwegian_stem,
    french_stem,
    italian_stem,
    spanish_stem,
    swedish_stem,
    russian_stem,
    danish_stem, 
    dutch_stem,
    rate_beer.all_stop_dict,
    finnish_stem;

SET default_text_search_config = 'rate_beer.btc';
