<%inherit file="base.mako" />

<div class="twelve columns content offset-by-one">

    <h1>Supported Syntaxes</h1>

  Total syntaxes count: ${len(syntaxes)}

  <br />

  <ol>
  % for syntax in syntaxes:
    <% uri  = '/recent-%s-pads' % syntax %>
    <li><a href="${ uri }">${ syntax.title() }</li>
  % endfor
  </ol>
  <br />
