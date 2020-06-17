import urllib.request
import os
import string
from datetime import datetime

to_del = None

def get_poster(link, time):
    global to_del
    src = 'poster.txt'
    os.chdir("..")
    save = os.getcwd() + r"\\static\\tmp\\"
    os.chdir(save)
    save = save + src
    url = 'https://www.imdb.com/title/' + link
    urllib.request.urlretrieve(url, save)

    start = "        <link rel='image_src' href="
    end = '">'

    html = open('poster.txt', 'r')
    while 1:
        code = html.readline()
        if start in code:
            path = [None] * (len(code) - len(start) - len(end) - 2)
            for i in range((len(code) - len(start) - len(end)) - 2):
                path[i] = code[i + len(start) + 1]
            break
    dwnld = ''.join(path)

    jpg = 'poster' + str(time) + '.jpg'
    save = os.getcwd() + r'\\' + jpg
    url = dwnld
    urllib.request.urlretrieve(url, save)
    html.close()
    os.remove(src)
    try:
        os.remove(to_del)
        to_del = jpg
    except:
        to_del = jpg
    os.chdir("..")
    os.chdir("..")
    save = os.getcwd() + r'\\db'
    os.chdir(save)