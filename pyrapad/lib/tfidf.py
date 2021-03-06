#!/usr/bin/env python

import math
from operator import itemgetter

def tf(word, document):
    return freq( word, document ) / float( wordCount( document ) )

def freq( word, document ):
    return document.split().count( word )

def wordCount( document ):
    return len( document.split() )

def idf(word, documentList):
    try:
        return math.log( len( documentList ) / numDocsContaining( word, documentList ) )
    except ZeroDivisionError:
        return False

def numDocsContaining( word, documentList ):
    count = 0
    for document in documentList:
      if freq( word,document ) > 0:
        count += 1
    return count

def tfidf( word, document, documentList ):
  if len( word ) > 2: # prevent 1 and 2 letter words from scoring
      return ( tf( word, document ) * idf( word,documentList ) )
  else:
      return False

if __name__ == '__main__':
    documentList = []
    documentList.append("""DOCUMENT #1 TEXT""")
    documentList.append("""DOCUMENT #2 TEXT""")
    documentList.append("""DOCUMENT #3 TEXT""")
    words = {}
    documentNumber = 0
    for word in documentList[documentNumber].split(None):
        words[word] = tfidf( word, documentList[documentNumber], documentList )
    for item in sorted( words.items(), key=itemgetter(1), reverse=True ):
        print "%f <= %s" % (item[1], item[0])
