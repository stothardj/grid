init = ->
	console.log 'Finding a game!'
	socket = io.connect('http://' + document.domain + ':' + location.port)
	socket.on 'connect', () -> findMatch(socket)
	socket.on 'found_match', (data) -> startMatch socket, data.matchid

findMatch = (socket) ->
	socket.emit 'find_match'

startMatch = (socket, matchid) ->
	console.log "Found a new match! #{matchid}"
	window.location.href = "/play/#{matchid}"

init()
