import configparser
config = configparser.ConfigParser()
config.read('.env')

SPOTIFY_CLIENT_ID = config['SPOTIFY']['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = config['SPOTIFY']['SPOTIFY_CLIENT_SECRET']