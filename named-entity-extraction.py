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


# TEST 2
import nltk
sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
tokens = nltk.word_tokenize(sentence)
tokens

tagged = nltk.pos_tag(tokens)
tagged[0:6]

entities = nltk.chunk.ne_chunk(tagged)
entities








# Approach3
str = 'Christiane heeft een lam.'

tagger = nltk.data.load('taggers/dutch.pickle')
chunker = nltk.data.load('chunkers/dutch.pickle')

str_tags = tagger.tag(nltk.word_tokenize(str))
print str_tags

str_chunks = chunker.parse(str_tags)
print str_chunks




















