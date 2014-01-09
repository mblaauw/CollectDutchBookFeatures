__author__ = 'MBlaauw'
import re
import pandas as pd
import time
import datetime
import numpy as np
from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+5260+7373+16638+14033/index.html"

def get_bol_booklist( url ):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")


    # todo: Logic works but need to iterate 12 time per page. now takes first result per page


    # collect and clean data
    item = BeautifulSoup(str(soup.find_all("div", "product_content tst_searchresults_details_1")), 'lxml')
    title = re.sub('<[^>]+>', '', str(item.find_all("a", "product_name")))
    pubdat = str(item.find_all(itemprop="datePublished"))[16:20]
    rating = str(item.find_all(itemprop="ratingValue"))[16:19]
    author = re.sub('<[^>]+>', '', str(item.find_all(itemprop="author")))

    # build array and then data frame
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    columns = ['Timestamp', 'Author', 'Title', 'Pubdat', 'Rating']
    arr = np.array([[timestamp], [author], [title], [pubdat], [rating]]).T
    df = pd.DataFrame(arr, columns=columns)

    # collect price block
    # BeautifulSoup(str(soup.find_all("strong", "bol_pricetag big")), 'lxml')
    # price = items.find_all(itemprop="price")

    # determine maxmimum results and devide bij 12 (results per page)
    total_nr_of_items = re.sub('<[^>]+>', '', str(soup.find("span", "tst_searchresults_nrFoundItems")))
    total_nr_of_items = float(total_nr_of_items.replace('.', ''))
    total_nr_of_items = int(round(total_nr_of_items / 12))



    # collect next url and append
    for eachItem in range(1, 5):
        newurl = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+14033/No/' + str(eachItem * 12) + '/section/books/index.html'
        html = urlopen(newurl).read()
        soup = BeautifulSoup(html, "lxml")

        # collect and clean data
        item = BeautifulSoup(str(soup.find_all("div", "product_content tst_searchresults_details_1")), 'lxml')
        title = re.sub('<[^>]+>', '', str(item.find_all("a", "product_name")))
        pubdat = str(item.find_all(itemprop="datePublished"))[16:20]
        rating = str(item.find_all(itemprop="ratingValue"))[16:19]
        author = re.sub('<[^>]+>', '', str(item.find_all(itemprop="author")))

        # build array and then data frame
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        columns = ['Timestamp', 'Author', 'Title', 'Pubdat', 'Rating']
        arr = np.array([[timestamp], [author], [title], [pubdat], [rating]]).T

        print arr
        #df.append(arr)
        #df = pd.DataFrame(arr, columns=columns)

    return arr



test = get_bol_booklist(BASE_URL)

