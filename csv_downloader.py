# This script downloads and extracts the CSV.gz datasets from https://datasets.imdbws.com/

import requests
import gzip
import shutil
import os

# file streaming with method from: http://masnun.com/2016/09/18/python-using-the-requests-module-to-download-large-files-efficiently.html
def dwnldr(url, file):
    response = requests.get(url , stream=True)
    handle = open(file, 'wb')
    for chunk in response.iter_content(chunk_size = 512):
        if chunk:
            handle.write(chunk)

# unzip archives with method from: https://stackoverflow.com/questions/31028815/how-to-unzip-gz-file-using-python
def unzip(name, archive):
    with gzip.open(archive, 'rb') as f_in:
        with open(name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

dirct = os.getcwd() + r'\\csv'

IMDb =[{"url" : 'https://datasets.imdbws.com/name.basics.tsv.gz', "file" : dirct + r'\name.basics.tsv.gz'},
    {"url" : 'https://datasets.imdbws.com/title.akas.tsv.gz', "file" : dirct + r'\title.akas.tsv.gz'},
    {"url" : 'https://datasets.imdbws.com/title.basics.tsv.gz', "file" : dirct + r'\title.basics.tsv.gz'},
    {"url" : 'https://datasets.imdbws.com/title.crew.tsv.gz', "file" : dirct + r'\title.crew.tsv.gz'},
    {"url" : 'https://datasets.imdbws.com/title.episode.tsv.gz', "file" : dirct + r'\title.episode.tsv.gz'},
    {"url" : 'https://datasets.imdbws.com/title.principals.tsv.gz', "file" : dirct + r'\title.principals.tsv.gz'},
    {"url" : 'https://datasets.imdbws.com/title.ratings.tsv.gz', "file" : dirct + r'\title.ratings.tsv.gz'}]

nr = len(IMDb)
for i in range(nr):
    dwnldr(IMDb[i]["url"], IMDb[i]["file"])

os.chdir(dirct)

GZ =[{"name" : 'name.basics.tsv', "archive" : 'name.basics.tsv.gz'},
    {"name" : 'title.akas.tsv', "archive" : 'title.akas.tsv.gz'},
    {"name" : 'title.basics.tsv', "archive" : 'title.basics.tsv.gz'},
    {"name" : 'title.crew.tsv', "archive" : 'title.crew.tsv.gz'},
    {"name" : 'title.episode.tsv', "archive" : 'title.episode.tsv.gz'},
    {"name" : 'title.principals.tsv', "archive" : 'title.principals.tsv.gz'},
    {"name" : 'title.ratings.tsv', "archive" : 'title.ratings.tsv.gz'}]

nr = len(GZ)
for i in range(nr):
    unzip(GZ[i]["name"], GZ[i]["archive"])
    os.remove(GZ[i]["archive"])