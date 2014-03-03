__author__ = 'mich'
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

fuzz.ratio("this is a test", "this is a test!")

f = open('booklist.txt', 'r')
book_list = f.readlines()
f.close()

f = open('gea_lookup.txt', 'r')
lookup_list = f.readlines()
f.close()


ratios = list()
gea_book = list()
epub_book = list()


for eachLookup in lookup_list:
    find_book = eachLookup
    for eachBook in book_list:
        ratio = fuzz.token_sort_ratio(find_book, eachBook)
        if ratio > 70:
            ratios.append(ratio)
            gea_book.append(find_book)
            epub_book.append(eachBook)


result = zip(ratios, gea_book, epub_book)

print result

with open('output.txt','w') as file:
    for item in result:
        print>>file, item