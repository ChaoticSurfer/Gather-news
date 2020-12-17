import requests
import regex
import bs4

start_url = "http://mignews.ru/export/yandex_rss2.html"
request = requests.get(start_url)

if request.status_code != 200:
    request = requests.get(start_url)
    print(request.status_code)

content = request.content.decode(encoding='windows-1251', errors="strict")
soup = bs4.BeautifulSoup(content, "html.parser")
items = soup.select('item')
# print(soup.prettify())

for item in items:
    print(item.select_one('title').text)
    print(item.select_one('description').text)
    s = str(item)
    l1 = s.find("link")
    l2 = s.find("<", l1)
    print(s[l1 + 6:l2])
    print(item.select_one('pubdate').text)
    print(item.select_one('category').text)
    print(item.select_one('author').text)
    print(item.find("yandex:full-text").text)
    print("-" * 40)

# print(soup.prettify())
