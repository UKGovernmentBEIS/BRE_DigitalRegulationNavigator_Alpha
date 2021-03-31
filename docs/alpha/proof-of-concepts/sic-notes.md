# SIC Notes

See: https://www.gov.uk/government/publications/standard-industrial-classification-of-economic-activities-sic

## Condensed list used by Companies House

[HTML](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/527619/SIC07_CH_condensed_list_en.csv/preview) |
[CSV](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/527619/SIC07_CH_condensed_list_en.csv)

CSV contains: code,label

Those related to Food prep and retail seem to be between: 56101 - 56302

The categories are pretty broad, e.g. "Take-away food shops and mobile food stands"

## ONS full list

Full lists are here: <https://www.ons.gov.uk/methodology/classificationsandstandards/ukstandardindustrialclassificationofeconomicactivities/uksic2007>

They're a mixture of PDF and Excel files.

There's the [Main Volume PDF](https://www.ons.gov.uk/file?uri=/methodology/classificationsandstandards/ukstandardindustrialclassificationofeconomicactivities/uksic2007/uksic2007webamend8531.pdf) and an [interactive HTML version](https://onsdigital.github.io/dp-classification-tools/standard-industrial-classification/ONS_SIC_hierarchy_view.html). The [data](https://onsdigital.github.io/dp-classification-tools/standard-industrial-classification/data/sicDB.js) for this is in JS which should be easy enough to extract. Has a short description for each classification, plus inclusions/exlusions, e.g.

```javascript
SICmeta['I56101'] = {
  title: 'Licensed restaurants',
  detail:
    'This subclass includes the provision of food services to customers, whether they are served while seated or serve themselves from a display of items. The meals provided are generally for consumption on the premises and alcoholic drinks to accompany the meal are available.',
  includes: [
    'restaurants',
    'cafeterias',
    'fast-food restaurants',
    'restaurant and bar activities connected to transportation (when carried out by separate units)',
  ],
  excludes: ['concession operation of eating facilities, see ##56.29'],
};
```

Food service activities in section I.

To convert the sicDB.js to JSON in the browser, open a JavaScript console and run:

```javascript
codes = [];

for (code in SICmeta) {
  codes.push({
    code: code,
    info: SICmeta[code],
  });
}

JSON.stringify(codes);
```

The resulting JSON string can be copied and saved to a file.

There's sample code to process this JSON and split it up into the different sections, devisions and groups and also to process the text content into lists. See `sample-code/sic_db_json.py`

---

## Code

Added a `sic_codes` app that provides a basic `Code` model tracking the SIC code and label.
The app provides a `import_sic_codes` management command to import the condensed list of SIC codes from Companies House.

```shell
$ ./manage.py import_sic_codes
```
