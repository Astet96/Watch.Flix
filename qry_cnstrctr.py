import sqlite3
import os
import random
import string

def t_name(tsv):
    ln = len(tsv)
    name = [None] * ln
    for i in range(ln):
        name[i] = tsv[i]
    return ''.join(name)

def qry(crit):
    conn = sqlite3.connect('IM.db')
    crsr = conn.cursor()
    #get: type, period, genre
    q1 = ("SELECT title_basics.tconst FROM title_basics WHERE title_basics.titleType LIKE '%{}%' AND title_basics.startYear >= {} AND title_basics.startYear < {} AND title_basics.genres LIKE '%{}%'" .format(crit[0], crit[1], int(crit[1]) + 10, crit[2]))
    #get: rating
    q2 = (" INTERSECT SELECT title_ratings.tconst FROM title_ratings WHERE title_ratings.averageRating >= {} AND title_ratings.averageRating <= {}" .format(float(crit[3]) - 0.5, float(crit[3]) + 0.5))
    #get: country
    q3 = (" INTERSECT SELECT DISTINCT title_akas.titleId FROM title_akas WHERE title_akas.region LIKE '%{}%' AND (title_akas.types = 'original' OR title_akas.types = 'working')" .format(crit[7]))

    #get: actor
    if crit[4] != "":
        q4 = (" INTERSECT SELECT title_principals.tconst FROM title_principals WHERE (title_principals.category = 'actor' OR title_principals.category = 'actress') AND title_principals.nconst IN (SELECT name_basics.nconst FROM name_basics WHERE name_basics.primaryName = '{}')" .format(crit[4]))
    else:
        q4 = ""
    #get: director
    if crit[5] != "":
        q5 = (" INTERSECT SELECT title_principals.tconst FROM title_principals WHERE title_principals.category = 'director' AND title_principals.nconst IN (SELECT name_basics.nconst FROM name_basics WHERE name_basics.primaryName = '{}')" .format(crit[5]))
    else:
        q5 = ""
    #get: producer
    if crit[6] != "":
        q6 = (" INTERSECT SELECT title_principals.tconst FROM title_principals WHERE title_principals.category = 'producer' AND title_principals.nconst IN (SELECT name_basics.nconst FROM name_basics WHERE name_basics.primaryName = '{}')" .format(crit[6]))
    else:
        q6 = ""

    query = q1 + q2 + q3 + q4 + q5 + q6
    crsr.execute(query)
    res = crsr.fetchall()
    ln = len(res) - 1
    if not res:
        return 0
    else:
        chs = random.randint(0, ln)
        ret = t_name(res[chs])
        return ret

def rand_qry():
    conn = sqlite3.connect('IM.db')
    crsr = conn.cursor()
    q = "SELECT title_basics.tconst FROM title_basics WHERE titleType != 'tvEpisode' AND isAdult != '1' ORDER BY RANDOM() LIMIT 1"
    crsr.execute(q)
    res = crsr.fetchone()
    return t_name(res)