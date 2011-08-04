<%inherit file="base.mako" />

<h1>${paste.uri.replace('-',' ')}</h1>

<div class="paste">${pygpaste}</div>
<br/>
% for node in pygnodes:
<br/>
<div class="node">${node}</div>
% endfor

<form action="/${paste.id}/reply">
<ul>
  <li>
    data <textarea name="data">${paste.data}</textarea>
  </li>
  <li>
    <select name="syntax">
      <option value="${paste.syntax}">${paste.syntax}</option>
      <option value="python">python</option>
      <option value="c++">c++</option>
    </select>
  </li>
  <li>
    <input type="submit" value="paste" name="form.submitted"></input>
  </li>
</ul>
</form>
