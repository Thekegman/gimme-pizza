from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import string, os

URL = "https://www.boards.ie/vbulletin/showthread.php?t=2056744169&page="
punctuation_strip = "".maketrans('','',string.punctuation)

class MyHandlerForHTTP(BaseHTTPRequestHandler):
     def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes('<br><p style="text-align:center;font-weight:bold;font-size:x-large">Potential Codes</p>','UTF-8'))
        for code in get_codes(4):
            self.wfile.write(bytes('<p style="text-align:center">'+code+"</p>", 'UTF-8'))

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', os.environ['PORT'])
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
    
def get_codes(n):
    response = urlopen(URL+'999999').read()
    soup = BeautifulSoup(response, 'html.parser')
    tmp = str(soup.title).split()
    page = int(tmp[tmp.index("Page")+1])

    potential_codes = []

    for count in range(n,0,-1) :
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
    return potential_codes


run(handler_class=MyHandlerForHTTP)
