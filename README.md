# Varna Environmental Monitor

A bilingual Flask web application for displaying environmental data from Varna, Bulgaria.

Двуезично Flask уеб приложение за показване на данни за околната среда във Варна, България.

## Current version / Текуща версия

The application reads air-quality measurements from a local OpenAQ CSV dataset and displays the latest valid measurement for each pollutant.

Приложението прочита измервания за качеството на въздуха от локален OpenAQ CSV файл и показва последното валидно измерване за всеки замърсител.

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
├── project_roadmap.py
├── README.md
└── .gitignore