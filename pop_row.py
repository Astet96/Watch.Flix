import sqlite3
import os

dirct = os.getcwd()
dir_db = dirct  + r'\\db'
os.chdir(dir_db)
conn = sqlite3.connect('rows.db')
crsr = conn.cursor()

query = 'CREATE TABLE IF NOT EXISTS genre (genre TEXT)'
crsr.execute(query)
query = 'CREATE TABLE IF NOT EXISTS actor (actor TEXT)'
crsr.execute(query)
query = 'CREATE TABLE IF NOT EXISTS director (director TEXT)'
crsr.execute(query)
query = 'CREATE TABLE IF NOT EXISTS producer (producer TEXT)'
crsr.execute(query)
query = 'CREATE TABLE IF NOT EXISTS country (country TEXT)'
crsr.execute(query)
conn.commit()
conn.close()

conn = sqlite3.connect('IM.db')
crsr = conn.cursor()

query = 'attach "rows.db" as rows'
crsr.execute(query)
query = "INSERT INTO rows.genre SELECT DISTINCT genres FROM title_basics WHERE title_basics.genres NOT LIKE '%,%' AND title_basics.genres != '\\N' AND title_basics.genres !='Adult' ORDER BY genres"
crsr.execute(query)
conn.commit()

query = "INSERT INTO rows.actor SELECT DISTINCT primaryName FROM name_basics WHERE primaryProfession LIKE '%act%' ORDER BY primaryName"
crsr.execute(query)
conn.commit()

query = "INSERT INTO rows.director SELECT DISTINCT primaryName FROM name_basics WHERE primaryProfession LIKE '%direct%' ORDER BY primaryName"
crsr.execute(query)
conn.commit()

query = "INSERT INTO rows.producer SELECT DISTINCT primaryName FROM name_basics WHERE primaryProfession LIKE '%producer%' ORDER BY primaryName"
crsr.execute(query)
conn.commit()

query = "INSERT INTO rows.country SELECT DISTINCT region FROM title_akas WHERE region !='\\N' AND region NOT LIKE '%,%' ORDER BY region"
crsr.execute(query)
conn.commit()
conn.close()