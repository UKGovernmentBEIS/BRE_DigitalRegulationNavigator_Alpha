# Entity Extraction From Regulator

General issues:

- Finding sources
- Differing formats (HTML, PDF)
- Identifying structure
- Finding content relevant to bussineses
- Extracting non-text content (e.g. tables - loss of info)

Found a couple of example sources to try out on Food.gov.uk:

[Allergen guidance for food businesses](https://www.food.gov.uk/business-guidance/allergen-guidance-for-food-businesses) (HTML)

Main text content found within a single `<article>` tag. Consists of `<h2>` headings followed by numerous paragraphs.

So far pulled out all of the content and used NER to find entities using the [NLTK](https://www.nltk.org/) (`sample-code/nltk_ner_allegen.py`) and [Spacy](https://spacy.io/) (`sample-code/spacy_ner_allegen.py`) toolkits. Also tried finding certain phrases (`sample-code/spacy_phrase_matcher.py`).

[Food Law Practice Guidance](http://fsa.riams.org/connected/ZftGP6vTIF) (PDF, found via [Codes of practice](https://www.food.gov.uk/about-us/food-and-feed-codes-of-practice))

There's a large ToC and many numbered sections and sub-sections. These could be extracted in chunks based on section and sub-sections headings using regexes.

Info relevant to business in section 8.

I've quickly tried extracting a page to text (`sample-code/pdf2text.py`) but it might make sense to convert to HTML first so less formatting is lost (tables etc).

## Code examples

=== "Pipfile"

    ```toml
    [[source]]
    name = "pypi"
    url = "https://pypi.org/simple"
    verify_ssl = true

    [dev-packages]
    black = "==19.10b0"
    flake8 = "*"

    [packages]
    "pdfminer.six" = "*"
    beautifulsoup4 = "*"
    nltk = "*"
    requests = "*"
    spacy = "*"
    spacy-lookups-data = "*"


    [requires]
    python_version = "3.8"
    ```

=== "NLTK"

    ```python
    # nltk_ner_allegen.py
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
    ```

=== "Spacy"

    ```python
    # spacy_ner_allegen.py
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
    ```

=== "Spacy phrase matcher"

    ```python
    # spacy_phrase_matcher.py
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
    ```

=== "PDF2Text"

    ```python
    # pdf2text.py
    import io

    import requests
    from pdfminer.high_level import extract_text

    response = requests.get("http://fsa.riams.org/connected/ZftGP6vTIF")
    response.raise_for_status()

    # See: https://github.com/pdfminer/pdfminer.six
    contents = extract_text(io.BytesIO(response.content), page_numbers=[162])

    print(contents.strip())

    # Could use regex to find headings, something like ^([\d]+\.?)+
    ```

## Specific extraction from [Food and feed law guide PDF](https://www.food.gov.uk/sites/default/files/media/document/food-and-feed-law-guide-july-2020.pdf)

The PDF contains tables of regulations with links and descriptions. Tried extracting these using [Camelot](https://camelot-py.readthedocs.io/en/master/) to extract the tables and [pdftohtml](http://poppler.freedesktop.org) to extract the links (as Camelot strips them). The resulting CSV is then converted to JSON, ready to import using Django's loaddata command.

Sample code (also in `sample-code/extract-regs`):

=== "Instructions"

    1. Create `src` and `dest` folders and copy the PDF to the `src` folder.
    2. Run `python extract_links.py` to create CSV file containing all the links from the PDF (pages 4-24).
    3. Next, run `python extract_regs.py` to create CSV file of the regulations (pages 4-11 only - it currently doesn't work properly past that).
    4. Finally run `python create_fixtures.py` to create JSON file read for use with Django's loaddata command.

=== "Pipfile"

    ```toml
    [[source]]
    name = "pypi"
    url = "https://pypi.org/simple"
    verify_ssl = true

    [dev-packages]
    black = "==19.10b0"
    flake8 = "*"

    [packages]
    beautifulsoup4 = "*"
    camelot-py = {extras = ["cv"], version = "*"}
    pandas = "*"

    [requires]
    python_version = "3.8"
    ```

=== "extract_links.py"

    ```python
    import csv
    import subprocess

    from bs4 import BeautifulSoup

    # Available from: https://www.food.gov.uk/business-guidance/general-food-law?navref=search-global-all-4
    src = "src/food-and-feed-law-guide-july-2020.pdf"

    dest_html = "dest/food-and-feed-law-guide-july-2020.html"
    dest_csv = "dest/food-and-feed-law-guide-july-2020-links.csv"

    first_page = 4
    last_page = 24


    subprocess.run(
        [
            "pdftohtml",
            "-f",
            str(first_page),
            "-l",
            str(last_page),
            "-c",
            "-i",
            "-noframes",
            src,
            dest_html,
        ]
    )

    subprocess.run(["tidy", "-m", "-i", dest_html])


    def strip_whitespace(value: str) -> str:
        value = value.replace("\n", " ")
        return " ".join(value.split())


    with open(dest_html) as f:
        soup = BeautifulSoup(f, "html.parser")

    pages = soup.body.find_all("div")

    links = []

    for page in pages:
        page_num = int(page["id"].replace("page", "").replace("-div", ""))

        for a in page.find_all("a"):
            link_title = strip_whitespace(a.get_text())
            if link_title:
                if a.b:
                    a.b.unwrap()
                links.append((page_num, a["href"], link_title))

    with open(dest_csv, mode="w") as f:
        fieldnames = ["page_number", "url", "title"]

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for link in links:
            writer.writerow({"page_number": link[0], "url": link[1], "title": link[2]})
    ```

=== "extract_regs.py"

    ```python
    import csv

    import camelot
    import pandas as pd

    src = "src/food-and-feed-law-guide-july-2020.pdf"
    links_src = "dest/food-and-feed-law-guide-july-2020-links.csv"

    links = pd.read_csv(links_src)

    tables = camelot.read_pdf(
        src,
        pages="4,5,6,7,8,9,10,11",
        strip_text="\n",
    )


    print("Total tables extracted:", tables.n)


    def strip_whitespace(value: str) -> str:
        return " ".join(value.split())


    def match_links(arg, *args, **kwargs):
        title = arg[0].strip()
        description = strip_whitespace(arg[1])

        if not title or title == "Regulation":
            return [None, None, None, None]  # This well be dropped by .dropna() below.

        for index, link_row in links.iterrows():
            link_title = link_row["title"]

            if title.endswith(link_title):
                link_url = link_row["url"]

                links.drop([index])

                return [
                    title.replace(link_title, "").strip(),
                    link_title,
                    link_url,
                    description,
                ]


    processed = []

    for table in tables:
        report = table.parsing_report
        print(report)

        result = table.df.apply(match_links, axis=1, result_type="expand")
        result = result.dropna(how="all", axis=0)

        processed.append(result)


    pd.concat(processed).to_csv(
        "dest/food-and-feed-law-guide-july-2020.csv",
        header=False,
        index=True,
        quoting=csv.QUOTE_NONNUMERIC,
    )
    ```

=== "create_fixtures.py"

    ``` python
    import csv
    import json
    from datetime import datetime, timezone

    src = "dest/food-and-feed-law-guide-july-2020.csv"
    dest = "dest/regulations.json"

    fixtures = []
    now = datetime.now(timezone.utc).isoformat()


    with open(src) as f:
        reader = csv.reader(f)
        for index, row in enumerate(reader):

            fixtures.append(
                {
                    "model": "regulations.regulation",
                    "pk": index + 1,
                    "fields": {
                        "name": row[1],
                        "url": row[3],
                        "description": row[4],
                        "inserted_at": now,
                        "updated_at": now,
                    },
                }
            )


    with open(dest, "w") as f:
        json.dump(fixtures, f, indent=2)
    ```
