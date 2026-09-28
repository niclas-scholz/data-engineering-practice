from pathlib import Path

import pandas as pd
import requests

"""
Problems Statement
You need to download a file of weather data from a government website. files that are sitting at the following specified location.

https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/

You are looking for the file that was Last Modified on 2024-01-19 10:27, you can't cheat and lookup the file number yourself. You must use Python to scrape this webpage, finding the corresponding file-name for this timestamp, 2024-01-19 10:27

Once you have obtained the correct file, and downloaded it, you must load the file into Pandas and find the record(s) with the highest HourlyDryBulbTemperature. Print these record(s) to the command line.

Generally, your script should do the following ...

Attempt to web scrap/pull down the contents of https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/
Analyze it's structure, determine how to find the corresponding file to 2024-01-19 10:27 using Python.
Build the URL required to download this file, and write the file locally.
Open the file with Pandas and find the records with the highest HourlyDryBulbTemperature.
Print this to stdout/command line/terminal.
"""


def main():

    url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
    df = pd.read_html(url)[0]
    print(df)

    match = df[(df == "2024-01-19 15:01").any(axis=1)]
    name = match["Name"].iloc[0]

    file_url = url + name
    Path("downloads").mkdir(parents=True, exist_ok=True)
    (Path("downloads") / name).write_bytes(requests.get(file_url, timeout=30).content)

    df = pd.read_csv(Path("downloads") / name)
    max_hourly_dry_bulb_temperature = df["HourlyDryBulbTemperature"].max()
    print(f"Maximum HourlyDryBulbTemperature: {max_hourly_dry_bulb_temperature}")


if __name__ == "__main__":
    main()
