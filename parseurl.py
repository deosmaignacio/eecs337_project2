import re
import urllib.request
from bs4 import BeautifulSoup

def processhtml(url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html,features="html.parser")
    data = soup.findAll(text=True)

    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        return True

    result = list(filter(visible, data))

    count = 0
    for i in result:
        if i == '\n':
            count += 1

    for i in range(count):
        result.remove('\n')

    for index in range(len(result)):
        result[index] = ' '.join(result[index].split())

    count = 0
    for i in result:
        if i == '':
            count += 1

    for i in range(count):
        result.remove('')

    for index in range(len(result)):
        if result[index] == "Ingredients":
            result = result[index:]
            break

    for index in range(len(result)):
        if result[index] =="Share":
            result = result[:index]
            break

    return result
