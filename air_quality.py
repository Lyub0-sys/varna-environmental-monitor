import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "openaq_varna_8843.csv"

#Създаване на функция за обръщане на формата на датата и часа:
# 2026-06-01T00:00:00+03:00 -> 01.06.2026 00:00

def format_datetime(datetime_text):
    if not datetime_text: # Проверка дали datetime_text е празен.
        return""  # Ако няма дата, връща празен низ (текст)
    date_part, time_part = datetime_text.split("T") # Разделя датата и часа по "T"
    year, month, day = date_part.split("-") # Разделя датата по тирета
    formatted_date = f"{day}.{month}.{year}" #Обръща датата в български формат (ден.месяц.година)
    formatted_time = time_part[:5]  # Взимаме само първите 5 символа (час и минути)
    return f"{formatted_date} {formatted_time}" # Връща форматираната дата и час като низ (текст)

def get_measurements(limit=5): # Функция за извличане на измервания от CSV файл с ограничение на броя на редовете
    measurements = [] # Създава празен списък за съхранение на измерванията.
    with DATA_FILE.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for number, row in enumerate(reader): # Използва enumerate, за да получи номера на реда и самия ред като речник (dictionary).
            if number >= limit:
                break
            
            measurement = {
                'datetime_local': format_datetime(row.get('datetimeLocal', '')), # Взима стойността на 'datetimeLocal' от реда и я форматира с функцията format_datetime. Ако няма стойност, връща празен низ.
                'datetime_utc': format_datetime(row.get('datetimeUtc', '')), # Взима стойността на 'datetimeUtc' от реда и я форматира с функцията format_datetime. Ако няма стойност, връща празен низ.
                'parameter': row.get('parameter', ''), # Взима стойността на 'parameter' от реда. Ако няма стойност, връща празен низ.
                'unit': row.get('unit', ''), # Взима стойността на 'unit' от реда. Ако няма стойност, връща празен низ.
                'value': row.get('value', ''), # Взима стойността на 'value' от реда. Ако няма стойност, връща празен низ.
                'location_name': row.get('location_name', ''), # Взима стойността на 'location_name' от реда. Ако няма стойност, връща празен низ.  
            }
            measurements.append(measurement)
            
    return measurements

def get_parameters():
    parameters = set()
    with DATA_FILE.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            parameter = row.get("parameter", "").strip()
            if parameter:
                parameters.add(parameter)
    return sorted(parameters)

def get_latest_measurements_by_parameter():
    latest_measurements = {}

    with DATA_FILE.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

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

            if value < 0:
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


if __name__ == "__main__":
    parameters = get_parameters()
    print("Available parameters:", parameters)

    measurements = get_measurements()
    for number, measurement in enumerate(measurements):
        print(
            f"{number}: {measurement['datetime_local']} | {measurement['datetime_utc']} " # Извежда номера на измерването и форматираните дати
            f"| {measurement['parameter']} = {measurement['value']} {measurement['unit']}" # Извежда параметъра, стойността и единицата
        )

   # Проверяваме последното валидно измерване за всеки параметър.
    print("\nLatest valid measurements:")

    latest_measurements = get_latest_measurements_by_parameter()

    for parameter in sorted(latest_measurements):
        measurement = latest_measurements[parameter]

        print(
            f"{parameter}: "
            f"{measurement['value']} {measurement['unit']} | "
            f"{measurement['datetime_local']}"
        )        
