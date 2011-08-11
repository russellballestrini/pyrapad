<%inherit file="base.mako" />

##<div class="twelve columns">
<div class="ten columns">

  <h1>add a pad ...</h1>
  
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
      placeholder="python, c++, perl, java, ect ... we guess poorly"
      />
      
    <label for="data">data</label>
    <textarea name="data" rows="12" style="width:100%;" placeholder="data"></textarea>
    <input type="submit" value="submit" name="form.submitted"></input>
  </form>

</div>

<div class="three columns">
   <nav>
     <h3>how to ...</h3>

     <ol>
       <li> Chose an optional markup syntax. </li>
       <li> Paste your text data into <a href="http://pyrapad.com">Pyrapad</a>. </li>
       <li> Hit submit to save and share! </li>
     </ol>

     <h3>say no to ...</h3>
     <ol>
       <li> usernames </li>
       <li> passwords </li>
       <li> registration </li>
       <li> captchas </li>
       ##<li> manditory fields </li>
       <li> rules </li>
     </ol>

     <h3>say yes to ...</h3>
     <ol>
       ##<li> syntax prediction </li>
       <li> syntax highlighting </li>
       <li> pad replies </li>
       <li> generated uri's </li>
       <li> human readable uri's </li>
     </ol>
   </nav>
</div>
