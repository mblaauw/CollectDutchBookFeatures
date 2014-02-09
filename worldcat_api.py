__author__ = 'MICH'
import isbndb
import urllib
from bs4 import BeautifulSoup
import pickle

input_list  = pickle.load( open( "thr-covers.pickle", "rb" ) )

isbn = list()
author = list()
city = list()
ed = list()
form = list()
lang = list()
lccn = list()
oclcnum = list()
originallang = list()
publisher = list()
title = list()
url = list()
year = list()




def get_worldcat_metadata(input_list):
    for eachIsbn in input_list:
        url_start ='http://xisbn.worldcat.org/webservices/xid/isbn/'
        url_end = '?method=getMetadata&format=xml&fl=*'
        url_isbn = str(eachIsbn[0])
        url = url_start + url_isbn + url_end
        print url

        xml_file = urllib.urlopen(url)
        soup = BeautifulSoup(xml_file)

        isbn.append(url_isbn)

        if soup.find('rsp')['stat'] == 'ok':
            try:
                author.append(soup.find('isbn')['author'])
            except:
                author.append('')

            try:
                city.append(soup.find('isbn')['city'])
            except:
                city.append('')

            try:
                ed.append(soup.find('isbn')['ed'])
            except:
                ed.append('')

            try:
                form.append(soup.find('isbn')['form'])
            except:
                form.append('')

            try:
                lang.append(soup.find('isbn')['lang'])
            except:
                lang.append('')

            try:
                oclcnum.append(soup.find('isbn')['oclcnum'])
            except:
                oclcnum.append('')

            try:
                originallang.append(soup.find('isbn')['originallang'])
            except:
                originallang.append('')

            try:
                publisher.append(soup.find('isbn')['publisher'])
            except:
                publisher.append('')

            try:
                title.append(soup.find('isbn')['title'])
            except:
                title.append('')

            try:
                url.append(soup.find('isbn')['url'])
            except:
                url.append('')

            try:
                year.append(soup.find('isbn')['year'])
            except:
                year.append('')
        else:
            print 'Error response : ', soup.find('rsp')['stat']

    result = zip(isbn, author, title, city, ed, form, lang, oclcnum, originallang, publisher, url, year)
    return result


output = get_worldcat_metadata(input_list)


