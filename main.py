#!/usr/bin/python
# encoding: utf-8
import sys
from workflow import Workflow3
from bs4 import BeautifulSoup
import requests


def main(wf):
    link = "https://namu.wiki/go/%s" % wf.args[0]
    pg = requests.get(link)
    soup = BeautifulSoup(pg.text, "html.parser")
    items = soup.select('.search-item')

    if len(soup.select('button[type=submit]')) == 0:
        wf.add_item(title="Most relevant: %s" % wf.args[0], arg=link, valid=True)
        pg = requests.get("https://namu.wiki/Search?q=%s"%wf.args[0])
        soup = BeautifulSoup(pg.text, "html.parser")
        items = soup.select('.search-item')
    if len(items) == 0:
        wf.add_item(title="%s: No result" % wf.args[0])
    for item in items:
        anchor = item.select('a')[0]
        url = anchor.attrs['href']
        title = anchor.text.strip()
        if url.startswith("/"):
            url = "https://namu.wiki"+url
        wf.add_item(title=title, arg=url, valid=True)
    wf.send_feedback()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
