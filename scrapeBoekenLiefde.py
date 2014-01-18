__author__ = 'MBlaauw'
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")

import pandas as pd
from pandas import concat
import numpy as np
from bs4 import BeautifulSoup
from urllib2 import urlopen

# Reviews
# https://boekenliefde.nl/edition_reviews_get.api?key=47L0ss6cDInejrV8SpJmPk4AgxEZTpEXy0BNQzvQ&isbn=9789047201441&type=text&outputformat=xml

# Details
# https://boekenliefde.nl/edition_info_get.api?key=47L0ss6cDInejrV8SpJmPk4AgxEZTpEXy0BNQzvQ&isbn=9789047201441&outputformat=xml

# Load inititial ISBN list
isbn_file = open('unqiue_isbn10_list.txt', 'r')
lines = isbn_file.readlines()
lines = [line[:-1] for line in lines]

lines = lines[1:10]

columns = 'eachLine','title','author','productsize','productform','image','yearofpublication','numberofratings','averagerating','averagerating_five','numberofreviews','othercontributor','illustrated','translator','flaptext'

for eachLine in lines:
    new_url = 'https://boekenliefde.nl/edition_info_get.api?key=47L0ss6cDInejrV8SpJmPk4AgxEZTpEXy0BNQzvQ&isbn=' + str(eachLine) + '&outputformat=xml'
    print eachLine
    html = urlopen(new_url).read()
    soup = BeautifulSoup(html, 'xml')

    title = soup.response.find_all('title')
    for eachTitle in title:
        title = eachTitle.string

    author = soup.response.find_all('author')
    for eachAuthor in author:
        author = eachAuthor.string

    productsize = soup.response.find_all('productsize')
    for eachProdSize in productsize:
        productsize = eachProdSize.string

    productform = soup.response.find_all('productform')
    for eachProdForm in productform:
        productform = eachProdForm.string

    image = soup.response.find_all('image')
    for eachImage in image:
        image = eachImage.string

    yearofpublication = soup.response.find_all('yearofpublication')
    for eachYearOfPub in yearofpublication:
        yearofpublication = eachYearOfPub.string

    numberofratings = soup.response.find_all('numberofratings')
    for eachNumOfRatings in numberofratings:
        numberofratings = eachNumOfRatings.string

    averagerating = soup.response.find_all('averagerating')
    for eachAvgRating in averagerating:
        averagerating = eachAvgRating.string

    averagerating_five = soup.response.find_all('averagerating_five')
    for eachAvgRatingFive in averagerating_five:
        averagerating_five = eachAvgRatingFive

    numberofreviews = soup.response.find_all('numberofreviews')
    for eachNumOfRev in numberofreviews:
        numberofreviews = eachNumOfRev.string

    othercontributor = soup.response.find_all('othercontributor')
    for eachOtherContri in othercontributor:
        othercontributor = eachOtherContri.string

    illustrated = soup.response.find_all('illustrated')
    for eachIllustrate in illustrated:
        illustrated = eachIllustrate.string

    translator = soup.response.find_all('translator')
    for eachTrans in translator:
        translator = eachTrans.string

    flaptext = soup.response.find_all('flaptext')
    for eachFlap in flaptext:
        flaptext = eachFlap.string

    arr = np.array([[eachLine],
                    [title],
                    [author],
                    [productsize],
                    [productform],
                    [image],
                    [yearofpublication],
                    [numberofratings],
                    [averagerating],
                    [averagerating_five],
                    [numberofreviews],
                    [othercontributor],
                    [illustrated],
                    [translator],
                    [flaptext]
    ]).T

    if 'df' in locals() or 'df' in globals():
        df2 = pd.DataFrame(arr, columns=columns)
        df = concat([df, df2], ignore_index=True)
    else:
        df = pd.DataFrame(arr, columns=columns)





