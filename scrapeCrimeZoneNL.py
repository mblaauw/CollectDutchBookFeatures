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



soup.find_all('a','normal')
