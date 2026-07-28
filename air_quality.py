import csv
import math
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


# Намираме основната папка на проекта.
BASE_DIR = Path(__file__).resolve().parent

# Създаваме пълния път до локалния CSV файл.
DATA_FILE = BASE_DIR / "data" / "openaq_varna_8843.csv"

# Създаваме пълния път до защитения .env файл.
ENV_FILE = BASE_DIR / ".env"

# Зареждаме настройките от .env файла.
load_dotenv(ENV_FILE)


# OpenAQ идентификатор на станцията във Варна.
OPENAQ_LOCATION_ID = 8843

# Име на станцията, което показваме в страницата.
STATION_NAME = "AMS SOU Angel Kanchev-Varna"

# Замърсителите, които показваме в първата версия.
TARGET_PARAMETERS = {
    "co",
    "no2",
    "o3",
    "pm10",
    "pm25",
    "so2",
}


def format_datetime(datetime_text):
    """Преобразува OpenAQ дата в по-удобен формат."""

    if not datetime_text:
        return ""

    try:
        date_part, time_part = datetime_text.split("T", 1)

        year, month, day = date_part.split("-")

        formatted_date = f"{day}.{month}.{year}"
        formatted_time = time_part[:5]

        return f"{formatted_date} {formatted_time}"

    except ValueError:
        # Ако форматът е неочакван, връщаме оригиналния текст.
        return datetime_text


def get_measurements(limit=5):
    """Връща първите няколко измервания от локалния CSV."""

    measurements = []

    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for number, row in enumerate(reader):
            if number >= limit:
                break

            measurement = {
                "datetime_local": format_datetime(
                    row.get("datetimeLocal", "")
                ),
                "datetime_utc": format_datetime(
                    row.get("datetimeUtc", "")
                ),
                "parameter": row.get("parameter", ""),
                "unit": row.get("unit", ""),
                "value": row.get("value", ""),
                "location_name": row.get("location_name", ""),
            }

            measurements.append(measurement)

    return measurements


def get_parameters():
    """Връща сортиран списък с наличните CSV параметри."""

    parameters = set()

    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            parameter = row.get("parameter", "").strip()

            if parameter:
                parameters.add(parameter)

    return sorted(parameters)


def get_latest_measurements_by_parameter():
    """
    Намира последното валидно измерване за всеки параметър
    от локалния CSV файл.
    """

    latest_measurements = {}

    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            parameter = row.get("parameter", "").strip()
            datetime_utc = row.get("datetimeUtc", "").strip()
            value_text = row.get("value", "").strip()

            if not parameter or not datetime_utc or not value_text:
                continue

            try:
                value = float(value_text)

            except ValueError:
                continue

            # Пропускаме отрицателни, безкрайни и NaN стойности.
            if value < 0 or not math.isfinite(value):
                continue

            if (
                parameter not in latest_measurements
                or datetime_utc
                > latest_measurements[parameter]["datetime_utc_raw"]
            ):
                latest_measurements[parameter] = {
                    "datetime_local": format_datetime(
                        row.get("datetimeLocal", "")
                    ),
                    "datetime_utc": format_datetime(datetime_utc),
                    "datetime_utc_raw": datetime_utc,
                    "value": value,
                    "unit": row.get("unit", ""),
                    "location_name": row.get("location_name", ""),
                }

    return latest_measurements


def get_live_measurements():
    """
    Получава последните измервания от OpenAQ API
    и ги преобразува във формат, подходящ за Flask.
    """

    # Получаваме API ключа безопасно от .env.
    api_key = os.getenv("OPENAQ_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAQ_API_KEY is missing.")

    headers = {
        "X-API-Key": api_key
    }

    latest_url = (
        "https://api.openaq.org/v3/locations/"
        f"{OPENAQ_LOCATION_ID}/latest"
    )

    sensors_url = (
        "https://api.openaq.org/v3/locations/"
        f"{OPENAQ_LOCATION_ID}/sensors"
    )

    # Получаваме последните стойности.
    latest_response = requests.get(
        latest_url,
        headers=headers,
        timeout=30,
    )

    latest_response.raise_for_status()

    # Получаваме информацията за сензорите.
    sensors_response = requests.get(
        sensors_url,
        headers=headers,
        timeout=30,
    )

    sensors_response.raise_for_status()

    latest_data = latest_response.json()
    sensors_data = sensors_response.json()

    latest_results = latest_data.get("results", [])
    sensor_results = sensors_data.get("results", [])

    if not latest_results:
        raise RuntimeError("OpenAQ returned no latest measurements.")

    if not sensor_results:
        raise RuntimeError("OpenAQ returned no sensor information.")

    # Създаваме връзка:
    # sensor ID → parameter name и unit.
    sensor_map = {}

    for sensor in sensor_results:
        parameter_data = sensor.get("parameter", {})

        sensor_id = sensor.get("id")
        parameter_name = (
            parameter_data.get("name", "")
            .strip()
            .lower()
        )
        unit = parameter_data.get("units", "")

        if sensor_id is None or not parameter_name:
            continue

        sensor_map[sensor_id] = {
            "parameter": parameter_name,
            "unit": unit,
        }

    live_measurements = {}

    # Свързваме всяка последна стойност
    # с информацията за нейния сензор.
    for result in latest_results:
        sensor_id = result.get("sensorsId")
        sensor_info = sensor_map.get(sensor_id, {})

        parameter = sensor_info.get("parameter", "")
        unit = sensor_info.get("unit", "")

        # Пропускаме NO и всички други непланирани параметри.
        if parameter not in TARGET_PARAMETERS:
            continue

        value = result.get("value")

        try:
            value = float(value)

        except (TypeError, ValueError):
            continue

        if value < 0 or not math.isfinite(value):
            continue

        datetime_data = result.get("datetime", {})

        if not isinstance(datetime_data, dict):
            continue

        datetime_local_raw = str(
            datetime_data.get("local", "")
        ).strip()

        datetime_utc_raw = str(
            datetime_data.get("utc", "")
        ).strip()

        if not datetime_utc_raw:
            continue

        measurement = {
            "datetime_local": format_datetime(
                datetime_local_raw
            ),
            "datetime_utc": format_datetime(
                datetime_utc_raw
            ),
            "datetime_utc_raw": datetime_utc_raw,
            "value": value,
            "unit": unit,
            "location_name": STATION_NAME,
        }

        # Ако има повече от една стойност за параметъра,
        # запазваме най-новата.
        if (
            parameter not in live_measurements
            or datetime_utc_raw
            > live_measurements[parameter]["datetime_utc_raw"]
        ):
            live_measurements[parameter] = measurement

    missing_parameters = (
        TARGET_PARAMETERS - set(live_measurements)
    )

    if missing_parameters:
        missing_text = ", ".join(sorted(missing_parameters))

        raise RuntimeError(
            "OpenAQ is missing required parameters: "
            f"{missing_text}"
        )

    return live_measurements


def get_current_measurements():
    """
    Връща live OpenAQ данните.

    Ако API заявката се провали, използва локалния CSV
    като резервен източник.
    """

    try:
        measurements = get_live_measurements()

        print("Data source: Live OpenAQ API")

        return measurements

    except (
        requests.RequestException,
        RuntimeError,
        TypeError,
        ValueError,
    ) as error:
        print(
            "OpenAQ unavailable. "
            f"Using local CSV fallback. Reason: {error}"
        )

        return get_latest_measurements_by_parameter()


if __name__ == "__main__":
    current_measurements = get_current_measurements()

    print("\nCurrent valid measurements:")

    for parameter in sorted(current_measurements):
        measurement = current_measurements[parameter]

        print(
            f"{parameter}: "
            f"{measurement['value']} "
            f"{measurement['unit']} | "
            f"{measurement['datetime_local']}"
        )