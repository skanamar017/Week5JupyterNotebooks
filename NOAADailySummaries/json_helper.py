import requests
import json
import os
import pandas as pd

url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
headers = {"token": "YNdSNAKuShEffldROWvMFiYgGZpcaSsL"}
params = {
    "limit": 1000,
    "offset": 1,
    "datasetid": "GHCND",
    "locationid": "FIPS:10003",
    "startdate": "2018-01-01",
    "enddate": "2018-01-31"
}

os.makedirs("data/daily_summaries", exist_ok=True)

response = requests.get(url=url, headers=headers, params=params)

if response.status_code == 200:
    print("Initial request successful!")
    data = response.json()
    total_count = data["metadata"]["resultset"]["count"]

    i = 0
    while i * params["limit"] < total_count:
        params["offset"] = i * params["limit"] + 1
        sub_response = requests.get(url=url, headers=headers, params=params)
        if sub_response.status_code == 200 and sub_response.content:
            try:
                sub_data = sub_response.json()
                json_file = f"data/daily_summaries/daily_summaries_FIPS10003_jan_2018_{i}.json"
                with open(json_file, mode='w') as file:
                    json.dump(sub_data, file, indent=4)
                print(f"Saved: {json_file}")
            except json.JSONDecodeError:
                print(f"Failed to decode JSON at offset {params['offset']}")
                print(sub_response.text)
        else:
            print(f"Request failed at offset {params['offset']} with status code: {sub_response.status_code}")
        i += 1
else:
    print(f"Initial request failed with status code: {response.status_code}")

