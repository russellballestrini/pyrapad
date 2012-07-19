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
        //$('#' + target).slideDown( "slow" );
        $('#' + target).fadeIn( "slow" );
        $('#' + button).text( "hide" );
    }
    else {
        //$('#' + target).slideUp( "slow" );
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

        <b><a href="http://${request.host}" style="text-decoration: none;">${request.host}</a></b> 

        <ul> 
          <li><a href="#" onClick="document.forms[0].submit();">save pad</a></li> 
          <li><a href="/">new pad</a></li> 
          % if pad:
              <li><a href="/${pad.id}/${pad.uri}/raw">raw pad</a></li> 
              <li><a href="/${pad.id}/${pad.uri}/clone">clone pad</a></li> 
              <li><a href="javascript: toggle('settingsform', 'alterlink', 'alter pad')" id="alterlink">alter pad</a></li> 
              
          % else:
              <li>raw pad</li> 
              <li>clone pad</li> 
              <li>alter pad</li> 
          % endif
          <li><a href="/random">random pad</a></li> 
          <li><a href="/recent">recent pads</a></li> 
          ##<li><a href="/syntaxes">syntaxes</a></li> 
          ##<li><a href="/about">about pad</a></li> 
        </ul> 

      </nav> 

    % if pad:
      <form action="/${pad.id}/${pad.uri}/alter" id="settingsform" method="post" style="display: none;">
        <div id="settingsdiv">
            uri:
            <br/>
            <input id="renametext" value="${pad.uri}" size="35" name="newuri"/> 
            <br/>
            <br/>
            syntax:
            <br/>
            <input id="syntaxtext" value="${pad.syntax}" size="35" name="newsyntax"/>
            <br/>
            <br/>
            <center>
            <input type="button" value="cancel" name="cancel" onClick="javascript: toggle('settingsform', 'alterlink', 'alter pad')"/> 
            <input type="submit" value="save" name="save"/> 
            </center>
        </div>
    </form>
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
