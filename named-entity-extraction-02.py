__author__ = 'MBlaauw'
import nltk

# Read the file
f = open('/Users/mblaauw/Downloads/04_R_PROJECTS\DutchTextAnalytics/data/misc-nl/Ben Hur - Lewis Wallace.txt')

# Each sentence stored in line
data = f.readlines()
data = str(data)

tokens = nltk.word_tokenize(data)

pos_tags = nltk.pos_tag(tokens)

trees = nltk.ne_chunk(pos_tags)

for tree in trees.subtrees():
    etype = None
    if tree.node == "PERSON":
        etype = "PERSON"
    elif tree.node == "GPE":
        etype = "PLACE"
    if etype is not None:
        ne = " ".join([leaf[0] for leaf in tree.leaves()])
        tweet = data.replace(ne, "<" + etype + ">" + ne + "</" + etype + ">")
print data
