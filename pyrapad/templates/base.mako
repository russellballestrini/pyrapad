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

  ##<link rel="stylesheet" href="/static/skel/stylesheets/base.css"> 
  ##<link rel="stylesheet" href="/static/skel/stylesheets/skeleton.css"> 
  ##<link rel="stylesheet" href="/static/skel/stylesheets/layout.css"> 
  ##<link rel="stylesheet" href="/static/skel/stylesheets/docs.css"> 
 
  <link rel="stylesheet" href="/static/custom.css"> 

  <!-- Pygments
  ================================================== --> 

  ##<link rel=stylesheet HREF="/static/pygments/pygments-tango.css" TYPE="text/css"> 
  ##<link rel=stylesheet HREF="/static/pygments/colorful.css" TYPE="text/css"> 
  <link rel=stylesheet HREF="/static/pygments/native.css" TYPE="text/css"> 

  <!-- Favicon
  ================================================== --> 

  <link rel="shortcut icon" href="/static/skel/images/favicon.ico"> 
  <link rel="apple-touch-icon" sizes="57x57" href="/static/skel/images/apple-touch-icon.png"> 
  <link rel="apple-touch-icon" sizes="72x72" href="/static/skel/images/apple-touch-icon-72x72.png" /> 
  <link rel="apple-touch-icon" sizes="114x114" href="/static/skel/images/apple-touch-icon-114x114.png" /> 

  <script type="text/javascript" src="/static/js/jquery.js"></script>

<script type="text/javascript">
// this toggles the dropdown
function toggle( target, button, origtext ){
    if ( !$('#' + target + ":visible").size() ){
        $('#' + target).fadeIn( "slow" );
        $('#' + button).text( "hide" );
    }
    else {
        $('#' + target).fadeOut( "slow" );
        $('#' + button).text( origtext );
    }
}
</script>

${ google_analytics() }

</head>
<body>

  <div class="container"> 

      <nav>  

        <ul> 
          <li><a href="/">new</a></li> 
          <li><a href="#" onClick="document.forms[0].submit();">save</a></li> 
          % if pad:
              <li><a href="/${pad.id}/${pad.uri}/raw">raw</a></li> 
              <li><a href="javascript: toggle('settingsform', 'alterlink', 'alter')" id="alterlink">alter</a></li> 
              <li><a href="/${pad.id}/${pad.uri}/edit">edit</a></li> 
              <li><a href="/${pad.id}/${pad.uri}/clone">clone</a></li> 
              
          % else:
              <li>raw</li> 
              <li>alter</li> 
              <li>edit</li> 
              <li>clone</li> 
          % endif
          <li><a href="/random">random</a></li> 
          <li><a href="/recent">recent</a></li> 
          ##<li><a href="/syntaxes">syntaxes</a></li> 
          ##<li><a href="/about">about</a></li> 
        </ul> 

      </nav> 

    % if pad:
      <form action="/${pad.id}/${pad.uri}/alter" id="settingsform" method="post" style="display: none;">
        <div id="settingsdiv">
            uri:
            <br/>
            <input id="renametext" name="newuri" type="text" value="${pad.uri}"/> 
            <br/>
            <br/>
            syntax:
            <br/>
            <input id="syntaxtext" name="newsyntax" type="text" value="${pad.syntax}"/>
            <br/>
            <br/>
            wordwrap:
            <br/>
            <input id="wordwrap" name="wordwrap" type="checkbox" ${'checked' if pad.wordwrap else ''}/>
            <span class="tiny-text" style="text-align: top;">no horizontal scrolling</span>
            <br/>
            <br/>
            <center>
            <input type="button" value="cancel" name="cancel" onClick="javascript: toggle('settingsform', 'alterlink', 'alter')"/> 
            <input type="submit" value="save" name="save"/> 
            </center>
        </div>
      </form>
      % if pad.wordwrap == True:
        <style>
        div.highlight pre {
          white-space: pre-wrap;
        }
        div.linenodiv {
          visibility:hidden;
        }
        table.highlighttable {
          width:85%;
        }
        </style>
      % endif
    % endif

  ${next.body()}

  </div>

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
          ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
          var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
          })();

      </script>
    % endif
</%def>
