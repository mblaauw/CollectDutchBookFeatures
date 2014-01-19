__author__ = 'MBlaauw'


# Load ISBN, Title, Write from masterlist
from xlrd import open_workbook,XL_CELL_TEXT

book = open_workbook('masterlist.xls')
sheet = book.sheet_by_index(0)
cell = sheet.cell(0,0)

lookup_list = list()
for i in range(1, sheet.nrows):
    lookup_list.append([sheet.cell_value(i, 2), sheet.cell_value(i, 7)])



isbn_file = open('NL_physical_booklist.txt', 'r')
physical_books = isbn_file.readlines()
physical_books = [line[:-1] for line in physical_books]

# fuzzy matching
import difflib
# for i in range(len(lookup_list)):
winner = 0

for i in range(1, 10):    
    # find highest match in physicals
    for eachPhysical in physical_books:
        ratio = difflib.SequenceMatcher(None, eachPhysical, lookup_list[i][1]).ratio()
        if winner < ratio:
            winner = ratio
            winner_isbn = lookup_list[i][0]
        
