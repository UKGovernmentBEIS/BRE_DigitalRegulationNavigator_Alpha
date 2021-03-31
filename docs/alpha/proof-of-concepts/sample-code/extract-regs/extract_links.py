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
