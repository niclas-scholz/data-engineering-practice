import zipfile
from pathlib import Path

import requests

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

"""
Generally, your script should do the following ...

create the directory downloads if it doesn't exist

download the files one by one.

split out the filename from the uri, so the file keeps its original filename.

Each file is a zip, extract the csv from the zip and delete the zip file.

"""


def main():
    # your code here

    Path("downloads").mkdir(parents=True, exist_ok=True)

    for uri in download_uris:
        name = uri.split("/")[-1]
        dest = Path("downloads") / name
        dest.write_bytes(requests.get(uri).content)
        if zipfile.is_zipfile(dest):
            zipfile.ZipFile(dest).extractall("downloads")
            dest.unlink()

    for z in Path("downloads").glob("*.zip"):
        z.unlink()




if __name__ == "__main__":
    main()
