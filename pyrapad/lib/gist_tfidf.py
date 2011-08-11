import tfidf
import os

def cleansourcecode( document ):
    """Replace all Non Alpha Numeric and Non space chars with a space"""
    # Also setting words to lower here... is this bad?
    return ''.join( e.lower() if e.isalnum() or e.isspace() else ' ' for e in document )

path = '/home/fox/hg/pyrapad/pyrapad/lib/gist/'

documentList = os.listdir( path )

# choose a subject from the documentList and read it into subject
subject = open( path + documentList[29], 'r' ).read()

print subject

# read in EVERY file into the documentList, also run clean code on each
documentList = [ cleansourcecode( open( path + document, 'r' ).read() ) for document in documentList ]

subject = cleansourcecode( subject )

documentList.append( subject )

subjectwords = subject.split()

scores = {} 

# At this point I'm not taking into account
# multiple occurances of the same word.
# multiple occurances should weigh more
# maybe score += score * count / 10
#
# score of .20 with a word count of 3 would be
# score = .20 + .20 * 3 / 10
# >>> score = 0.26
#
# score of .20 with a word count of 9 would be
# score = .20 + .20 * 9 / 10
# >>> score = 0.38

for word in subjectwords:
    #print tfidf.tfidf( word, document2, documentList )
    scores[word] = tfidf.tfidf( word, subject, documentList ) 

# reverse sort dict by word scores
# creates a list out of the dict 
scorelist = sorted( scores.items(), key=lambda x: x[1], reverse=True )
# from operator import itemgetter
# scorelist = sorted( scores.items(), key=itemgetter(1), reverse=True )

# top keywords for subject document
topsix = scorelist[0:6]

# print sorted scores to the screen
for score in scorelist: 
    print score

# create the url string for subject document
slug = '-'.join( word[0] for word in topsix )    

print slug
