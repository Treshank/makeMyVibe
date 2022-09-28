from glob import glob
from flask import Flask, render_template, request, make_response
from utils.spotify import create_spotipy_client

app = Flask(__name__)
spotify_client = create_spotipy_client()
users = []
votes = []


def play_next_track():
    global votes
    votes = []
    spotify_client.next_track()


@app.route('/', methods=['POST', 'GET'])
def root():
    if request.method == "POST":
        name = request.form['Name']
        users.append({
            "name": name,
            "id": str(len(users))
        })
        response = make_response(render_template("index.html", have_user=True, name=name))
        response.set_cookie('id', users[-1]['id'])
        response.set_cookie('name', users[-1]['name'])
        return response
    else:
        id = request.cookies.get('id')
        name = request.cookies.get('name')
        try:
            if id is not None and users[int(id)]['name'] == name:
                return render_template("index.html", have_user=True, name=name)
        except IndexError as ie:
            pass
        return render_template("index.html", have_user=False)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == "POST":
        search_query = request.form["Search"]
        search_result = spotify_client.search(search_query)
        track_list = []
        if search_result:
            for track in search_result['tracks']['items']:
                track_list.append(
                    {
                        'name': track['name'],
                        'uri': track['uri'],
                        'artist': track['artists'][0]['name']
                    }
                )
        # return search_result['tracks']
        return render_template("search.html", tracks=track_list)
    return render_template("search.html")

    # spotify_client.start_playback(
    #     uris=["spotify:track:4PTG3Z6ehGkBFwjybzWkR8"]


@app.route('/vote_to_skip', methods=['GET'])
def vote_to_skip():
    id = request.cookies.get('id')
    if id is not None:
        if int(id) in votes:
            return "You have already cast your vote!"
        votes.append(int(id))
        if len(votes)/len(users) > 0.6:
            play_next_track()
        return "Cast vote successfully"
    else:
        return "You are not registered user!"


@app.route('/play_song/<uri>', methods=['GET'])
def play_song(uri):
    spotify_client.add_to_queue(uri=uri)
    return "Added to queue"


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")

