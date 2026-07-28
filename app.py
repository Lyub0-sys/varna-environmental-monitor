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
POLLUTANT_REFERENCES = {
    "co": {
        "value": 4000.0,
        "period": "24 h",
    },
    "no2": {
        "value": 25.0,
        "period": "24 h",
    },
    "o3": {
        "value": 100.0,
        "period": "8 h",
    },
    "pm10": {
        "value": 45.0,
        "period": "24 h",
    },
    "pm25": {
        "value": 15.0,
        "period": "24 h",
    },
    "so2": {
        "value": 40.0,
        "period": "24 h",
    },
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

   # Подготвяме всеки замърсител спрямо
    # неговата собствена WHO референтна стойност.
    chart_measurements = []

    for parameter, measurement in latest_measurements.items():
        reference = POLLUTANT_REFERENCES.get(parameter)

        # Пропускаме параметъра, ако няма зададена
        # референтна стойност.
        if reference is None:
            continue

        value = measurement["value"]
        reference_value = reference["value"]

        # Изчисляваме колко процента от
        # референтната стойност представлява измерването.
        reference_percent = (
            value / reference_value
        ) * 100

        # Лентата не може да бъде по-дълга от 100%.
        # Реалният процент обаче остава видим като текст.
        progress_value = min(reference_percent, 100)

        # Цветовете показват близостта до референцията.
        # Това не е официална AQI класификация.
        if reference_percent > 75:
            status = "warning"

    
        else:
            status = "normal"

        chart_measurements.append(
            {
                "parameter": parameter,
                "label": POLLUTANT_NAMES.get(
                    parameter,
                    parameter.upper(),
                ),
                "value": value,
                "unit": measurement["unit"],
                "reference_value": reference_value,
                "reference_period": reference["period"],
                "reference_percent": reference_percent,
                "progress_value": progress_value,
                "status": status,
            }
        )

    # Подготвяме обща информация за станцията и датата на данните.
    station_name = ""
    latest_update = ""

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