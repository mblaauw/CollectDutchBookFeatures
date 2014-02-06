__author__ = 'MBlaauw'
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")

import Image
import scipy
import scipy.misc
import scipy.cluster
import os
import re
import sys
from bs4 import BeautifulSoup
import urllib
from urllib2 import urlopen


BASE_URL = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-literatuur-nieuw/N/87+8293+14033/No/0/section/books/index.html'
#BASE_URL = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+14033/No/0/section/books/index.html'

# Get list of unique product ID's
def get_bol_book_cover_list(url, test=True):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')
    unique = list()

    # collect the motherload (minus one, cause less results on final page)
    # determine maxmimum results and devide bij 12 (results per page)
    total_nr_of_items = re.sub('<[^>]+>', '', str(soup.find('span', 'tst_searchresults_nrFoundItems')))
    total_nr_of_items = int(round(int(float(total_nr_of_items.replace('.', '')))/12))

    # check for test run to save on waiting time
    if test:
        total_nr_of_items = 2000

    # Collect all IMG tages and filter out the proper ones
    for eachItem in range(1, total_nr_of_items):
        print 'Scraping link number: ' + str(eachItem)

        #new_url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+14033/No/' + str(eachItem * 12) + '/section/books/index.html'
        new_url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-literatuur-nieuw/N/87+8293+14033/No/' + str(eachItem * 12) + '/section/books/index.html'
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

            tmp_isbn = str(eachLine).split('"')[5].split('/')
            tmp_isbn = tmp_isbn[len(tmp_isbn)-1]
            isbn.append(tmp_isbn[:-4])

    return zip(isbn, title, img)


# download physical
def download_covers_files_to_folder(input_list, output_folder= './data/covers/'):
    for eachItem in testresult:
        output_file = output_folder + eachItem[0] + '.jpg'
        urllib.urlretrieve(eachItem[2], filename=output_file)


# Calculate color values for all downloaded images
def tag_images_with_color_value(NUM_CLUSTERS = 5, INPUT_FOLDER = './data/covers/'):

    isbn = list()
    cover_color = list()

    files = os.listdir(INPUT_FOLDER)
    for eachFile in files:
        print eachFile
        try:
            im = Image.open(INPUT_FOLDER + eachFile)
            im = im.resize((50, 50))                          # optional, to reduce time
            ar = scipy.misc.fromimage(im)
            shape = ar.shape

            if len(shape) == 2:
                ar = ar.reshape(scipy.product(shape[:1]), shape[1])
            else:
                ar = ar.reshape(scipy.product(shape[:2]), shape[2])

            # finding clusters
            codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
            # cluster centres:\n', codes

            vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
            counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

            index_max = scipy.argmax(counts)                    # find most frequent
            peak = codes[index_max]
            colour = ''.join(chr(c) for c in peak).encode('hex')

            isbn.append(eachFile[:-4])
            cover_color.append(colour)
        except:
            e = sys.exc_info()[0]
            print ( "Error: %s" % e )

    result = zip(isbn, cover_color)
    return result



testresult = get_bol_book_cover_list(BASE_URL, test=False)
download_covers_files_to_folder(testresult)

result = tag_images_with_color_value()

