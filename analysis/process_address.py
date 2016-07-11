# -*- coding: utf-8 -*-

import re
import pandas as pd
import numpy as np
from collections import defaultdict
import csv

apps = pd.read_csv('../google_play_apps_tmp.csv', encoding='utf-8')

addressess = apps.address

# replace non word characters (utf-8, so also chinese characters etc) and make everything lowercase
cleaned_addressess = addressess.str.replace('\W', ' ', flags=re.UNICODE).str.lower()

# collect all words in a bag of words with frequency (dict)
words = defaultdict(int)
for address in cleaned_addressess:
    if not pd.isnull(address):
        for word in address.split():
            words[word] += 1

# sort words by frequency of occurrence
words_series = pd.Series(words).sort_values(ascending=False)

# take top 1000 words in address field
top_words = pd.DataFrame(words_series[0:5000], columns=['count'])

# keep the annotation in the file, if regenerating withouth annotation, comment out below 2 lines
top_words_annotated = pd.read_csv('../output/top_words.csv', index_col=0, encoding='utf-8')['country']
top_words = top_words.join(top_words_annotated)

# convert the country annotated dataframe into a list of records [word -> {country: country}]
annotations = top_words[pd.notnull(top_words.country)].to_dict('index')

# write the file to disk
top_words.to_csv('../output/top_words.csv', encoding='utf-8')

# function that converts an address to a country
def tag_country(address):
    for word, value in annotations.iteritems():
        if not pd.isnull(address):
            if word in address:
                return value['country']

# now tag apps with country
apps['country'] = cleaned_addressess.map(tag_country)

# convert num of downloads
apps['min_downloads'] = pd.to_numeric(apps.downloads.str.split('-').str[0].str.replace(',', ''))
apps['max_downloads'] = pd.to_numeric(apps.downloads.str.split('-').str[1].str.replace(',', ''))
apps['average_downloads'] = (apps['min_downloads'] + apps['max_downloads']) / 2

# export in new csv file
apps.to_csv('../output/google_play_with_country.csv', encoding='utf-8',index=False)
