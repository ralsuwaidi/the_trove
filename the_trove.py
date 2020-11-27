# import

import datetime
import itertools
import os
import re
import subprocess
import sys
import threading
import time
from functools import partial
from multiprocessing import Pool, cpu_count, freeze_support

import requests
from bs4 import BeautifulSoup
from progress.bar import Bar

url_list = []
done = False

def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rGetting all links, one moment ' + c)
        sys.stdout.flush()
        time.sleep(0.1)



def get_link_list(url):
    urls = []

    website = url
    page = requests.get(website)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find("table", {"id": "list"})
    start = False

    for td in results.find_all("a", href=True):
        href = td['href']
        site = url+href

        if(start and href not in urls):
            urls.append(site)
            if(not site.endswith("/")):
                url_list.append(site)
            if(site.endswith("/")):
                get_link_list(site)
        if(href == '../'):
            start = True


# download file from URL
def get_file(url):
    try:
        link = url
        url = url.replace("https://thetrove.is/Books/", "").replace("%20", " ")
        url = re.sub(r'%\d\d', '', url)
        url = re.sub(r'%\d', '', url)
        url = re.sub(r'%3B', '', url)
        if(url.startswith("/")):
            url = url[1:]

        string_split = url.split("/")
        download_dir = '/'.join([str(elem)
                                 for elem in string_split[:-1]]) + "/"
        try:
            os.makedirs(download_dir)
        except:
            pass
        omar_file = string_split[-1]

        # check if file exists
        if not os.path.exists(download_dir+omar_file):
            # download from link
            # r = requests.get(link, allow_redirects=True)
            # open(download_dir+omar_file, 'wb').write(r.content)
            # print(link)
            # print("downloading to "+download_dir+omar_file)
            cmd = r'c:\aria2\aria2c.exe -m 5 -x 3 ' + ' -d ' + "\"" + download_dir + \
                "\"" + ' -o ' + "\"" + omar_file + "\"" + " " + link
            p1 = subprocess.Popen(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            p1.wait()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    freeze_support()

    print("There are {} CPUs on this machine ".format(cpu_count()))
    initial_link = input('What initial link you want to start with? ')

    try:
        t = threading.Thread(target=animate)
        t.start()
        get_link_list(initial_link)
        done = True
    except KeyboardInterrupt:
        done = True


    pool = Pool()

    bar = Bar('Downloading', max=len(url_list))
    try:
        start = datetime.datetime.now()

        for i in pool.imap(get_file, url_list):
            # print("downloading: "+item)
            bar.next()
        bar.finish()
        end = datetime.datetime.now()
        print("Time elapsed: ", end-start)
        input("DONE :D\n")

    except KeyboardInterrupt:
        print("shutting down...")
