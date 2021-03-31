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
