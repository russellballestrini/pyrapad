<%inherit file="base.mako" />

  <div class="dinker">></div>
  <form action="/add" method="post">
    <textarea name="data" spellcheck="false" autofocus></textarea>
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
