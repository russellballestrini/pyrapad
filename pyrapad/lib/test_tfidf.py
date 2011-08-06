import tfidf

word = 'pygnodes'

def cleansourcecode( document ):
    return ''.join( e if e.isalnum() or e.isspace() else ' ' for e in document )

document = """<%inherit file="base.mako" />

<div class="ten columns">

  <h3>add a pad...</h3>
  
  <form action="/add">

    <label for="uri">uri</label>
    <input 
      id="uri"
      name="uri"
      type="text"
      style="width:100%;" 
      placeholder="uri" 
      />

    <label for="syntax">syntax</label>
    <input
      id="syntax"
      name="syntax"
      type="text"  
      style="width:100%;" 
      placeholder="python, c++, perl, java, ect"
      />
      
    <label for="data">data</label>
    <textarea name="data" rows="10" style="width:100%;" placeholder="data"></textarea>
    <input type="submit" value="submit" name="form.submitted"></input>
  </form>

</div>
"""

document2 = """<%inherit file="base.mako" />

##<div class="ten columns">
<div class="nine columns content offset-by-one">

  <h3>${paste.uri.replace('-',' ')}</h3>
 
  <% replycount = len(pygnodes) %>

  % if replycount == 0:
    Be the first to <a href="#reply">reply</a> to this pad!
  % else:
    This pad has <a href="#replies">${len(pygnodes)} replies</a>
  % endif
  <br/>

  <hr/>

  <span class="paste">${pygpaste}</span>

  <br/>

  <hr/>

  <h3 id="reply">reply to this pad ...</h3>

  <form action="/${paste.id}/reply">

      <label for="syntax">syntax</label>
      <input 
        id="syntax" 
        name="syntax" 
        type="text" 
        value="${paste.syntax}" 
        style="width:100%;" 
        placeholder="${paste.syntax}" 
        />

      <label for="data">data</label>
      <textarea 
        id="data" 
        name="data" 
        rows="${ len( paste.data.split('\n') ) + 2 }" 
        style="width:100%;">${paste.data}</textarea>

      <input 
        type="submit" 
        value="submit" 
        name="form.submitted"
        />

  </form>

  % if replycount > 0:
    <h3 id="replies">replies ...</h3>
    % for node in pygnodes:
      <div class="node">${node}</div>
      <br/>
      <hr/>
    % endfor
  % endif

</div>

<div class="three columns sidebar">
</div>"""

#print document
#print document2

document = cleansourcecode( document )
document2 = cleansourcecode( document2 )

documentList = [ document, document2 ]

#print document
#print document2

#document = document.split()
#document2 = document2.split()

#print document
#print document2

#document = ' '.join( e for e in document )
#document2 = ' '.join( e for e in document2 )

#print document
#print document2

document2words = document.split()

scores = {} 

for word in document2words:
    #print tfidf.tfidf( word, document2, documentList )
    scores[word] = tfidf.tfidf( word, document, documentList ) 

# sort dict by value
# creates a list out of the dict 
topsix = sorted( scores.iteritems(), key=lambda item: -item[1] )[0:6]

slug = '-'.join( word[0] for word in topsix )    

print slug
