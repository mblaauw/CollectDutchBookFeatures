__author__ = 'MBlaauw'
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")


import re
from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-thrillers/N/261+8293+5260+7373+16638/index.html'


# Get list of unique product ID's
def get_bol_book_covers(url, test=True):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')

    unique = list()

    # collect the motherload (minus one, cause less results on final page)
    # determine maxmimum results and devide bij 12 (results per page)
    total_nr_of_items = re.sub('<[^>]+>', '', str(soup.find('span', 'tst_searchresults_nrFoundItems')))
    total_nr_of_items = int(round(int(float(total_nr_of_items.replace('.', '')))/12))

    # check for test run to save on waiting time
    if test:
        total_nr_of_items = 10

    # Collect all IMG tages and filter out the proper ones
    for eachItem in range(1, total_nr_of_items):
        print 'Scraping link number: ' + str(eachItem)
        new_url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-thrillers/N/261+8293/No/' + str(eachItem * 12) + '/section/books/index.html'

        html = urlopen(new_url).read()
        soup = BeautifulSoup(html, 'lxml')

        for eachRow in list(soup.find_all('img')):
            if 'itemprop=' in str(eachRow) and '.jpg' in str(eachRow):
                unique.append(eachRow)

    # Break up links in three tuples: Title, ImgUrl and ISBN
    title = list()
    img = list()
    isbn = list()

    for eachLine in unique:
            title.append(str(eachLine).split('"')[1])
            img.append(str(eachLine).split('"')[5])
            isbn.append(str(eachLine).split('/')[11].split('"')[0][:-4])

    # collect pubyears
    rating = list()

    for eachIsbn in isbn:
        new_url = 'https://api.bol.com/catalog/v4/products/' + str(eachIsbn) +'/?apikey=AFF492148CFC4491B29E53C183B05BF2&format=xml'
        html = urlopen(new_url).read()
        soup = BeautifulSoup(html, 'lxml')

        rating = soup.productlist.products.rating.string

        rating.append(rating)

    return zip(isbn, title, img, rating)









testresult = get_bol_book_covers(BASE_URL, test=True)


parse_result = parse_image_list( testresult )


testresult2= [i for i in testresult if i.attribute == 'img']