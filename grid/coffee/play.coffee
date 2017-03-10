init = ->
  console.log 'Playing a game'
  chatinput = document.getElementById 'chatinput'
  chatinput.addEventListener 'keyup', chatKey

chatKey = (ev) ->
  if ev.keyCode != 13 then return
  ev.preventDefault()
  text = ev.currentTarget.value
  ev.currentTarget.value = ''
  textNode = document.createTextNode text
  lineEl = document.createElement 'div'
  lineEl.appendChild textNode
  chatlog = document.getElementById 'chatlog'
  chatlog.appendChild lineEl

init()
