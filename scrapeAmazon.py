__author__ = 'MBlaauw'
import re, time, datetime, numpy as np, pandas as pd
from pandas import concat
from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+5260+7373+16638+14033/index.html'



def get_bol_bookList(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')

    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    columns = ['Timestamp', 'Author', 'Title', 'Pubdat', 'Rating']

    # todo: Logic works but need to iterate 12 time per page. now takes first result per page
    for i in range(1,13):
        # collect and clean data
        item = BeautifulSoup(str(soup.find_all('div', 'product_content tst_searchresults_details_' + str(i))), 'lxml')
        title = re.sub('<[^>]+>', '', str(item.find_all('a', 'product_name')))
        pubdat = str(item.find_all(itemprop='datePublished'))[16:20]
        rating = str(item.find_all(itemprop='ratingValue'))[16:19]
        author = re.sub('<[^>]+>', '', str(item.find_all(itemprop='author')))

        # build array and then data frame
        arr = np.array([[timestamp], [author], [title], [pubdat], [rating]]).T
        if i == 1:
            df = pd.DataFrame(arr, columns=columns)
        else:
            df2 = pd.DataFrame(arr, columns=columns)
            df = concat([df, df2], ignore_index=True)

    # determine maxmimum results and devide bij 12 (results per page)
    total_nr_of_items = re.sub('<[^>]+>', '', str(soup.find('span', 'tst_searchresults_nrFoundItems')))
    total_nr_of_items = int(round(int(float(total_nr_of_items.replace('.', '')))/12))

    # collect the motherload (minus one, cause less results on final page)
    for eachItem in range(1, total_nr_of_items):
        print 'Scraping link number: ' + str(eachItem)
        newurl = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+14033/No/' + str(eachItem * 12) + '/section/books/index.html'
        html = urlopen(url).read()
        soup = BeautifulSoup(html, 'lxml')

        for i in range(1, 13):
            # collect and clean data
            item = BeautifulSoup(str(soup.find_all('div', 'product_content tst_searchresults_details_' + str(i))), 'lxml')
            title = re.sub('<[^>]+>', '', str(item.find_all('a', 'product_name')))
            pubdat = str(item.find_all(itemprop='datePublished'))[16:20]
            rating = str(item.find_all(itemprop='ratingValue'))[16:19]
            author = re.sub('<[^>]+>', '', str(item.find_all(itemprop='author')))

            # build array and then data frame
            arr = np.array([[timestamp], [author], [title], [pubdat], [rating]]).T
            df2 = pd.DataFrame(arr, columns=columns)
            df = concat([df, df2], ignore_index=True)

    # return the final results
    # time.sleep(1)
    return df

    '''
    # collect price block
    # BeautifulSoup(str(soup.find_all('strong', 'bol_pricetag big')), 'lxml')
    # price = items.find_all(itemprop='price')
    '''
test = get_bol_bookList(BASE_URL)

