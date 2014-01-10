__author__ = 'MBlaauw'
import re, time, datetime, numpy as np, pandas as pd
from pandas import concat
from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+5260+7373+16638+14033/index.html'


def get_bol_book_list(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')

    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    columns = ['Timestamp', ['BOL_Key'], 'Author', 'Title', 'Pubdat', 'Rating']

    for i in range(1,13):
        # collect and clean data
        item = BeautifulSoup(str(soup.find_all('div', 'product_content tst_searchresults_details_' + str(i))), 'lxml')
        unique = str(item.find_all('a', 'product_name')).split('/')[6]
        title = str(item.find_all('a', 'product_name')).split('/')[7][25:-1]
        title = title[:title.find('">')]
        pubdat = str(item.find_all(itemprop='datePublished'))[16:20]
        rating = str(item.find_all(itemprop='ratingValue'))[16:19]
        author = re.sub('<[^>]+>', '', str(item.find_all(itemprop='author')))

        # build array and then data frame
        arr = np.array([[timestamp], [unique], [author], [title], [pubdat], [rating]]).T
        if i == 1:
            df = pd.DataFrame(arr, columns=columns)
        else:
            df2 = pd.DataFrame(arr, columns=columns)
            df = concat([df, df2], ignore_index=True)

    return df
    # determine maxmimum results and devide bij 12 (results per page)
    total_nr_of_items = re.sub('<[^>]+>', '', str(soup.find('span', 'tst_searchresults_nrFoundItems')))
    total_nr_of_items = int(round(int(float(total_nr_of_items.replace('.', '')))/12))

    # collect the motherload (minus one, cause less results on final page)
    for eachItem in range(1, total_nr_of_items):
        print 'Scraping link number: ' + str(eachItem)
        newurl = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+14033/No/' + str(eachItem * 12) + '/section/books/index.html'
        html = urlopen(newurl).read()
        soup = BeautifulSoup(html, 'lxml')

        for i in range(1, 13):
            # collect and clean data
            item = BeautifulSoup(str(soup.find_all('div', 'product_content tst_searchresults_details_' + str(i))), 'lxml')
            unique = str(item.find_all('a', 'product_name')).split('/')[6]
            title = str(item.find_all('a', 'product_name')).split('/')[7][25:-1]
            title = title[:title.find('">')]
            pubdat = str(item.find_all(itemprop='datePublished'))[16:20]
            rating = str(item.find_all(itemprop='ratingValue'))[16:19]
            author = re.sub('<[^>]+>', '', str(item.find_all(itemprop='author')))

            # build array and then data frame
            arr = np.array([[timestamp], [unique], [author], [title], [pubdat], [rating]]).T
            df2 = pd.DataFrame(arr, columns=columns)
            df = concat([df, df2], ignore_index=True)

    # return the final results
    # time.sleep(1)
    return df


def get_bol_book_details(df):

    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    for i, row in enumerate(df.values):
        new_url = 'https://api.bol.com/catalog/v4/products/' + row[1] + '/?apikey=AFF492148CFC4491B29E53C183B05BF2&format=xml'

        html = urlopen(new_url).read()
        s = BeautifulSoup(html, 'lxml')

        values = s.find_all('value')

        # todo: clean this up, get the right attribute its mixing up as not all html is formed the same
        taal = values[1].string
        afmeting = values[2].string
        gewicht = values[3].string
        druk = values[4].string
        isbn10 = values[5].string
        isbn13 = values[6].string
        auteur = values[7].string
        uitgever = values[8].string

        print taal

        # build array and then data frame
        arr = np.array([[timestamp],
                        [s.id.string],
                        [s.ean.string],
                        [s.gpc.string],
                        [s.title.string],
                        [s.rating.string],
                        [taal],
                        [afmeting],
                        [gewicht],
                        [druk],
                        [isbn10],
                        [isbn13],
                        [auteur],
                        [uitgever]
                        ]).T

        if i == 1:
            df = pd.DataFrame(arr)
        else:
            df2 = pd.DataFrame(arr)
            df = concat([df, df2])

    return df

x = get_bol_book_details(test)



test = get_bol_book_list(BASE_URL)
test.to_csv('out3.csv')



# todo: take dataframe and parse through BOL API and collect: ISBN10-13, Image URL, Afmeting, Gewicht, Druk, Uitgever,

# https://api.bol.com/catalog/v4/products/9200000015494232/?apikey=AFF492148CFC4491B29E53C183B05BF2&format=xml
