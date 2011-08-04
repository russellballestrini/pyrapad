<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
<head>
  <title>${title} - ${request.host}</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <meta name="keywords" content="Pyrapad" />
  <meta name="description" content="Pyrapad" />

  <link rel=stylesheet HREF="/static/pygments-tango.css" TYPE="text/css"> 
  ##<link rel=stylesheet HREF="/static/colorful.css" TYPE="text/css"> 

${ google_analytics() }

</head>
<body>

<div id="body">

    ##<h1>${title}</h1>

    ${next.body()}

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
          ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
          var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
          })();

      </script>
    % endif
</%def>
