# import

from bs4 import BeautifulSoup
import requests
import os
import re
import sys
from progress.bar import Bar
from multiprocessing import Pool, cpu_count


def get_link_list(url):
    url_list = []
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
                print("saving link: "+site)
            if(site.endswith("/")):
                get_link_list(site)
        if(href == '../'):
            start = True

    return url_list




# download file from URL
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

    # check if file exists
    if not os.path.exists(download_dir+omar_file):
        # download from link
        r = requests.get(link, allow_redirects=True)
        open(download_dir+omar_file, 'wb').write(r.content)


if __name__ == "__main__":
    print("There are {} CPUs on this machine ".format(cpu_count()))
    initial_link = input('What initial link you want to start with? ')

    downloads = get_link_list(initial_link)


    pool = Pool()
    
    bar = Bar('Downloading', max=len(downloads))
    for i in pool.imap(get_file, downloads):
        # print("downloading: "+item)
        bar.next()
    bar.finish()

    input("DONE :D\n")
