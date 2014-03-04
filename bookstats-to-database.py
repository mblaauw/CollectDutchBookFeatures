__author__ = 'mich'

import os
import sys
import readability

rd = readability.Readability

rd.ARI('dsadsdas')


input_folder = '/Users/mich/datascience-projects/dutch-text-analytics/data/misc-nl/'
input_ext = '*.txt'

for file in os.listdir(input_folder):
    current = os.path.join(input_folder, file)
    if os.path.isfile(current):
        data = open(current, "rb")
        text = data.read()



        print text