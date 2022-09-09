from flask import Flask, render_template, request
from utils.spotify import create_spotipy_client

app = Flask(__name__)
spotify_client = create_spotipy_client()


@app.route('/', methods=['POST', 'GET'])
def root():
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
        return render_template("index.html", tracks=track_list)
    return render_template("index.html")

    # spotify_client.start_playback(
    #     uris=["spotify:track:4PTG3Z6ehGkBFwjybzWkR8"]


@app.route('/play_song/<uri>', methods=['GET'])
def play_song(uri):
    spotify_client.add_to_queue(uri=uri)
    return "Done"


if __name__ == '__main__':
    app.run()

