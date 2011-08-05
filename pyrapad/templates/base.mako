<html>
<!doctype html> 
<!--[if lt IE 7 ]><html class="ie ie6" lang="en"> <![endif]--> 
<!--[if IE 7 ]><html class="ie ie7" lang="en"> <![endif]--> 
<!--[if IE 8 ]><html class="ie ie8" lang="en"> <![endif]--> 
<!--[if (gte IE 9)|!(IE)]><!--><html lang="en"> <!--<![endif]--> 

<head> 

  <!-- Basic Page Needs
  ================================================== -->

  <title>${title} - ${request.host}</title>

  <meta charset="utf-8" /> 
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <meta name="keywords" content="${request.host}" />
  <meta name="description" content="${title.replace('-', ' ')} ${request.host}" />
  <meta name="author" content="http://russell.ballestrini.net"> 

  <!--[if lt IE 9]>
    <script static/skel="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
  <![endif]--> 

  <!-- Mobile Specific Metas
  ================================================== --> 

  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" /> 
 
  <!-- CSS
  ================================================== --> 

  <link rel="stylesheet" href="/static/skel/stylesheets/base.css"> 
  <link rel="stylesheet" href="/static/skel/stylesheets/skeleton.css"> 
  <link rel="stylesheet" href="/static/skel/stylesheets/layout.css"> 
 
  <!-- Favicon
  ================================================== --> 

  <link rel="shortcut icon" href="/static/skel/images/favicon.ico"> 
  <link rel="apple-touch-icon" sizes="57x57" href="/static/skel/images/apple-touch-icon.png"> 
  <link rel="apple-touch-icon" sizes="72x72" href="/static/skel/images/apple-touch-icon-72x72.png" /> 
  <link rel="apple-touch-icon" sizes="114x114" href="/static/skel/images/apple-touch-icon-114x114.png" /> 

  <!-- Pygments
  ================================================== --> 

  <link rel=stylesheet HREF="/static/pygments/pygments-tango.css" TYPE="text/css"> 
  ##<link rel=stylesheet HREF="/static/pygments/colorful.css" TYPE="text/css"> 

${ google_analytics() }

</head>
<body>

  <div class="container"> 
    <div class="three columns sidebar"> 
      <nav> 
        <h3 id="logo">pyrapad.com</h3> 
        <ul> 
          <li><a href="/">add a pad</a></li> 
          <li><a href="/random">random pad</a></li> 
          <li><a href="/recent">recent pads</a></li> 
        </ul> 
      </nav> 
     &nbsp;
    </div>

      ${next.body()}
    
    <div class="three columns">

      <h3>how to ...</h3>
      <ol>
        <li> Chose an optional markup syntax. </li>
        <li> Paste your text data into <a href="http://pyrapad.com">Pyrapad</a>. </li>
        <li> Hit submit to save and share! </li>
      </ol>

      <br/>

      <h3>say no ...</h3>
      <ul>
        <li> no registration </li>
        <li> no login </li>
        <li> no usernames </li>
        <li> no passwords </li>
        <li> no captchas </li>
        <li> no manditory fields </li>
        <li> no rules </li>
      </ul>

      <br/>

      <h3>say yes!</h3>
      <ul>
        <li> yes syntax prediction </li>
        <li> yes syntax highlighting </li>
        <li> yes pad replies </li>
        <li> yes generated uri's </li>
        <li> yes human readable uri's </li>
      </ul>
      
    </div>

  </div>

<br><br>

</body>
</html>


<%def name="google_analytics()">
    % if google_analytics_key:
      <script type="text/javascript">

          var _gaq = _gaq || [];
          _gaq.push(['_setAccount', "${google_analytics_key}"]);
          _gaq.push(['_trackPageview']);

          (function() {
          var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
          ga.static/skel = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
          var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
          })();

      </script>
    % endif
</%def>
