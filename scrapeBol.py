__author__ = 'MBlaauw'
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")

import sys
import re, time, datetime, numpy as np, pandas as pd
from pandas import concat
from bs4 import BeautifulSoup
from urllib2 import urlopen

#BASE_URL = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-thrillers/N/261+8293+5260+7373+16638/index.html'
BASE_URL = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-literatuur-nieuw/N/87+8293+14033/No/0/section/books/index.html'


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
        new_url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-literatuur-nieuw/N/87+8293+14033/No/' + str(eachItem * 12) + '/section/books/index.html'

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
def get_bol_book_details(book_id_list):

    # clean and extract ids before parse
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    columns = ['Timestamp', 'BOL_Key', 'EAN', 'GPC', 'Title', 'Price', 'Rating', 'Summary']

    for i in range(1, len(book_id_list)):
        get_id = book_id_list[i]

        print get_id
        new_url = 'https://api.bol.com/catalog/v4/products/' + str(get_id) + '/?apikey=6B7C36DAC35D448C81938122EA8C7C1B&format=xml'

        # collect detailed html
        html = urlopen(new_url).read()
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

        print price

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


# Get dataframe with book attributes
def get_bol_book_attributes(book_id_list):
    for i in range(0, len(book_id_list)):
        # DUMMY

        get_id = book_id_list[i]
        new_url = 'https://api.bol.com/catalog/v4/products/' + str(get_id) + '/?apikey=6B7C36DAC35D448C81938122EA8C7C1B&format=xml'
        print new_url

        html = urlopen(new_url).read()
        soup = BeautifulSoup(html, 'lxml')

        # parse key attributes
        keys = soup.products.attributegroups.find_all('key')
        key_list = list(['Id'])

        for eachKey in keys:
            key_list.append(eachKey.string)

        # check for dupes, if found, ignore the row and move to the next
        if len(key_list)!=len(set(key_list)):
            print 'dupe found' + str(get_id) + ' line: ' + str(i)
        else:
            print 'Line: ' + str(i) + ' Parsing book ID :' + str(get_id)
            # parse value attributes
            values = soup.products.attributegroups.find_all('value')
            value_list = list([get_id])
            for eachValue in values:
                value_list.append(eachValue.string)

            # Dump key/values into array
            arr_val = np.array([value_list])

            # build dataframe
            if i == 1:
                df = pd.DataFrame(arr_val, columns=key_list)
            else:
                df2 = pd.DataFrame(arr_val, columns=key_list)
                df = concat([df, df2], ignore_index=True)

    return df


def get_pubdates(book_id_list):
    summary = []
    color = []
    isbn = []

    for eachIsbn in book_id_list:
        try:
            url = 'https://api.bol.com/catalog/v4/products/' + str(
                eachIsbn[0]) + '/?apikey=AFF492148CFC4491B29E53C183B05BF2&format=xml'
            html = urlopen(url).read()
            soup = BeautifulSoup(html, 'lxml')

            soup.productlist.products.summary.string
            isbn.append(eachIsbn[0])
            color.append(eachIsbn[1])
            summary.append(soup.productlist.products.summary.string)
        except:
            e = sys.exc_info()[0]
            print ( "Error: %s" % e )

    result = zip(isbn, color, summary)
    return result


output = get_pubdates(result)

import pickle
pickle.dump(output, open('color_covers_types_pubdate.pickle', "w"))
pickle.dump(result, open('color_covers.pickle', "w"))
result = pickle.load(open("color_covers.pickle", "r"))

import csv

myfile = open('color_covers_types_pubdate.csv', 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerow(output)

isbn = list()
color = list()
detail = list()
for i in range(0, len(output) - 1):
    isbn.append(output[i][0])
    color.append(output[i][1])
    detail.append(output[i][2])

output_final = zip(isbn, color, detail)

import csv

myfile = open('color_covers_types_pubdate.csv', 'wb')
csv_writer = csv.writer(myfile, delimiter='\t')
rows = output
csv_writer.writerows(rows)

idlist = ('9789029576291',
          '9789029577908',
          '9789029579735',
          '9789029580151',
          '9789029582193',
          '9789029574983',
          '9789029575249',
          '9789029575317',
          '9789029575317',
          '9789029578592',
          '9789029573580',
          '9789029573580',
          '9789029573580',
          '9789029586115',
          '9789029573580',
          '9789029575935',
          '9789029576048',
          '9789029578592',
          '9789029573580',
          '9789029584869',
          '9789029573580',
          '9789029575935',
          '9789029575935',
          '9789029578592',
          '9789029578592',
          '9789029575935',
          '9789029578592',
          '9789029586092',
          '9789029575980',
          '9789029578592',
          '9789029575935',
          '9789029592611')