<%inherit file="base.mako" />

<div class="ten columns">

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
      <input name="syntax" value="${paste.syntax}" style="width:100%;" placeholder="${paste.syntax}"></input>
      <label for="data">data</label>
      <textarea name="data" rows="${ len( paste.data.split('\n') ) + 2 }" style="width:100%;">${paste.data}</textarea>
      <input type="submit" value="submit" name="form.submitted"></input>
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
