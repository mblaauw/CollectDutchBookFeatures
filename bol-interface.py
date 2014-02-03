#################################################################################
# MODULE: bol-interface
#################################################################################

def get_isbn_list(category='thrillers', test=True):
    if category.lower() == 'thrillers':
        print category


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

