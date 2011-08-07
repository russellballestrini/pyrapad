<%inherit file="base.mako" />

##<div class="ten columns">
##<div class="nine columns content offset-by-one">
<div class="twelve columns content offset-by-one">

  <h1>${paste.uri.replace('-',' ').title()}</h1>
 
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

  <h2 id="reply">reply to this pad ...</h2>

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
</div>
