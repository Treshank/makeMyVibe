from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def search():  # put application's code here
    if request.method == 'POST':
        search_text = request.form['song']
        sender_name = request.form['name'] if request.form['name'] else "Anonymous"
        # search_cmd = '/home/t_rekt/PycharmProjects/makeMyVibe/spt search "Ariana" --tracks'
        search_cmd = ["./spt", "s", f"'{str(search_text)}'", "--tracks"]
        process = subprocess.Popen(search_cmd, stdout=subprocess.PIPE)
        output, error = process.communicate()
        track_list = []
        if output:
            decoded = output.decode("utf-8")
            for item in decoded.split(')'):
                try:
                    name, uri = item.split(' (spotify:')
                    track_list.append({
                        'name': name.strip(),
                        'uri': 'spotify:'+uri
                        }
                    )
                except ValueError as e:
                    pass
        # for idx, track in enumerate(results['tracks']['items']):
        # 	print(idx, track['name'])
        # songlist = results['tracks']['items']
        return render_template('index.html', tracks=track_list, sender_name=sender_name)

        # return render_template('spotify-flask.html', tracks=songlist)
    return render_template('index.html')


@app.route('/done/<uri>/<song_name>/<name>', methods=['GET'])
def success(uri, song_name, name):
    print(name, "sent the song:", song_name)
    search_cmd = ["./spt", "p", "--uri", uri]
    process = subprocess.Popen(search_cmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    return render_template('done.html')


if __name__ == '__main__':
    app.run()

