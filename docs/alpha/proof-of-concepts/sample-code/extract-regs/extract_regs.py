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
