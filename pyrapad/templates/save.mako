<%inherit file="base.mako" />

  <div class="dinker">></div>
  <form action="/save" method="post">
    <textarea name="data_form" spellcheck="false" autofocus>${data}</textarea>
    <label for="semail" class="semail">email</label>
    <input
      id="semail" 
      name="semail" 
      class="semail" 
      type="text" 
      style="width:100%;" 
      placeholder="you@example.com"
      />
  </form>
