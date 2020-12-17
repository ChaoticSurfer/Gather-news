import requests
import bs4
import time
import regex as re
import lxml

t1 = time.time()


def safe_get(url):
    fail_counter = 0
    request = requests.get(url)
    while request.status_code != 200:
        request = requests.get(url)
        fail_counter += 1
        time.sleep(5 + fail_counter * 3)

        if fail_counter == 3:
            raise Exception("safe_get failed 3 times!")
    return request


start_url = "http://feeds.newsru.co.il/il/www/news/all"
request = safe_get(start_url).content.decode("utf-8", errors='ignore')
soup = bs4.BeautifulSoup(request, "lxml")

items = soup.select("item")

for item in items:
    print(item, '\n')

    for i in str(item).splitlines():
        if i.startswith("<link/>"):
            url = i[7:]

    print(url)

    pubdate = item.select_one("pubdate")
    print(pubdate, "pub-date")
# detailed
    request = safe_get(url).content.decode('utf-8', errors='ignore')
    soup = bs4.BeautifulSoup(request, "lxml")

    text = soup.select_one("article.text").select("p")
    text_result = ''
    for i in text:
        i = i.text
        if not i.isspace():
            text_result += i + '\n'

    print('\n|', text_result, '|\n')

    heading = soup.select_one("h1.article_title_h1")
    # img_link = soup.select_one("div.images").select_one("img").get("src")

    # l = re.compile(u'<link\/>.*rss', flags=re.MULTILINE | re.UNICODE)
    # item = string(item)
    # link = l.search(string(item))
    # print('!!!!', link.group(), l.match(string(item)))

t2 = time.time()
s = t2 - t1
print(s)
