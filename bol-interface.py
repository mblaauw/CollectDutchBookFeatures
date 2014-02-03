#################################################################################
# MODULE: bol-interface
#################################################################################

def get_isbn_list(category='thrillers', test=True):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')

    unique = list()

    for eachRow in list(soup.find_all('a', 'product_name')):
        unique.append(eachRow.get('href'))

    # collect the motherload (minus one, cause less results on final page)
    # determine maxmimum results and devide bij 12 (results per page)
    total_nr_of_items = re.sub('<[^>]+>', '', str(soup.find('span', 'tst_searchresults_nrFoundItems')))
    total_nr_of_items = int(round(int(float(total_nr_of_items.replace('.', ''))) / 12))

    if test:
        total_nr_of_items = 10

    for eachItem in range(1, total_nr_of_items):
        # Get LITERATURE Cat - Est. 10000
        if category.lower() == 'thrillers':
            new_url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-thrillers/N/261+8293/No/' + str(
                eachItem * 12) + '/section/books/index.html'

        # Get LITERATURE Cat - Est. 45000
        if category.lower() == 'literature'
        new_url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-literatuur-nieuw/N/87+8293+14033/No/' + str(
            eachItem * 12) + '/section/books/index.html'

    html = urlopen(new_url).read()
    soup = BeautifulSoup(html, 'lxml')

    for eachRow in list(soup.find_all('a', 'product_name')):
        unique.append(eachRow.get('href'))

# clean the list and return from function
unique_result = list()
for i in range(1, len(unique)):
    unique_result.append(str(unique[i]).split('/')[6])

return unique_result


def get_book_details(isbn_list, test=True):
    # ['Timestamp', 'BOL_Key', 'EAN', 'GPC', 'Title', 'Price', 'Rating', 'Summary']
    # isbn10, isbn13, EAN, GPC
    # Pubdate, Uitgever, Vertaald uit,
    # Title, Subtitle
    # Taal, Vertaald uit
    # short desc/longdesc
    # Auteurs
    print isbn_list


def get_book_covers(isbn_list, output_folder='./data/covers/'):
    print isbn_list

