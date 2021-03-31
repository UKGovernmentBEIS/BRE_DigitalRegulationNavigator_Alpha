import requests
import spacy
from bs4 import BeautifulSoup
from spacy.pipeline import EntityRuler

response = requests.get(
    "https://www.food.gov.uk/business-guidance/allergen-guidance-for-food-businesses"
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
article = soup.find("article")
text = article.getText()

nlp = spacy.load("en_core_web_sm")

# Add custom patterns
patterns = [
    {"label": "ORG", "pattern": "FSA"},
    {"label": "CUSTOM", "pattern": "safety"},
]
ruler = EntityRuler(nlp)
ruler.add_patterns(patterns)
nlp.add_pipe(ruler)

doc = nlp(text)

print("Sentences:")
for i, sent in enumerate(doc.sents):
    print("{:d}: {}".format(i, sent.text.strip()))
print("\n")

print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("\n")

print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
print("\n")

print("Named entities, phrases and concepts:")
# Key: https://spacy.io/api/annotation#named-entities
for entity in doc.ents:
    print(entity.text, entity.label_)

# Uncomment to view visualisation (starts a local server)
# spacy.displacy.serve(doc, style="ent")
