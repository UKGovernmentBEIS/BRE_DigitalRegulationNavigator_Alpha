from pprint import pprint

import requests
from bs4 import BeautifulSoup
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.chunk import tree2conlltags

# See: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#get-text
# See: https://nlpforhackers.io/named-entity-extraction/

"""
Install data:
>>> import nltk
>>> nltk.download("punkt")
>>> nltk.download("averaged_perceptron_tagger")
>>> nltk.download("maxent_ne_chunker")
>>> nltk.download("words")
"""

response = requests.get(
    "https://www.food.gov.uk/business-guidance/allergen-guidance-for-food-businesses"
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
article = soup.find("article")
text = article.getText()

tokens = word_tokenize(text)
tags = pos_tag(tokens)
ne_tree = ne_chunk(tags)
iob_tagged = tree2conlltags(ne_tree)

pprint(iob_tagged)
