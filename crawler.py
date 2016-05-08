#!ENV/bin/python

import re
import urllib.request
from bs4 import BeautifulSoup

chapters = []
base_url = "http://www.phpinternalsbook.com/"

def fix_internal_link(link):
    href = link['href']
    href = re.sub('^(.*)#', '', href)
    link['href'] = "#%s" % href
    
def fix_external_link(link):
    href = link['href']
    link['href'] = "#%s" % href

def fix_image(img):
    rsrc = img['src']
    lsrc = re.sub('^(\.\./_images/)', '', rsrc)
    url = base_url + '_images/' + lsrc
    content = urllib.request.urlopen(url).read()
    content_str = content.decode(encoding='UTF-8')

    f = open(lsrc, "w")
    f.write(str(content_str))
    f.close()

    img['src'] = lsrc

def add_linked_page(link):

    href = link['href']

    fix_external_link(link)

    url = base_url + href

    anchor = "<a name=\"%s\"></a>" % href

    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')

    # remove these strange links
    [x.extract() for x in soup.select('a.headerlink')]

    # fix links for TOC's inside chapters
    [fix_internal_link(x) for x in soup.select('a.reference.internal')]

    [fix_image(x) for x in soup.select('img')]

    content = " ".join([str(x) for x in soup.select('div.content')])
    chapters.append(anchor + content)

toc_url = 'http://www.phpinternalsbook.com/index.html'

toc_page = urllib.request.urlopen(toc_url).read()
toc_soup = BeautifulSoup(toc_page, 'html.parser')
[x.extract() for x in toc_soup.select('a.headerlink')]

[add_linked_page(x) for x in toc_soup.select('div#table-of-contents a.reference.internal')]

c = toc_soup.select('div#table-of-contents')

head = """
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
"""
print(head)

[print(x) for x in c]
[print(x) for x in chapters]
