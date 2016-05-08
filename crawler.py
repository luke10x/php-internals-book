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
    return href
    
def fix_external_link(link):
    href = link['href']
    link['href'] = "#%s" % href
    return href

def add_linked_page(link):

    href = fix_external_link(link)

    url = base_url + href

    anchor = "<a name=\"%s\"></a>" % href

    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')

    [x.extract() for x in soup.select('a.headerlink')] # remove these strange links 

    [fix_internal_link(x) for x in soup.select('a.reference.internal')]

    content = " ".join([str(x) for x in soup.select('div.content')])
    chapters.append(anchor + content)

toc_url = 'http://www.phpinternalsbook.com/index.html'

toc_page = urllib.request.urlopen(toc_url).read()
toc_soup = BeautifulSoup(toc_page, 'html.parser')
[x.extract() for x in toc_soup.select('a.headerlink')]

[add_linked_page(x) for x in toc_soup.select('div#table-of-contents a.reference.internal')]

c = toc_soup.select('div#table-of-contents')

[print(x) for x in c]
[print(x) for x in chapters]
