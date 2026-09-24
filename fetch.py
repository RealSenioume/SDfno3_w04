//fetching data fr0m NASA POWER

import requests
from pathlib import Path

API_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

params = {
    "parameters": "ALLSKY_SFC_SW_DWN,T2M",
    "community": "RE",
    "latitude": 22.32,
    "longitude": 114.17,
    "start": "20260101",
    "end": "20260601",
    "format": "CSV",
    "time-standard": "LST",
}

response = requests.get(API_URL, params=params, timeout=60)
response.raise_for_status()

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

output_file = data_dir / "nasa_power_hongkong_202601t06.csv"
output_file.write_text(response.text, encoding="utf-8")

print(f"Saved {len(response.text.splitlines())} lines to {output_file}")
