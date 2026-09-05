"""
Fetch daily river discharge data from the Open-Meteo Flood API (GloFAS) for a
list of Bangladeshi districts.

API docs: https://open-meteo.com/en/docs/flood-api
No API key required for non-commercial use. Data is simulated river discharge
(m3/s) at ~5 km resolution, available from 1984-01-01 up to a 7-month forecast.
"""

import time

import pandas as pd
import requests

from districts import DISTRICTS

FLOOD_API_URL = "https://flood-api.open-meteo.com/v1/flood"


def fetch_district_discharge(
    district: dict, past_days: int = 92, forecast_days: int = 14
) -> pd.DataFrame:
    """
    Fetch river discharge (m3/s) for one district: recent history + short forecast.

    past_days: days of recent history to pull (max 92 per request without
               explicit start_date/end_date)
    forecast_days: days ahead to pull (max 210)
    """
    params = {
        "latitude": district["latitude"],
        "longitude": district["longitude"],
        "daily": "river_discharge",
        "past_days": past_days,
        "forecast_days": forecast_days,
        "timeformat": "iso8601",
    }

    response = requests.get(FLOOD_API_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()

    daily = payload["daily"]
    df = pd.DataFrame(
        {
            "date": daily["time"],
            "river_discharge_m3s": daily["river_discharge"],
        }
    )
    df["district"] = district["name"]
    df["division"] = district["division"]
    df["latitude"] = district["latitude"]
    df["longitude"] = district["longitude"]
    return df


def fetch_all_districts(districts: list | None = None) -> pd.DataFrame:
    """Fetch discharge data for every district and combine into one DataFrame."""
    districts = districts or DISTRICTS
    frames = []
    for district in districts:
        print(f"Fetching flood data for {district['name']}...")
        frames.append(fetch_district_discharge(district))
        time.sleep(1)  # be polite to the free, no-key API
    return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    all_data = fetch_all_districts()
    print(all_data.head(20))
    print(f"\nTotal rows: {len(all_data)}")
    all_data.to_csv("flood_discharge_raw.csv", index=False)
    print("Saved to flood_discharge_raw.csv")
