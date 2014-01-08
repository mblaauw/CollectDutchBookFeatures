__author__ = 'MBlaauw'
import re
from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+5260+7373+16638+14033/index.html"

def get_bol_booklist( url ):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    product_details = soup.find_all("div", "product_details_thumb")
    total_nr_of_items = re.sub('<[^>]+>', '', str(soup.find("span", "tst_searchresults_nrFoundItems")))
    total_nr_of_items = total_nr_of_items.replace('.', '')
    total_nr_of_items = float(total_nr_of_items)

    # determine iterations
    iterations = int(round(total_nr_of_items / 12))

    nr_of_items = len(product_details_thumb)
    # collect details from subpages
    # generate_next_url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+14033/No/' + nr_of_items + '/section/books/index.html'

print get_bol_booklist(BASE_URL)





url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+5260+7373+16638+14033/index.html'
url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+14033/No/12/section/books/index.html'
url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+14033/No/24/section/books/index.html'