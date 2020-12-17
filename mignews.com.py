import requests
import regex
import bs4
import time

t1 = time.time()


def safe_get(url):
    fail_counter = 0
    request = requests.get(url)
    while request.status_code != 200:
        request = requests.get(url)
        fail_counter += 2
        time.sleep(5 + fail_counter)

        if fail_counter == 6:
            break
    return request


start_url = "https://mignews.com/export/xml/all.html"
request = safe_get(start_url).content.decode("windows-1251")
soup = bs4.BeautifulSoup(request, "lxml")

items = soup.select("contentitem")
for item in items:
    print(item, '\n')
    headline = item.select_one('headline').text
    url = item.select_one('url').text
    abstract = item.select_one('abstract').text
    media = item.select_one("media")['src']

    print(headline)
    print(url)
    print(abstract)
    print(media)
    soup = bs4.BeautifulSoup(safe_get(url).content.decode("windows-1251"), "html.parser")
    left_part = soup.select_one('div#leftc')
    for_time = soup.select_one('span.txtm')
    time = " ".join(for_time.text.split()[:2])
    # del left['div']
    text = list(filter(bool, left_part.text.split('\n')))[1:-5]
    if text[-1].startswith("Читайте"):
        del text[-1]
    text = "\n".join(text)
    print(text)
    print('-' * 150)

import time

t2 = time.time()
s = t2 - t1
print(s)
