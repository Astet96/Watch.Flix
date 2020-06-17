# This script converts the downloaded CSV files to a SQLite database
import sqlite3
import csv
import os
import string
import sys

dirct = os.getcwd()
dir_csv = dirct  + r'\\csv'
dir_db = dirct  + r'\\db'

os.chdir(dir_db)
fail_log = open('fail_log.txt', 'a', encoding = 'UTF8')
conn = sqlite3.connect('IM.db')
crsr = conn.cursor()

os.chdir(dir_csv)
tsv = os.listdir(dir_csv)

#maximize csv field size method from: https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072
maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

#Ensure table name doesn't contain '.'
def t_name(tsv):
    ln = len(tsv)-4
    name = [None] * ln
    for i in range(ln):
        if tsv[i] == '.':
            name[i] = '_'
        else:
            name[i] = tsv[i]
    return ''.join(name)

#generate tables from CSVs
def imprt(tsv):
    tbl_name = t_name(tsv)
    with open(tsv, 'r', encoding = 'UTF8') as table:
        rdr = csv.DictReader(table, delimiter = "\t")
        hdr = rdr.fieldnames
        cl = len(hdr)
        batch = 0
        for i in range(cl):
            if i == 0:
                query = 'CREATE TABLE IF NOT EXISTS {} ({} TEXT)' .format(tbl_name, hdr[i])
                crsr.execute(query)
                conn.commit()
            else:
                query = 'ALTER TABLE {} ADD {} TEXT' .format(tbl_name, hdr[i])
                crsr.execute(query)
                conn.commit()
        for row in rdr:
            try:
                query = "INSERT INTO {} ({}) VALUES('{}')" .format(tbl_name, ", ".join(hdr), "', '".join(row.values()))
                crsr.execute(query)
            except:
                try:
                    query = 'INSERT INTO {} ({}) VALUES("{}")' .format(tbl_name, ', '.join(hdr), '", "'.join(row.values()))
                    crsr.execute(query)
                except:
                    try:
                        query = 'INSERT INTO {} ({}) VALUES({})' .format(tbl_name, ', '.join(hdr), ', '.join(row.values()))
                        crsr.execute(query)
                    except:
                        #catches all failed imports into log
                        print(query, file = fail_log)
            batch +=1
            if batch == 50:
                conn.commit()
                batch = 0
        conn.commit()

nr = len(tsv)
for i in range(nr):
    imprt(tsv[i])

conn.close()
fail_log.close()