from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html)

book = []
for link in bsObj.find("div", {"id":"bodyContent"}).find_all("a",href=re.compile("^(/wiki/)((?!:).)*$")):
    if 'href' in link.attrs:
        # print(link.attrs['href'])
        book.append(link.attrs['href'])

me = []
for link in bsObj.find("div", {"id":"bodyContent"}).find_all("a",href=re.compile("^(/wiki/)((?!:).)")):
    print(link.attrs)
    # if 'href' in link.attrs:
        # print(link.attrs['href'])
        # me.append(link.attrs['href'])
np.setdiff1d(book,me)



# A single function, getLinks, that takes in a Wikipedia article URL of the form
# /wiki/<Article_Name> and returns a list of all linked article URLs in the
# same form.
# A main function that calls getLinks with some starting article, chooses a
# random article link from the returned list, and calls getLinks again, until we
# stop the program or until there are no article links found on the new page.
# Here is the complete code that accomplishes this:


from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re
random.seed(datetime.datetime.now())

def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html)
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$"))
links = getLinks("/wiki/Kevin_Bacon")
while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
    print(newArticle)
links = getLinks(newArticle)




# now to get all the articles in wiki page, but filter so that dont get links that are not url we are interested in:
# eg:

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html)
for link in bsObj.find("div", {"id":"bodyContent"}).findAll("a",
href=re.compile("^(/wiki/)((?!:).)*$")):
if 'href' in link.attrs:
print(link.attrs['href'])





# generate a site map:
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen("http://en.wikipedia.org"+pageUrl)
    bsObj = BeautifulSoup(html)
    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                #We have encountered a new page
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks("/wiki/Christopher_Columbus")




# TODO:: Let's now try to generate a site map of McGill University.
https://www.mcgill.ca



from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
pages = set()

def getLinks(pageUrl):
    global pages
    html = urlopen("http://en.wikipedia.org"+pageUrl)
    bsObj = BeautifulSoup(html)
    try:
        print(bsObj.h1.get_text())
        print(bsObj.find(id ="mw-content-text").findAll("p")[0])
        print(bsObj.find(id="ca-edit").find("span").find("a").attrs['href'])
    except AttributeError:
        print("This page is missing something! No worries though!")
    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                #We have encountered a new page
                newPage = link.attrs['href']
                print("----------------\n"+newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks("")








# Flexible python functions:
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random


pages = set()
random.seed(datetime.datetime.now())
#Retrieves a list of all Internal links found on a page
def getInternalLinks(bsObj, includeUrl):
    internalLinks = []
    #Finds all links that begin with a "/"
    for link in bsObj.findAll("a", href=re.compile("^(/|.*"+includeUrl+")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks

#Retrieves a list of all external links found on a page
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    #Finds all links that start with "http" or "www" that do
    #not contain the current URL
    for link in bsObj.findAll("a",
    href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def splitAddress(address):
    addressParts = address.replace("http://", "").split("/")
    return addressParts

def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html)
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    if len(externalLinks) == 0:
        internalLinks = getInternalLinks(startingPage)
        return getNextExternalLink(internalLinks[random.randint(0,len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]


def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink("http://oreilly.com")
    print("Random external link is: "+externalLink)
    followExternalOnly(externalLink)


followExternalOnly("http://oreilly.com")












