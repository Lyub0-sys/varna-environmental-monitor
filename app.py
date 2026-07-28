# Импортираме Flask от инсталираната библиотека flask.
from flask import Flask, render_template

# Импортираме нашия модули за обработка на данните.
import air_quality
import radiation

# Имена на замърсителите на български и английски език.
POLLUTANT_NAMES = {
    "co": "Въглероден оксид / Carbon monoxide (CO)",
    "no2": "Азотен диоксид / Nitrogen dioxide (NO₂)",
    "o3": "Озон / Ozone (O₃)",
    "pm10": "Фини прахови частици / Particulate matter (PM10)",
    "pm25": "Фини прахови частици / Fine particulate matter (PM2.5)",
    "so2": "Серен диоксид / Sulfur dioxide (SO₂)",
}

# Създаваме Flask приложението.
app = Flask(__name__)


# Този route определя какво да се случи при отваряне на началната страница.
@app.route("/")
def index():
    # Вземаме последното валидно измерване за всеки параметър.
    latest_measurements = (
    air_quality.get_current_measurements()
)
    radiation_data = radiation.get_current_radiation()

    # Подготвяме данни за проста графика
    # на текущите стойности на замърсителите.
    chart_measurements = []

    # Намираме най-голямата стойност,
    # за да изчислим ширината на всяка лента.
    max_value = 0

    for measurement in latest_measurements.values():
        value = measurement["value"]

        if value > max_value:
            max_value = value

    # Ако по някаква причина всички стойности са 0,
    # пазим се от деление на нула.
    if max_value == 0:
        max_value = 1

    # Създаваме списък с данни за графиката.
    for parameter, measurement in latest_measurements.items():
        width_percent = (
            measurement["value"] / max_value
        ) * 100

        chart_measurements.append(
            {
                "parameter": parameter,
                "label": POLLUTANT_NAMES.get(
                    parameter,
                    parameter.upper(),
                ),
                "value": measurement["value"],
                "unit": measurement["unit"],
                "width_percent": width_percent,
            }
        )

    # Подготвяме обща информация за станцията и датата на данните.
    station_name = ""
    latest_update = ""

    for measurement in latest_measurements.values():
        station_name = measurement["location_name"]
        latest_update = measurement["datetime_local"]
        break

     # Изпращаме информацията към HTML страницата.
    return render_template(
        "index.html",
        measurements=latest_measurements,
        pollutant_names=POLLUTANT_NAMES,
        station_name=station_name,
        latest_update=latest_update,
        radiation=radiation_data,
        chart_measurements=chart_measurements,
    )



# Стартираме приложението само когато изпълняваме app.py директно.
if __name__ == "__main__":
    app.run(debug=True)