#! /bin/sh
# borrowed and modified from here: http://dba.stackexchange.com/questions/57058/how-do-i-use-an-ispell-dictionary-with-postgres-text-search
cd /usr/share/postgresql/9.5/tsearch_data

wget https://src.chromium.org/viewvc/chrome/trunk/deps/third_party/hunspell_dictionaries/en_US.dic
wget https://src.chromium.org/viewvc/chrome/trunk/deps/third_party/hunspell_dictionaries/en_US.dic_delta
wget https://src.chromium.org/viewvc/chrome/trunk/deps/third_party/hunspell_dictionaries/en_US.aff -O en_us.affix


# Remove first line
sed -i 1d en_US.dic

# Concat the dic and dic_delta, sort alphabetically and remove the leading blank line (leaves the ending newline intact)
cat en_US.dic en_US.dic_delta | sort > en_us.dict
sed -i 1d en_us.dict

# Set permissions
chown -R postgres:postgres *

sudo -u postgres psql -c "CREATE TEXT SEARCH DICTIONARY ispell_en_us (template  = ispell, dictfile = en_us, afffile = en_us, stopwords = english);"

# Clean up source files
rm en_US*
