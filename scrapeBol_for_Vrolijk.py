__author__ = 'MBlaauw'


import sys
import re, time, datetime, numpy as np, pandas as pd
from pandas import concat
from bs4 import BeautifulSoup
from urllib2 import urlopen

#sys.setdefaultencoding("utf-8")
#BASE_URL = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-thrillers/N/261+8293+5260+7373+16638/index.html'
#BASE_URL = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-literatuur-nieuw/N/87+8293+14033/No/0/section/books/index.html'

BASE_URL = 'http://www.bol.com/nl/s/boeken/zoekresultaten/N/8299/No/12/section/books/Ntt/gay%2Bebook/Nty/0/sc/books_all/index.html'


# Get list of unique product ID's
def get_bol_book_list(url, test=True):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')

    unique = list()

    for eachRow in list(soup.find_all('a', 'product_name')):
        unique.append(eachRow.get('href'))

    # collect the motherload (minus one, cause less results on final page)
    # determine maxmimum results and devide bij 12 (results per page)
    total_nr_of_items = re.sub('<[^>]+>', '', str(soup.find('span', 'tst_searchresults_nrFoundItems')))
    total_nr_of_items = int(round(int(float(total_nr_of_items.replace('.', '')))/12))

    if test:
        total_nr_of_items = 10

    for eachItem in range(1, total_nr_of_items):
        print 'Scraping link number: ' + str(eachItem)
        # new_url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-thrillers/N/261+8293/No/' + str(eachItem * 12) + '/section/books/index.html'
        # new_url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-literatuur-nieuw/N/87+8293+14033/No/' + str(eachItem * 12) + '/section/books/index.html'
        new_url = 'http://www.bol.com/nl/s/boeken/zoekresultaten/N/8299/No/' + str(eachItem * 12) + '/section/books/Ntt/gay%2Bebook/Nty/0/sc/books_all/index.html'
        print new_url

        html = urlopen(new_url).read()
        soup = BeautifulSoup(html, 'lxml')

        for eachRow in list(soup.find_all('a', 'product_name')):
            unique.append(eachRow.get('href'))

    # clean the list and return from function
    unique_result = list()
    for i in range(1, len(unique)):
        unique_result.append(str(unique[i]).split('/')[6])

    return unique_result


# Get details per product ID's through API
def get_bol_book_details(book_id_list, test=True):

    # clean and extract ids before parse
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    columns = ['Timestamp', 'BOL_Key', 'EAN', 'GPC', 'Title', 'Price', 'Rating', 'Summary']

    if test == True:
        number_to_fetch = 10
    else:
        number_to_fetch = len(book_id_list)


    for i in range(1, number_to_fetch):
        get_id = book_id_list[i]

        print get_id

        new_url = 'https://api.bol.com/catalog/v4/products/' + str(get_id) + '/?apikey=6B7C36DAC35D448C81938122EA8C7C1B&format=xml'

        # collect detailed html
        html = urlopen(new_url, timeout=5).read()
        soup = BeautifulSoup(html, 'lxml')

        # trap the rating attribute. Sometimes doesnt exist. Zero them if this happens
        rating = soup.find_all('rating')
        if len(rating) == 0:
            rating = str(0)
        else:
            rating = soup.products.rating.string

        # trap the summary attribute. Sometimes doesnt exist. Zero them if this happens
        summary = soup.find_all('summary')
        if len(summary) == 0:
            summary = str(0)
        else:
            summary = soup.products.summary.string


        price = soup.find_all('price')
        if len(price) == 0:
            price = str(0)
        else:
            price = soup.products.offerdata.offers.price.string

        #print price, summary, rating, price
        print i, [timestamp],[soup.products.id.string],[soup.products.ean.string],[soup.products.gpc.string],[soup.products.title.string],[price],[rating],[summary]

        arr = np.array([[timestamp],
                        [soup.products.id.string],
                        [soup.products.ean.string],
                        [soup.products.gpc.string],
                        [soup.products.title.string],
                        [price],
                        [rating],
                        [summary]
        ]).T

        if i == 1:
            df = pd.DataFrame(arr, columns=columns)
        else:
            df2 = pd.DataFrame(arr, columns=columns)
            df = concat([df, df2], ignore_index=True)

    return df


## VROLIJK GAY BOOKS
import pickle
#book_id_list = get_bol_book_list(BASE_URL, test=False)
#pickle.dump(book_id_list, open('book_id_list_bol_gay.pickle', "w"))
book_id_list = pickle.load(open('book_id_list_bol_gay.pickle'))

book_details_bol_gay = get_bol_book_details(book_id_list, test=False)
book_details_bol_gay.to_csv('output_gay_ebooks_bol.csv')



