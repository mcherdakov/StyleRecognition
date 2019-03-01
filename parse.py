import urllib.request
from bs4 import BeautifulSoup

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def parse(html):
    soup = BeautifulSoup(html)
    table = soup.find("div", class_="cards cards_layout_large")
    imgs = []
    for row in table.find_all("img"):
        imgs.append([row["alt"], row["data-src"]])
        
    return imgs

def download(last, imgs):
    i = last
    for cur in imgs:
        i += 1
        resource = urllib.request.urlopen(cur[1])
        out = open("Falk/" + str(i) + ".jpg", "wb")
        out.write(resource.read())
        out.close()
    return i

def main():
    main_url = "https://www.discogs.com/search/"
    spec = "?genre_exact=Folk%2C+World%2C+%26+Country&limit=250&page="
    last = 0
    for i in range(1, 25):
        page = parse(get_html(main_url + spec + str(i)))
        last = download(last, page)
