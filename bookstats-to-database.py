__author__ = 'mich'

import os
import sys
import readability as red



input_folder = '/Users/mich/datascience-projects/dutch-text-analytics/data/misc-nl/Anna Karenina - Leo Nikolaj Tolstoj.txt'
input_ext = '*.txt'


file = open(input_folder, 'r')

txt = file.read()


red.Readability(txt).ARI()
red.Readability(txt).ColemanLiauIndex()
red.Readability(txt).FleschKincaidGradeLevel()
red.Readability(txt).FleschReadingEase()
red.Readability(txt).GunningFogIndex()
red.Readability(txt).LIX()
red.Readability(txt).RIX()
red.Readability(txt).SMOGIndex()





for file in os.listdir(input_folder):
    current = os.path.join(input_folder, file)
    if os.path.isfile(current):
        data = open(current, "r")
        text = data.read()
        rd = red.Readability(text)

        rd.ARI()



data = open(current, "r")