from flask import Flask, render_template, request
from utils.spotify import create_spotipy_client

app = Flask(__name__)
spotify_client = create_spotipy_client()


@app.route('/', methods=['POST', 'GET'])
def root():
    spotify_client.start_playback(
        uris=["spotify:track:4PTG3Z6ehGkBFwjybzWkR8"]
    )
    return "Enjoy!"


if __name__ == '__main__':
    app.run()

