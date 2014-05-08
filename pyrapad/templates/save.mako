<%inherit file="base.mako" />

  <div class="dinker">></div>
  <form action="/save" method="post">
    <textarea name="data" spellcheck="false" autofocus>${data}</textarea>
    <label for="semail" class="semail">email</label>
    <input
      id="semail" 
      name="semail" 
      class="semail" 
      type="text" 
      style="width:100%;" 
      placeholder="you@example.com"
      />
    <input type="hidden" name="pad_id" value="${pad_id}"/>
  </form>
