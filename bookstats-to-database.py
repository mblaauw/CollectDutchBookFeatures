#-------------------
import sqlite3
conn = sqlite3.connect('/Users/mich/Calibre Library/metadata.db')
c = conn.cursor()

c.execute('SELECT * FROM stocks')
print c.fetchone()

conn.close()





#-------------------

__author__ = 'mich'
import os
import sys
import readability as red

input_folder = '/Users/mich/datascience-projects/dutch-text-analytics/data/misc-nl/'
input_ext = '*.txt'

def getScores():
    readability_score = list()

    for file in os.listdir(input_folder):
        current = os.path.join(input_folder, file)

        if os.path.isfile(current):
            file = open(current, 'r')
            txt = file.read()
            txt = str(unicode(txt, errors='ignore'))

            readability_score.append([red.Readability(txt).ARI(),
                          red.Readability(txt).ColemanLiauIndex(),
                          red.Readability(txt).FleschKincaidGradeLevel(),
                          red.Readability(txt).FleschReadingEase(),
                          red.Readability(txt).GunningFogIndex(),
                          red.Readability(txt).LIX(),
                          red.Readability(txt).RIX(),
                          red.Readability(txt).SMOGIndex()])

    return readability_score
print getScores()

#-------------------



book = '/Users/mich/Downloads/Ebooks/[NL] 2010 - Schikken of stikken - Rianne Verwoert.epub'

import zipfile
from lxml import etree

def get_epub_info(fname):
    ns = {'n':'urn:oasis:names:tc:opendocument:xmlns:container',
          'pkg': 'http://www.idpf.org/2007/opf',
          'dc':'http://purl.org/dc/elements/1.1/'}
    zip = zipfile.ZipFile(fname)

    # find the contents metafile
    txt = zip.read('META-INF/container.xml')
    tree = etree.fromstring(txt)
    cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path', namespaces=ns)[0]

    # grab the metadata block from the contents metafile
    cf = zip.read(cfname)
    tree = etree.fromstring(cf)
    p = tree.xpath('/pkg:package/pkg:metadata', namespaces=ns)[0]

    # repackage the data
    res = {}
    for s in ['title', 'language', 'creator', 'date', 'identifier']:
        res[s] = p.xpath('dc:%s/text()' % (s), namespaces=ns)[0]

    return res


get_epub_info(book)