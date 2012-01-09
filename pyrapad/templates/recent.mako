<%inherit file="base.mako" />

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

    chart = {
      4 : 'day',
      3 : 'hour',
      2 : 'minute',
      1 : 'second'
    }

    delta = timenow - pad.created

    ## parts tuple ( days, hours, minutes, seconds )
    parts = ( delta.days, delta.seconds/3600, (delta.seconds/60)%60, delta.seconds )

    ## remove leading zeros
    for part in parts:
        if part: break
        else: parts = parts[1:]
    
    type  = chart[len(parts)]
    count = str(parts[0])
    # determine if plural
    s = '' if parts[0] == 1 else 's'

    ago = count + ' ' + type + s
  %>
    <hr />
    <div>
      <a href="/recent-${pad.syntax}-pads">${pad.syntax}:</a> 
      <a href="${pad.id}/${pad.uri}">${pad.uri}</a> 
      created ${ago} ago
      <br />
      <a href="${pad.id}/${pad.uri}" style="text-decoration: none;">
        <pre>${data}</pre>
      </a> 
      ... view all <a href="${pad.id}/${pad.uri}">${ pad.data.count('\n') + 1 }</a> lines
    </div>
    <br />
  % endfor

  <div class="paginate" style="font-size: 1.5em;text-align: center;font-weight: bold;"> pages ${pads.pager()}</div>
