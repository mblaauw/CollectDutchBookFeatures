__author__ = 'MBlaauw'
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")

import re
import pandas as pd
from bs4 import BeautifulSoup
from urllib2 import urlopen
# http://www.crimezone.nl/web/Titels/Verschenen.htm?pagenr=1&queryElement=592958&sorton=rating%20desc
# http://www.crimezone.nl/web/Auteurs.htm?pagenr=1&queryElement=618064


def get_titles_rating():

    l_isbn = list()
    l_rating = list()

    for i in range(1, 399):
        new_url = 'http://www.crimezone.nl/web/Titels/Verschenen.htm?pagenr=' + str(i) + '&queryElement=592958&sorton=rating%20desc'

        html = urlopen(new_url).read()
        soup = BeautifulSoup(html, 'lxml')
        soup = BeautifulSoup(str(soup.find_all('div',{'id' : 'main-content'})), 'lxml')

        isbn = soup.find_all('div', 'query-field-div title')
        for eachTitle in isbn:
            for i in eachTitle.find_all('a'):
                l_isbn.append(re.findall('\d+', i['href']))

        rating = soup.find_all('div', class_= re.compile('t\d+'))
        for eachRating in rating:
            l_rating.append(eachRating.text.strip())

        print len(l_rating)

    result = zip(l_isbn, l_rating)
    return result


def get_author_rating():

    l_person_name = list()
    l_first_name = list()
    l_last_name = list()
    l_suffix = list()
    l_avg_rating = list()

    for i in range(1, 97):

        new_url = 'http://www.crimezone.nl/web/Auteurs.htm?pagenr=' + str(i) + '&queryElement=618064'
        print new_url

        html = urlopen(new_url).read()
        soup = BeautifulSoup(html, 'lxml')
        soup = BeautifulSoup(str(soup.find_all('div',{'id' : 'main-content'})), 'lxml')

        person_name = soup.find_all('div', 'query-field-div person_name')
        first_name = soup.find_all('div', 'query-field-div firstname')
        last_name = soup.find_all('div', 'query-field-div lastname')
        suffix = soup.find_all('div', 'query-field-div suffix')
        avg_rating = soup.find_all('div', 'query-field-div avgrating')

        for eachPerson in person_name:
            l_person_name.append(eachPerson.text.strip())

        for eachFirstName in first_name:
            l_first_name.append(eachFirstName.text.strip())

        for eachLastName in last_name:
            l_last_name.append(eachLastName.text.strip())

        for eachSuffix in suffix:
            l_suffix.append(eachSuffix.text.strip())

        for eachAvgRating in avg_rating:
            l_avg_rating.append(eachAvgRating.text.strip())

    result = zip(l_person_name,
                 l_last_name,
                 l_first_name,
                 l_suffix,
                 l_avg_rating)
    return result

# selftest
title_rating = get_titles_rating()
author_rating = get_author_rating()

df_title_rating = pd.DataFrame(title_rating, columns=('isbn','rating'))
df_author_rating = pd.DataFrame(author_rating, columns=('PersonName','LastName','FirstName','Suffix','Rating'))

df_title_rating.to_excel('crimezone_title_ratings.xls')
df_author_rating.to_excel('crimezone_author_rating.xls')