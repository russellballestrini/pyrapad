<%inherit file="base.mako" />

<%namespace name="m" module="pyrapad.lib.makofuncs"/>

<div class="twelve columns content offset-by-one">

  % if current_page == 1:
    <h1>Recent Pads</h1>
  % else:
    <h1>Recent Pads - Page ${current_page}</h1>
  % endif

  Total pad count: ${pad_count}

  <br />

  % for i, pad in enumerate( pads ):
  <% 
    data = pad.data.split( '\n', 7 )[:7]
    data = '\n'.join( data )

    ago = m.agohuman( pad.created, past_tense = 'created {} ago' )

  %>
    <div style="padding-top: 40px;">
      <b>
      ##<a href="/recent-${pad.syntax}-pads">${pad.syntax}:</a> 
      ${ago}  
      <br/>
      <a href="${pad.id}/${pad.uri}">${pad.uri}</a> 
      </b>
      <br />
      <a href="${pad.id}/${pad.uri}" style="text-decoration: none;">
        <pre>${data}</pre>
      </a> 
      <b>
      ... view all <a href="${pad.id}/${pad.uri}">${ pad.data.count('\n') + 1 }</a> lines
      </b>
    </div>
    <br />
  % endfor

  <div class="paginate" style="font-size: 1.5em;text-align: center;font-weight: bold;"> pages ${pads.pager()}</div>
