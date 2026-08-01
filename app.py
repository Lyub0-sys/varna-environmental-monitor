# Import Flask from the installed flask library.
from flask import Flask, render_template

# Import the project modules responsible for retrieving
# and processing environmental data.
import air_quality
import radiation


# English display names for the monitored air pollutants.
POLLUTANT_NAMES = {
    "co": "Carbon monoxide (CO)",
    "no2": "Nitrogen dioxide (NO₂)",
    "o3": "Ozone (O₃)",
    "pm10": "Particulate matter (PM10)",
    "pm25": "Fine particulate matter (PM2.5)",
    "so2": "Sulfur dioxide (SO₂)",
}


# Pollutant-specific WHO reference values and averaging periods.
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


# Create the Flask application.
app = Flask(__name__)


# Define what happens when the home page is accessed.
@app.route("/")
def index():
    # Retrieve the latest valid air-quality measurements.
    latest_measurements = (
        air_quality.get_current_measurements()
    )

    # Retrieve the latest available gamma dose-rate data.
    radiation_data = radiation.get_current_radiation()

    # Prepare chart data by comparing each measurement
    # with its pollutant-specific WHO reference value.
    chart_measurements = []

    for parameter, measurement in latest_measurements.items():
        reference = POLLUTANT_REFERENCES.get(parameter)

        # Skip parameters without a defined reference value.
        if reference is None:
            continue

        value = measurement["value"]
        reference_value = reference["value"]

        # Calculate the measurement as a percentage
        # of the corresponding WHO reference value.
        reference_percent = (
            value / reference_value
        ) * 100

        # Limit the visual progress bar to 100%.
        # The actual percentage remains visible as text.
        progress_value = min(reference_percent, 100)

        # Use orange when the value exceeds 75%
        # of the selected reference value.
        # This is not an official AQI classification.
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

    # Prepare general station and timestamp information.
    station_name = ""
    latest_update = ""

    for measurement in latest_measurements.values():
        station_name = measurement["location_name"]
        latest_update = measurement["datetime_local"]
        break

    # Send all prepared data to the HTML template.
    return render_template(
    "index.html",
    measurements=latest_measurements,
    pollutant_names=POLLUTANT_NAMES,
    station_name=station_name,
    latest_update=latest_update,
    air_quality_source_url=air_quality.OPENAQ_SOURCE_URL,
    radiation=radiation_data,
    chart_measurements=chart_measurements,
)


# Start the development server only when app.py
# is executed directly.
if __name__ == "__main__":
    app.run(debug=True)