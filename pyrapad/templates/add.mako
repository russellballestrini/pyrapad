<%inherit file="base.mako" />

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

