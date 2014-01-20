__author__ = 'MBlaauw'
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")

import re
from bs4 import BeautifulSoup
from urllib2 import urlopen
# http://www.crimezone.nl/web/Titels/Verschenen.htm?pagenr=1&queryElement=592958&sorton=rating%20desc
# http://www.crimezone.nl/web/Auteurs.htm?pagenr=1&queryElement=618064

l_isbn = list()
l_rating = list()

for i in range(1,440):
    new_url = 'http://www.crimezone.nl/web/Titels/Verschenen.htm?pagenr=' + str(i) + '&queryElement=592958&sorton=rating%20desc'
    print new_url

    html = urlopen(new_url).read()
    soup = BeautifulSoup(html, 'lxml')

    isbn = soup.find_all('div', 'query-field-div title')
    for eachTitle in isbn:
        for i in eachTitle.find_all('a'):
            print i['href']
            l_isbn.append(re.findall('\d+', i['href']))

    rating = soup.find_all('div', 'query-field-div rating pct100')
    for eachRating in rating:
        l_rating.append(eachRating.text.strip())


result = zip(l_isbn,
             l_rating)












def get_titles_rating():
    for i in range(0,440):

        i = 1
        new_url = 'http://www.crimezone.nl/web/Titels/Verschenen.htm?pagenr=' + str(i) + '&queryElement=592958&sorton=rating%20desc'
        print new_url

        html = urlopen(new_url).read()
        soup = BeautifulSoup(html, 'lxml')


        l_person_name = list()
        l_first_name = list()
        l_last_name = list()
        l_suffix = list()
        l_avg_rating = list()

        person_name = soup.find_all('div', 'query-field-div person_name')
        title = soup.find_all('div', 'query-field-div title')


        for eachPerson in person_name:
            l_person_name.append(eachPerson.text.strip())

        for eachFirstName in first_name:
            l_first_name.append(eachFirstName.text.strip())


        result = zip(l_person_name,
                     l_last_name,
                     l_first_name,
                     l_suffix,
                     l_avg_rating)




def get_author_ratings():

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

