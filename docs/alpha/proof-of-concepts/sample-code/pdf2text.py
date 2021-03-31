import io

import requests
from pdfminer.high_level import extract_text

response = requests.get("http://fsa.riams.org/connected/ZftGP6vTIF")
response.raise_for_status()

# See: https://github.com/pdfminer/pdfminer.six
contents = extract_text(io.BytesIO(response.content), page_numbers=[162])

print(contents.strip())

# Could use regex to find headings, something like ^([\d]+\.?)+
