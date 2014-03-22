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

