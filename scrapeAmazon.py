__author__ = 'MBlaauw'
import re
from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+5260+7373+16638+14033/index.html"



def get_bol_booklist( url ):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")

    #
    # NEXT ACTIONS: clean tags, build data set and iterate through all 800+ pages
    #
    # then output the dataset (and timestamp) 

    items = BeautifulSoup(str(soup.find_all("div", "product_content tst_searchresults_details_1")), 'lxml')
    title = items.find_all("a","product_name")
    pubdat = items.find_all(itemprop="datePublished")
    rating = items.find_all(itemprop="ratingValue")
    author = items.find_all(itemprop="author")


    # implement pricetag later
    #items = BeautifulSoup(str(soup.find_all("div", "list_view")), 'lxml')
    #price = items.find_all(itemprop="price")


    for eachItem in items:
        print 'dd'
        print eachItem
        print '---------------------'
        print eachItem.get('class')

    total_nr_of_items = re.sub('<[^>]+>', '', str(soup.find("span", "tst_searchresults_nrFoundItems")))
    total_nr_of_items = float(total_nr_of_items.replace('.', ''))
    total_nr_of_items = int(round(total_nr_of_items / 12))


    '''
    # collect next url and append
    for eachItem in range(1, 10):
        newurl = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+14033/No/' + str(eachItem * 12) + '/section/books/index.html'
        html = urlopen(newurl).read()
        soup = BeautifulSoup(html, "lxml")
        items.append = soup.find_all("div", "product_details_thumb")

    return product_details
    '''

    # collect details from subpages
    # generate_next_url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+14033/No/' + nr_of_items + '/section/books/index.html'

x =  get_bol_booklist(BASE_URL)





url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+5260+7373+16638+14033/index.html'
url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+14033/No/12/section/books/index.html'
url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+14033/No/24/section/books/index.html'