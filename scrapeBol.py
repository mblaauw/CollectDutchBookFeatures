__author__ = 'MBlaauw'
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")

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
    for i in range(1, len(book_id_list)):
        # DUMMY
        get_id = book_id_list[i]
        new_url = 'https://api.bol.com/catalog/v4/products/' + str(get_id) + '/?apikey=6B7C36DAC35D448C81938122EA8C7C1B&format=xml'
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


# Self test
init = get_bol_book_list(BASE_URL, test=False)
attr1 = get_bol_book_attributes(init[0:5000])
attr2 = get_bol_book_attributes(init[5000:10630])
details1 = get_bol_book_details(init[0:5000])

details2 = get_bol_book_details(init[5000:10630])
details2.to_excel('details2_list.xls')

details1.to_csv('details1_list.csv')

details2.to_excel('details2_list.xls')
details1.to_excel('details1_list.xls')



details2.to_csv('details2_list.csv')

attr1.to_csv('attr1.csv')
attr2.to_csv('attr2.csv')





#
# Couchdb logic. Store all data in order to evalutate change over time
#
import couchdb
import json
couch = couchdb.Server()  # assumes CouchDB is running on localhost:5894
couch.delete('test')
db = couch.create('bolcom') # newly created

# build ID column
init_list = list()
for eachId in init:
    init_list.append('id')

# zip it up
zip_init = zip(init_list, init)

# store in db as key/value
for eachDict in zip_init:
    dict_init = dict(zip_init)
    db.save(dict_init)


# Collect all ID's from db




'''
import pickle
with open('init.pickle', 'wb') as handle:
  pickle.dump(init, handle)
with open('init.pickle','rb') as handle:
    init = pickle.load(handle)
test = get_bol_book_details(init)
print init
'''

    x =dict(id=init)

