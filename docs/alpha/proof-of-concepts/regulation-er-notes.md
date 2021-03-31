# Entity Extraction From legislation.gov.uk

Has developer zone! https://www.legislation.gov.uk/developer

Content available in XML, HTML, RDF/XML and Atom

[XML format](https://www.legislation.gov.uk/developer/formats/xml)

[URI scheme](https://www.legislation.gov.uk/developer/uris)

## API Searching

<http://www.legislation.gov.uk/id?title=Food+Safety+Act+1990>

If matching doc found you're redirected otherwise you're shown a list of possible matches. Searching always returns HTML (ignores content-type header).

## Specific docs

<http://www.legislation.gov.uk/id/{type}/{year}/{number}[/{section}][/data.{ext}]>

The {type} is short code, e.g ukpga = UK Public General Acts, asp = Acts of the Scottish Parliament

To get the Food Safety Act 1990 contents in XML you can do this:

<https://www.legislation.gov.uk/ukpga/1990/16/contents/data.xml>

To get just a section:

<https://www.legislation.gov.uk/ukpga/1990/16/section/18/data.xml>

### Extent (country)

Top-level element in XML doc has a RestrictExtent attribute which contains the countries the doc applies to, e.g.

    RestrictExtent="E+W+S+N.I."

Can also append {country} to URI to filter, e.g.

<https://www.legislation.gov.uk/ukpga/1990/16/contents/scotland/data.xml>

<https://www.legislation.gov.uk/ukpga/1990/16/section/18/scotland/data.xml>

## Web Searching

Aside from the Developer stuff they also have a web search you can use to find specific areas of legislation, e.g. to search primary and secondary legislation related "Licensed restaurants":

<https://www.legislation.gov.uk/primary+secondary?text=Licensed+restaurants>

You get back a fair bit, some of the older results are PDFs of low quality scans! e.g.

<https://www.legislation.gov.uk/uksi/1982/739/contents/made>

Searching for specific SIC codes doesn't return any results. Searching for their labels is hit and miss, e.g. "Licensed restaurants" does, "Take away food shops and mobile food stands" does not.

## [Defralex](https://www.legislation.gov.uk/defralex)

Defralex is part of legislation.gov.uk but lets you search Defra related legislation with far more options than the main site. You can limit by **category**, **regulator** and **subject**.

FSA related docs here, including what looks like docs related to businesses:

All:

<https://www.legislation.gov.uk/defralex/lists?regulator=http://www.legislation.gov.uk/id/publicbody/fsa>

Plans / Guidance / Assessments / Information / Schemes:

<https://www.legislation.gov.uk/defralex/lists?regulator=http://www.legislation.gov.uk/id/publicbody/fsa&content=http://defra-lex.legislation.gov.uk/id/activity/plans-guidance-assessments-information-schemes>

Notice / Order / Direction / Declaration:

<https://www.legislation.gov.uk/defralex/lists?regulator=http://www.legislation.gov.uk/id/publicbody/fsa&content=http://defra-lex.legislation.gov.uk/id/activity/notice-order-direction-declaration>

The URLs above have a `regulator` param which is itself an URL that looks like it could be used to filter all of the regulations by the regulator. It returns a 404 if used on it's own though! (referer check? internal param - just looks like an URL?)

<https://www.legislation.gov.uk/id/publicbody/fsa>
