init = ->
	console.log 'Playing a game'
	path = window.location.pathname
	[..., matchid] = path.split '/'
	console.log "Match id is #{matchid}"

	socket = io.connect('http://' + document.domain + ':' + location.port)
	socket.on 'connect', () -> startMatch socket, matchid
	socket.on 'relay_msg', (data) -> relayMessage data

startMatch = (socket, matchid) ->
	console.log 'Starting match'
	socket.emit 'start_match', {
		'matchid': matchid,
	}
	chatinput = document.getElementById 'chatinput'
	chatinput.addEventListener 'keyup', (ev) -> chatKey socket, matchid, ev

chatKey = (socket, matchid, ev) ->
	if ev.keyCode != 13 then return
	ev.preventDefault()
	msg = ev.currentTarget.value
	socket.emit 'send_msg', {
		'matchid': matchid
		'text': msg,
	}
	ev.currentTarget.value = ''

relayMessage = (data) ->
	appendChatMsg "#{data.author}: #{data.text}"

appendChatMsg = (msg) ->
	textNode = document.createTextNode msg
	lineEl = document.createElement 'div'
	lineEl.appendChild textNode
	chatlog = document.getElementById 'chatlog'
	chatlog.appendChild lineEl

init()
