__author__ = 'mich'
import nltk

# Read the file
f = open('/Users/mich/datascience-projects/dutch-text-analytics/data/misc-nl/Ben Hur - Lewis Wallace.txt')

# Each sentence stored in line
data = f.readlines()

for line in data:
  # Tokenize each line
  tokens = nltk.word_tokenize(line)
  # Apply POS Tagger on tokens
  tagged = nltk.pos_tag(tokens)
  # NE chunking on tags
  entities = nltk.chunk.ne_chunk(tagged)
  print entities

f.close()









import nltk
sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
tokens = nltk.word_tokenize(sentence)
tokens

tagged = nltk.pos_tag(tokens)
tagged[0:6]

entities = nltk.chunk.ne_chunk(tagged)
entities