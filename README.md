# Varna Environmental Monitor

A bilingual Flask web application that retrieves, validates and visualizes environmental data for Varna, Bulgaria.

The application integrates:

- live air-quality measurements from the OpenAQ API;
- gamma dose-rate data published by the Bulgarian Nuclear Regulatory Agency;
- pollutant-specific reference visualizations;
- bilingual Bulgarian/English presentation;
- validation and filtering of invalid measurements.

## Main technologies

- Python 3.11
- Flask
- Requests
- BeautifulSoup
- OpenAQ API
- Jinja templates
- HTML and CSS
- Jupyter Notebook
- Git and GitHub

## Scientific limitation

The application displays the latest available air-quality measurements. These instantaneous values are compared indicatively with health reference values whose official averaging periods may be 8 or 24 hours.

The visualization therefore does not represent an official air-quality index or a confirmed legal exceedance.
## Displayed pollutants / Показвани замърсители

- Carbon monoxide / Въглероден оксид — CO
- Nitrogen dioxide / Азотен диоксид — NO₂
- Ozone / Озон — O₃
- Particulate matter / Фини прахови частици — PM10
- Fine particulate matter / Фини прахови частици — PM2.5
- Sulfur dioxide / Серен диоксид — SO₂

## Current features / Текущи функционалности

- CSV data reading with `csv.DictReader`
- Air-quality value validation
- Filtering of negative and invalid measurements
- Selection of the latest valid measurement for each pollutant
- Bulgarian date and time formatting
- Flask web application
- Jinja HTML templates
- Shared `base.html` template
- Responsive basic CSS layout
- Bulgarian and English pollutant names
- Display of station name and actual data timestamp

## Project structure / Структура на проекта

```text
varna_environment_monitor/
├── data/
│   └── openaq_varna_8843.csv
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   └── index.html
├── air_quality.py
├── app.py
├── ExploreOpenAQ.ipynb
├── README.md
└── .gitignore