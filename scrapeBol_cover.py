__author__ = 'MBlaauw'
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")


import re
from bs4 import BeautifulSoup
import urllib
from urllib2 import urlopen

BASE_URL = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-thrillers/N/261+8293+5260+7373+16638/index.html'


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

    return zip(isbn, title, img)

def download_covers_files_to_folder(input_list, output_folder= './data/covers/'):
    for eachItem in testresult:
        output_file = output_folder + eachItem[0] + '.jpg'
        urllib.urlretrieve(eachItem[2], filename=output_file)






testresult = get_bol_book_cover_list(BASE_URL, test=True)
download_covers_files_to_folder(testresult)


#   iterate through each pixel in an image and
#   determine the average rgb color

# you will need to install the PIL module
from PIL import Image

class PixelCounter(object):
  ''' loop through each pixel and average rgb '''
  def __init__(self, imageName):
      self.pic = Image.open(imageName)
      # load image data
      self.imgData = self.pic.load()
  def averagePixels(self):
      r, g, b = 0, 0, 0
      count = 0
      for x in xrange(self.pic.size[0]):
          for y in xrange(self.pic.size[1]):
              tempr,tempg,tempb = self.imgData[x,y]
              r += tempr
              g += tempg
              b += tempb
              count += 1
      # calculate averages
      return (r/count), (g/count), (b/count), count

if __name__ == '__main__':
  # assumes you have a test.jpg in the working directory!
  pc = PixelCounter('./data/covers/666748892.jpg')
  print "(red, green, blue, total_pixel_count)"
  print pc.averagePixels()


# for my picture the ouput rgb values are:
#   (red, green, blue, total_pixel_count)
#   (135, 122, 107, 10077696)
#
# you can see that my image had 10,077,696 pixels and python/PIL
#   still churned right through it!