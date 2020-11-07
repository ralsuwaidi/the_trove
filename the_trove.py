# import

from bs4 import BeautifulSoup
import requests
import os
import re
import sys
from progress.bar import Bar

initial_link = input('What initial link you want to start with? ')

urls = []
downloads = []


def get_link_list(url):
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
                downloads.append(site)
                print("saving link: "+site)
            if(site.endswith("/")):
                get_link_list(site)
        if(href == '../'):
            start = True


get_link_list(initial_link)


def get_file(url):
    link = url
    url = url.replace("https://thetrove.is/Books/", "").replace("%20", " ")
    url = re.sub(r'%\d\d', '', url)
    url = re.sub(r'%\d', '', url)
    if(url.startswith("/")):
        url = url[1:]

    string_split = url.split("/")
    download_dir = '/'.join([str(elem) for elem in string_split[:-1]]) + "/"
    try:
        os.makedirs(download_dir)
    except:
        pass
    omar_file = string_split[-1]
    r = requests.get(link, allow_redirects=True)

    open(download_dir+omar_file, 'wb').write(r.content)


bar = Bar('Downloading', max=len(downloads))

for item in downloads:
    # print("downloading: "+item)
    bar.next()
    get_file(item)
bar.finish()

input("DONE :D\n")
