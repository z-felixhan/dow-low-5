from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://ca.finance.yahoo.com/quote/%5EDJI/components?p=%5EDJI"
html = urlopen(url)

titles = []
soup = BeautifulSoup(html, "lxml")
for a in soup.tbody.find_all('a'):
    titles.append(a.get('title'))

titles_count = len(titles)

print(titles)
print(titles_count)
