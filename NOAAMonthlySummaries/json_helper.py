import requests
import json
import os
import pandas as pd

url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
headers = {"token": "YNdSNAKuShEffldROWvMFiYgGZpcaSsL"}

os.makedirs("data/monthly_summaries", exist_ok=True)

base_params = {
    "limit": 1000,
    "datasetid": "GSOM",
    "locationid": "FIPS:10003",
    "datatypeid": "TAVG"
    
}

start_year = 1938
end_year = 2018
all_data = []

for year in range(start_year, end_year, 10):
    startdate = f"{year}-01-01"
    enddate = f"{min(year + 9, end_year)}-12-31"
    
    params = base_params.copy()
    params["startdate"] = startdate
    params["enddate"] = enddate
    params["offset"] = 1

    print(f"Fetching data from {startdate} to {enddate}")
    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code == 200 and response.content:
        try:
            data = response.json()
            records = data.get("results", [])
            all_data.extend(records)

            json_file = f"data/monthly_summaries/FIPS:10003_avg_{year}_to_{year+10}.json"
            with open(json_file, mode='w') as file:
                json.dump(data, file, indent=4)
            print(f"Saved: {json_file}")
        except json.JSONDecodeError:
            print(f"Failed to decode JSON for {startdate} to {enddate}")
    else:
        print(f"Request failed for {startdate} to {enddate} with status code: {response.status_code}")

df = pd.DataFrame(all_data)
print(df.head())
