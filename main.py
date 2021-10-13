from flask import Flask, redirect, request, render_template, url_for, session, render_template_string
import startup
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/')
def index():
    response = startup.getUser()
    return redirect(response)
        
@app.route('/callback/')
def callback():
    startup.getUserToken(request.args['code'])
    return redirect(url_for('test'))
      
@app.route('/test')
def test():
    access_token = startup.getAccessToken()
    username = startup.getUserJSON(access_token[0])
    userPlaylists = startup.getUserPlaylists(access_token[0], username)
    print(userPlaylists)
    return render_template('home.html', name = username, userPlaylists = userPlaylists)

app.run()
