import requests
import spacy
from bs4 import BeautifulSoup
from spacy.matcher import PhraseMatcher

response = requests.get(
    "https://www.food.gov.uk/business-guidance/allergen-guidance-for-food-businesses"
)
response.raise_for_status()


soup = BeautifulSoup(response.text, "html.parser")
article = soup.find("article")
text = article.getText()

nlp = spacy.load("en_core_web_sm")
matcher = PhraseMatcher(nlp.vocab)
matcher.add("SAFETY", None, nlp("safety"))

doc = nlp(text)
matches = matcher(doc)

# returns list of (match_id, start, end) tuples
for match_id, start, end in matches:
    print("{} ({:d}-{:d})".format(nlp.vocab.strings[match_id], start, end))
