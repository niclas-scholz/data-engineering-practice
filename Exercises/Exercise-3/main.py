import gzip
import urllib.request

'''Problems Statement
AWS puts out some "common crawl" web data, available on s3 with no special permissions needed. http://commoncrawl.org/the-data/get-started/

Your task is two-fold, download a .gz file located in s3 bucket commoncrawl and key crawl-data/CC-MAIN-2022-05/wet.paths.gz using boto3.

Once this file is downloaded, you must extract the file, open it, and download the file uri located on the first line using boto3 again. Store the file locally and iterate through the lines of the file, printing each line to stdout.

Generally, your script should do the following ...

boto3 download the file from s3 located at bucket commoncrawl and key crawl-data/CC-MAIN-2022-05/wet.paths.gz
Extract and open this file with Python (hint, it's just text).
Pull the uri from the first line of this file.
Again, download the that uri file from s3 using boto3 again.
Print each line, iterate to stdout/command line/terminal.'''


BASE = "https://data.commoncrawl.org/"
KEY = "crawl-data/CC-MAIN-2022-05/wet.paths.gz"


def main():
    with urllib.request.urlopen(BASE + KEY) as r, gzip.GzipFile(fileobj=r) as gz:
        first_key = gz.readline().decode().strip()

    with urllib.request.urlopen(BASE + first_key) as r, gzip.GzipFile(fileobj=r) as gz:
        for line in gz:
            print(line.decode(errors="replace").rstrip("\n"))


if __name__ == "__main__":
    main()
