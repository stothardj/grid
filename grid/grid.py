import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_socketio import SocketIO, emit, join_room, rooms

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'grid.db'),
    SECRET_KEY='development key',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
socketio = SocketIO(app)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    """Sets up empty tables for the flaskr app."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def home():
    name = None
    userid = session.get('userid')
    if userid:
        db = get_db()
        curr = db.execute('select name from person where id=?', [userid])
        row = curr.fetchone()
        if not row:
            return redirect(url_for('logout'))
        name = row['name']
    return render_template('home.html', name=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        db = get_db()
        curr = db.cursor()
        curr.execute('insert into person (name) values (?)',
            [name])
        session['userid'] = str(curr.lastrowid)
        db.commit()
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('userid', None)
    flash('Logged out')
    return redirect(url_for('home'))

@app.route('/findmatch', methods=['POST'])
def find_match():
    return render_template('findgame.html');

@app.route('/play/<int:matchid>')
def play(matchid):
    print('Request to play %s' % matchid)
    return render_template('play.html')

@socketio.on('connect')
def test_connect():
    print('Got connection from %s' % get_username())

@socketio.on('find_match')
def find_match():
    print('Got find match event from %s' % get_username())
    userid = session['userid']
    enter_game_queue(userid)

@socketio.on('start_match')
def start_match(message):
    matchid = message['matchid']
    print('Got match started! %s is joining room %s' % (get_username(), matchid))
    join_room(matchid)

@socketio.on('send_msg')
def send_msg(message):
    text = message['text']
    matchid = message['matchid']
    emit('relay_msg', {
        'author': get_username(),
        'text': text,
     }, room=matchid)

def get_username():
    userid = session['userid']
    db = get_db()
    curr = db.execute('select name from person where id=?', [userid])
    row = curr.fetchone()
    if not row: return None
    return row['name']

def check_in_game(userid):
    db = get_db()
    curr = db.execute('select matchid from gamer where userid=?', [userid])
    row = curr.fetchone()
    if not row: return
    return row['matchid']

def enter_game_queue(userid):
    db = get_db()
    curr = db.execute('select userid, sessionid from gamer where matchid is null and userid!=?', [userid])
    unmatched_row = curr.fetchone()
    sid = request.sid
    if unmatched_row:
        print('Found an unmatched player!')
        curr.execute('insert into match default values')
        matchid = curr.lastrowid
        unmatched_userid = unmatched_row['userid']
        unmatched_sid = unmatched_row['sessionid']
        print('Connecting to Userid: %s, Sid: %s. You are Userid: %s, Sid: %s' % (unmatched_userid, unmatched_sid, userid, sid))
        curr.execute('insert into gamer (userid, matchid, sessionid) values (?,?,?)',
            [userid, matchid, sid])
        curr.execute('update gamer set matchid=? where userid=?',
            [matchid, unmatched_userid])
        emit('found_match', {
            'matchid': matchid,
        });
        emit('found_match', {
            'matchid': matchid,
        }, room=unmatched_sid)
    else:
        print('No unmatched player, so waiting...')
        print('Userid: %s, Sid: %s' % (userid, sid))
        curr.execute('insert into gamer (userid, sessionid) values (?,?)',
            [userid, sid])
    db.commit()

if __name__ == '__main__':
    socketio.run(app)
