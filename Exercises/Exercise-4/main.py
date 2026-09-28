import csv
import glob
import json
import os

import pandas as pd

"""
Problems Statement
There is a folder called data in this current directory, Exercises/Exercise-4. There are also json files located at various spots inside this directory structure.

Your task is two use Python to find all the json files located in the data folder. Once you find them all, read them with Python and convert them to csv files, to do this you will have to flatten out some of the nested json data structures.

For example there is a {"type":"Point","coordinates":[-99.9,16.88333]} that must flattened.

Generally, your script should do the following ...

Crawl the data directory with Python and identify all the json files.
Load all the json files.
Flatten out the json data structure.
Write the results to a csv file, one for one with the json file, including the header names."""


def main():

    for root, dirs, files in os.walk("data"):
        for file in files:
            if file.endswith(".json"):
                with open(os.path.join(root, file)) as f:
                    data = json.load(f)
                    data = pd.json_normalize(data).to_dict(orient="records")
                with open(
                    "output_" + file.replace(".json", ".csv"), "w", newline=""
                ) as f:
                    if isinstance(data, dict):
                        data = [data]
                    w = csv.DictWriter(f, fieldnames=data[0].keys())
                    w.writeheader()
                    w.writerows(data)

    files = glob.glob("output_*.csv")
    df = pd.concat([pd.read_csv(f) for f in files])
    df.to_csv("combined.csv", index=False)
    df.to_csv("out.csv", index=False, float_format="%.3f")


if __name__ == "__main__":
    main()
