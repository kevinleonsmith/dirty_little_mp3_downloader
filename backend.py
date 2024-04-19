# backend.py
from flask import Flask, request, jsonify
from pytube import YouTube
import os
import threading

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_audio():
    mp3_link = request.json.get('mp3_link')
    if not mp3_link:
        return jsonify({'error': 'MP3 URL is required'}), 400

    try:
        def on_progress(stream, chunk, bytes_remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentage_completed = round(bytes_downloaded / total_size * 100)
            socketio.emit('progress', {'percentage': percentage_completed})

        audio = YouTube(mp3_link, on_progress_callback=on_progress)
        output = audio.streams.get_audio_only().download()
        base, ext = os.path.splitext(output)
        new_file = base + '.mp3'
        os.rename(output, new_file)
        return jsonify({'message': 'MP3 downloaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
