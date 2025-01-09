from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__, template_folder='templates')

# Load playlists from JSON file
def load_playlists():
    if os.path.exists('playlists.json'):
        with open('playlists.json', 'r') as f:
            return json.load(f)
    return {"playlists": []}  # Return an empty structure if the file doesn't exist

# Save playlists to JSON file
def save_playlists(playlists):
    with open('playlists.json', 'w') as f:
        json.dump(playlists, f, indent=4)  # Use indent for pretty printing

@app.route('/')
def index():
    playlists = load_playlists()
    return render_template('index.html', playlists=playlists['playlists'])

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    playlists = load_playlists()
    playlist_name = request.json.get('name')
    
    if not playlist_name:
        return jsonify({'error': 'Playlist name is required'}), 400
    
    playlists['playlists'].append({'name': playlist_name, 'songs': []})
    
    try:
        save_playlists(playlists)  # Save the updated playlists
        return jsonify(playlists['playlists']), 201  # Return the updated playlists with a 201 status
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error if saving fails

@app.route('/add_song', methods=['POST'])
def add_song():
    playlists = load_playlists()
    song_name = request.json.get('name')
    playlist_index = request.json.get('playlist_index')
    
    if not song_name or playlist_index is None:
        return jsonify({'error': 'Song name and playlist index are required'}), 400
    
    if 0 <= playlist_index < len(playlists['playlists']):
        playlists['playlists'][playlist_index]['songs'].append(song_name)
        
        try:
            save_playlists(playlists)  # Save the updated playlists
            return jsonify(playlists['playlists']), 201  # Return the updated playlists with a 201 status
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # Return error if saving fails
    else:
        return jsonify({'error': 'Invalid playlist index'}), 404

@app.route('/remove_song', methods=['POST'])
def remove_song():
    playlists = load_playlists()
    playlist_index = request.json.get('playlist_index')
    song_index = request.json.get('song_index')
    
    if 0 <= playlist_index < len(playlists['playlists']):
        if 0 <= song_index < len(playlists['playlists'][playlist_index]['songs']):
            playlists['playlists'][playlist_index]['songs'].pop(song_index)
            save_playlists(playlists)
            return jsonify(playlists['playlists']), 200  # Return the updated playlists
        else:
            return jsonify({'error': 'Invalid song index'}), 404
    else:
        return jsonify({'error': 'Invalid playlist index'}), 404

@app.route('/delete_playlist', methods=['POST'])
def delete_playlist():
    playlists = load_playlists()
    playlist_index = request.json.get('playlist_index')
    
    if 0 <= playlist_index < len(playlists['playlists']):
        playlists['playlists'].pop(playlist_index)
        save_playlists(playlists)
        return jsonify(playlists['playlists']), 200  # Return the updated playlists
    else:
        return jsonify({'error': 'Invalid playlist index'}), 404

if __name__ == '__main__':
    app.run(debug=True)