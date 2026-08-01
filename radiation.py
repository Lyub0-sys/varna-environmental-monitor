import re

import requests
from bs4 import BeautifulSoup


# Official Bulgarian Nuclear Regulatory Agency page
# containing published gamma dose-rate measurements.
RADIATION_URL = (
    "https://bnra.bg/bg/byuletin-za-gama-fona/"
)

# These Bulgarian labels are required for parsing
# the Bulgarian-language source page.
VARNA_LABEL_BG = "варна"
UPDATED_LABEL_BG = "Актуални към"


def get_live_radiation():
    """
    Retrieve the latest published gamma dose-rate value
    for Varna from the official BNRA website.
    """

    # Request the official BNRA webpage.
    response = requests.get(
        RADIATION_URL,
        timeout=30,
    )

    # Raise an exception for unsuccessful HTTP responses.
    response.raise_for_status()

    # Parse the returned HTML document.
    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    varna_row = None
    updated_row = None

    # Search all table rows for the row containing Varna.
    for row in soup.find_all("tr"):
        cells = [
            cell.get_text(" ", strip=True)
            for cell in row.find_all(["th", "td"])
        ]

        if not cells:
            continue

        if cells[0].casefold() == VARNA_LABEL_BG:
            varna_row = cells

            # Find the table containing the Varna row.
            varna_table = row.find_parent("table")

            if varna_table is not None:
                # Search the same table for the publication
                # date and time.
                for table_row in varna_table.find_all("tr"):
                    table_cells = [
                        cell.get_text(" ", strip=True)
                        for cell in table_row.find_all(
                            ["th", "td"]
                        )
                    ]

                    if (
                        table_cells
                        and UPDATED_LABEL_BG in table_cells[0]
                    ):
                        updated_row = table_cells
                        break

            break

    # The Varna row must contain at least the city
    # and its measured value.
    if not varna_row or len(varna_row) < 2:
        raise RuntimeError(
            "The Varna radiation row was not found."
        )

    value_text = varna_row[1]

    # Extract a decimal value written with either
    # a comma or a period.
    value_match = re.search(
        r"\d+(?:[.,]\d+)?",
        value_text,
    )

    if value_match is None:
        raise RuntimeError(
            "The Varna radiation value was not found."
        )

    # Convert Bulgarian decimal commas to decimal points.
    value = float(
        value_match.group().replace(",", ".")
    )

    # Extract the publication time and date.
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
        "city": "Varna",
        "value": value,
        "unit": "µSv/h",
        "updated_at": updated_at,
        "source_name": "BNRA",
        "source_url": RADIATION_URL,
    }


def get_current_radiation():
    """
    Return the current gamma dose-rate data.

    If the external source is unavailable or its HTML
    structure cannot be parsed, return a safe unavailable
    state so that the Flask application can continue running.
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
            "city": "Varna",
            "value": None,
            "unit": "µSv/h",
            "updated_at": "",
            "source_name": "BNRA",
            "source_url": RADIATION_URL,
        }


if __name__ == "__main__":
    radiation_data = get_current_radiation()

    print("\nRadiation data:")
    print(radiation_data)