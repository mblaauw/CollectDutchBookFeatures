__author__ = 'MBlaauw'
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")

import pandas as pd
from pandas import concat
import numpy as np
from bs4 import BeautifulSoup
from urllib2 import urlopen

# http://www.crimezone.nl/web/Titels/Verschenen.htm?pagenr=1&queryElement=592958&sorton=rating%20desc
# http://www.crimezone.nl/web/Auteurs.htm?pagenr=1&queryElement=618064

def get_titles():
    for i in range(0,440):

        i = 1
        new_url = 'http://www.crimezone.nl/web/Titels/Verschenen.htm?pagenr=' + str(i) + '&queryElement=592958&sorton=rating%20desc'
        print new_url

        html = urlopen(new_url).read()
        soup = BeautifulSoup(html, 'lxml')

        soup.find_all('a','normal')
        x = soup.find_all('div','query-field-div  person_name')
        for eachOne in x:
            print str(eachOne).strip()





            # soup.find_all('div','query-field-div rating pct100')



l_person_name = list()
l_firstname = list()
l_lastname = list()
l_suffix = list()
l_avg_rating = list()


for i in range(68,97):

    new_url = 'http://www.crimezone.nl/web/Auteurs.htm?pagenr=' + str(i) + '&queryElement=618064'
    print new_url

    html = urlopen(new_url).read()
    soup = BeautifulSoup(html, 'lxml')

    person_name = soup.find_all('div','query-field-div person_name')
    firstname = soup.find_all('div','query-field-div firstname')
    lastname= soup.find_all('div','query-field-div lastname')
    suffix = soup.find_all('div','query-field-div suffix')
    avgrating = soup.find_all('div','query-field-div avgrating')

    for eachPerson in person_name:
        l_person_name.append(eachPerson.text.strip())

    for eachFirstname in firstname:
        l_firstname.append(eachFirstname.text.strip())

    for eachLastname in lastname:
        l_lastname.append(eachLastname.text.strip())

    for eachSuffix in suffix:
        l_suffix.append(eachSuffix.text.strip())

    for eachAvgRating in avgrating:
        l_avg_rating.append(eachAvgRating.text.strip())


result = zip(l_person_name,
    l_lastname,
    l_firstname,
    l_suffix,
    l_avg_rating)
