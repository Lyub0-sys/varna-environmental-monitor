import re

import requests
from bs4 import BeautifulSoup


# Official website
RADIATION_URL = (
    "https://bnra.bg/bg/byuletin-za-gama-fona/"
)


def get_live_radiation():
    """
    Извлича последната публикувана стойност
    за гама-фона във Варна от сайта на АЯР.
    """

    # html
    response = requests.get(
        RADIATION_URL,
        timeout=30,
    )

    # if HTTP error
    response.raise_for_status()

    # converts
    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    varna_row = None
    updated_row = None

    
    for row in soup.find_all("tr"):
        cells = [
            cell.get_text(" ", strip=True)
            for cell in row.find_all(["th", "td"])
        ]

        if not cells:
            continue

        
        if cells[0].casefold() == "варна":
            varna_row = cells

         
            varna_table = row.find_parent("table")

            if varna_table is not None:
               
                for table_row in varna_table.find_all("tr"):
                    table_cells = [
                        cell.get_text(" ", strip=True)
                        for cell in table_row.find_all(
                            ["th", "td"]
                        )
                    ]

                    if (
                        table_cells
                        and "Актуални към" in table_cells[0]
                    ):
                        updated_row = table_cells
                        break

            break

    
    if not varna_row or len(varna_row) < 2:
        raise RuntimeError(
            "The Varna radiation row was not found."
        )

    # value of 10 microsivert per hour
    value_text = varna_row[1]

    
    value_match = re.search(
        r"\d+(?:[.,]\d+)?",
        value_text,
    )

    if value_match is None:
        raise RuntimeError(
            "The Varna radiation value was not found."
        )

   
    value = float(
        value_match.group().replace(",", ".")
    )
    if updated_row:
        updated_text = " ".join(updated_row)

        time_match = re.search(
            r"\d{1,2}:\d{2}",
            updated_text,
        )

        date_match = re.search(
            r"\d{2}\.\d{2}\.\d{4}",
            updated_text,
        )

        if time_match and date_match:
            updated_at = (
                f"{time_match.group()} h, "
                f"{date_match.group()}"
            )
        else:
            updated_at = updated_text

    else:
        updated_at = "Not specified"
    return {
        "available": True,
        "city": "Варна / Varna",
        "value": value,
        "unit": "µSv/h",
        "updated_at": updated_at,
        "source_name": "АЯР / BNRA",
        "source_url": RADIATION_URL,
    }


def get_current_radiation():
    """
    Връща текущите данни за гама-фона.

    При проблем сайтът продължава да работи,
    но показва, че данните временно не са налични.
    """

    try:
        radiation_data = get_live_radiation()

        print("Radiation source: Live BNRA website")

        return radiation_data

    except (
        requests.RequestException,
        RuntimeError,
        TypeError,
        ValueError,
    ) as error:
        print(
            "BNRA radiation data unavailable. "
            f"Reason: {error}"
        )

        return {
            "available": False,
            "city": "Варна / Varna",
            "value": None,
            "unit": "µSv/h",
            "updated_at": "",
            "source_name": "АЯР / BNRA",
            "source_url": RADIATION_URL,
        }


if __name__ == "__main__":
    radiation = get_current_radiation()

    print("\nRadiation data:")
    print(radiation)