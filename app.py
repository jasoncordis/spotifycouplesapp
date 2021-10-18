from flask import Flask, redirect, request, render_template, url_for, session, render_template_string
import startup
import random

app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/')
def index():
    response = startup.getUser()
    return redirect(response)
        
@app.route('/callback/')
def callback():
    startup.getUserToken(request.args['code'])
    return redirect(url_for('home'))
      
@app.route('/home')
def home():
    
    access_token = startup.getAccessToken()
    user = startup.getUserJSON(access_token[0])
    username = user[1]
    userimage = user[2]
    print("hello")
    return render_template('home.html', userimage = userimage, name = username)

@app.route('/playlist', methods = ['POST'])
def playlist():
    if request.method == 'POST':
            form_data = request.form
            access_token = startup.getAccessToken()
            user = startup.getUserJSON(access_token[0])
            userID = user[0]
            username = user[1]
            userimage = user[2]
            
            userPlaylists = startup.getUserPlaylists(access_token[0], userID)
            allUserPlaylists = startup.getUserOwnedPlaylists(userPlaylists, userID)
            randNums = startup.getRandomNumberList(10, len(allUserPlaylists[0]))
            randomPlaylist = startup.getRandomPlaylists(allUserPlaylists, randNums, userimage)
            randomTrack = startup.getRandomTrack(randomPlaylist, access_token)

            friendname = form_data["friendName"]
            if("user/" in friendname):
                beginName = friendname.find("user/")
                endName = friendname.find("?si")
                begin = int(beginName)
                end = int(endName)
                friendname = friendname[begin+5: end]

            friend = startup.getFriendJSON(access_token[0], friendname)
            friendimage = friend[2]
            if(friend == "none"):
                return render_template('error.html', userimage)
            friendDisplay = friend[1]
            friendPlaylists = startup.getUserPlaylists(access_token[0], friendname)
            allfriendPlaylists = startup.getUserOwnedPlaylists(friendPlaylists, friendname)
            randNums = startup.getRandomNumberList(10, len(allfriendPlaylists[0]))
            randomFriendPlaylist = startup.getRandomPlaylists(allfriendPlaylists, randNums, friendimage)
            randomFriendTrack = startup.getRandomTrack(randomFriendPlaylist, access_token)

            combinedPlaylist = startup.generateCombinedList(randomTrack, randomFriendTrack, randomPlaylist, randomFriendPlaylist, username, friendDisplay)
            idArray = startup.getIDarray(combinedPlaylist)

            return render_template('playlist.html', userimage = userimage, access_token = access_token, userid = userID, idArray = idArray, createPlaylist = startup.createPlaylist,  name = username, randomTrack = combinedPlaylist, friendName = friendDisplay, friendname = friendname)

@app.route('/createplaylist', methods = ['POST'])
def createplaylist():
    if request.method == 'POST':
        form_data = request.form
        access_token = startup.getAccessToken()
        user = startup.getUserJSON(access_token[0])
        userimage = user[2]
        playlist = startup.createPlaylist(access_token, user[0], user[1], form_data["friendName"])
        playID = playlist["id"]

        trackItems = form_data["idArray"]
        startup.addPlaylistItems(access_token, playID, trackItems)
        
        return render_template('createplaylist.html', userimage = userimage, playID = playID)
    
if __name__ == '__main__': app.run(debug=True)

