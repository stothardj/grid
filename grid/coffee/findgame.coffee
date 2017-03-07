init = ->
  console.log 'Finding a game!'
  socket = io.connect('http://' + document.domain + ':' + location.port)
  socket.on 'connect', -> console.log 'Connected!'
  socket.on 'found_match', (data) -> console.log "Found match #{data.matchid}"

init()
