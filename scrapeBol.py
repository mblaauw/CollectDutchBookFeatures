__author__ = 'MICH'
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")

import re, time, datetime, numpy as np, pandas as pd
from pandas import concat
from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+5260+7373+16638+14033/index.html'


# Get list of unique product ID's
def get_bol_book_list(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')

    unique = list()

    for eachRow in list(soup.find_all('a', 'product_name')):
        unique.append(eachRow.get('href'))

    # collect the motherload (minus one, cause less results on final page)
    # determine maxmimum results and devide bij 12 (results per page)
    total_nr_of_items = re.sub('<[^>]+>', '', str(soup.find('span', 'tst_searchresults_nrFoundItems')))
    total_nr_of_items = int(round(int(float(total_nr_of_items.replace('.', '')))/12))

    for eachItem in range(1, total_nr_of_items):
        print 'Scraping link number: ' + str(eachItem)
        new_url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+14033/No/' + str(eachItem * 12) + '/section/books/index.html'

        html = urlopen(new_url).read()
        soup = BeautifulSoup(html, 'lxml')

        for eachRow in list(soup.find_all('a', 'product_name')):
            unique.append(eachRow.get('href'))

    return unique


# Get details per product ID's through API
def get_bol_book_details(book_id_list):

    # clean and extract ids before parse
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    columns = ['Timestamp', ['BOL_Key'], 'EAN', 'GPC', 'Author', 'Title', 'Summary', 'Rating', 'Attributes']

    #len(init)
    for i in range(1, 100):
        get_id = str(init[i]).split('/')[6]

        print get_id
        new_url = 'https://api.bol.com/catalog/v4/products/' + get_id + '/?apikey=AFF492148CFC4491B29E53C183B05BF2&format=xml'

        # collect detailed html
        html = urlopen(new_url).read()
        soup = BeautifulSoup(html, 'lxml')

        # trap the rating attribute. Sometimes doesnt exist. Zero them if this happens
        rating = soup.find_all('rating')
        if len(rating) == 0:
            rating = str(0)
        else:
            rating = soup.products.rating.string

        arr = np.array([[timestamp],
                        [soup.products.id.string],
                        [soup.products.ean.string],
                        [soup.products.gpc.string],
                        [soup.products.entitygroups.entities.value.contents],
                        [soup.products.title.string],
                        [soup.products.summary.string],
                        [soup.products.offerdata.price.string],
                        [soup.products.parentcategorypaths.contents],

                        [rating],
                        [soup.products.attributegroups.contents]]).T

        if i == 1:
            df = pd.DataFrame(arr, columns=columns)
        else:
            df2 = pd.DataFrame(arr, columns=columns)
            df = concat([df, df2], ignore_index=True)

    return df

# Self test
init = get_bol_book_list(BASE_URL)
test = get_bol_book_details(init)

test.to_csv('newlist.csv')





import pickle

with open('init.pickle', 'wb') as handle:
  pickle.dump(init, handle)




with open('init.pickle','rb') as handle:
    init = pickle.load(handle)


test = get_bol_book_details(init)
print init


# parse attributes
keys = soup.products.attributegroups.find_all('key')
values = soup.products.attributegroups.find_all('value')

arr_val = np.array([list(values)]).T
arr_key = np.array([list(keys)]).T


pd.DataFrame(tmp_arr, columns=list(keys)).T




for i in range(1, len(keys)):
    tmp_arr = np.array([[values[i].string], [values[i].string]])



    tmp_df = pd.DataFrame(tmp_arr, columns=list(keys[i]))
    tmp_df2 = pd.DataFrame(tmp_arr, columns=list(keys[i]))


    print tmp_df


