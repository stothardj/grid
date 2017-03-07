init = ->
  console.log 'Finding a game!'
  socket = io.connect('http://' + document.domain + ':' + location.port)
  socket.on 'connect', -> console.log 'Connected!'
  socket.on 'found_match', (data) -> startMatch socket, data.matchid

startMatch = (socket, matchid) ->
  console.log "Found a new match! #{matchid}"
  socket.emit 'start_match', { matchid: matchid, }

init()
