from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import string
URL = "https://www.boards.ie/vbulletin/showthread.php?t=2056744169&page="
punctuation_strip = "".maketrans('','',string.punctuation)

print("Getting You codes...")

response = urlopen(URL+'999999').read()
soup = BeautifulSoup(response, 'html.parser')
tmp = str(soup.title).split()
page = int(tmp[tmp.index("Page")+1])


potential_codes = []

for count in range(4,0,-1) :
    for i in soup.find_all("div", class_="postcontent"):
        for code in i.get_text().split() :
            code = code.strip("'")
            code = code.translate(punctuation_strip)
            if code.isupper()  and len(code)>3 and code not in potential_codes:
                potential_codes.append(code)
    page -=1
    if count > 1:
        response = urlopen(URL+str(page)).read()
        soup = BeautifulSoup(response, 'html.parser')
for i in potential_codes:
    print(i)
input()
