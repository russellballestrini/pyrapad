<%inherit file="base.mako" />

<form action="/add">
<ul>
  <li>
    uri <input value="${uri}" name="uri"></input>
  </li>
  <li>
    data <textarea name="data">${data}</textarea>
  </li>
  <li>
    syntax <textarea name="syntax"></textarea>
  </li>
  <li>
    <input type="submit" value="paste" name="form.submitted"></input>
  </li>
</ul>
</form>
