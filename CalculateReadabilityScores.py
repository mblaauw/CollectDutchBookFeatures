from droopy import Droopy
from droopy.static import Static
from droopy.lang.english import English

text = Droopy("Just a simple test")
text.add_bundles(Static(), English())

print text.nof_words # print number of words
print text.nof_syllables # print number of syllables
print text.