import json
import re

from bs4 import BeautifulSoup

code_pattern = re.compile("(?P<char>[A-Z])(?P<code>[0-9]*)(?P<placeholder>x+)")
ref_pattern = re.compile("##([0-9]+).?([0-9]+)?")


def clean(value: str) -> list:
    doc = BeautifulSoup(value, "html.parser")
    return [clean_ref(value) for value in doc.stripped_strings]


def clean_ref(value: str) -> str:
    return ref_pattern.sub(r"#\1\2", value)


def hoist(values: list) -> list:
    return [value[0] if len(value) == 1 else [value[0], value[1:]] for value in values]


with open("sicDB.json", "r") as f:
    data = json.load(f)


results = []

section = None
division = None
group = None

for row in data:
    match = code_pattern.search(row["code"])
    if match:
        info = row["info"]
        title = info["title"].strip().capitalize()

        code = None
        description = None
        includes = None
        excludes = None

        if match.group("char") and not match.group("code"):
            section = match.group("char")
            division = None
            group = None
        else:
            code = match.group("code")
            length = len(code)
            code = int(code)

            if length == 2:
                division = code
            elif length == 3:
                group = code

        if "detail" in info:
            description = clean(info["detail"])
            description = "".join(description)

        if "includes" in info:
            includes = [clean(value) for value in info["includes"]]
            includes = hoist(includes)

        if "excludes" in info:
            excludes = [clean(value) for value in info["excludes"]]
            excludes = hoist(excludes)

        results.append(
            {
                "section": section,
                "division": division,
                "group": group,
                "code": code,
                "title": title,
                "description": description,
                "includes": includes,
                "excludes": excludes,
            }
        )


with open("sic_db.json", "w") as f:
    f.write(json.dumps(results, indent=2))
