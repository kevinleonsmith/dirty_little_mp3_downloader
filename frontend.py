# frontend.py
import tkinter as tk
from tkinter import ttk
import requests
import threading

def download_audio():
    mp3_link = url_entry.get()
    if not mp3_link:
        progress_label.config(text='Please enter the MP3 URL')
        return

    def update_progress(percentage):
        progress_label.config(text=f'{percentage}%')

    def download():
        try:
            response = requests.post('http://127.0.0.1:5000/download', json={'mp3_link': mp3_link})
            data = response.json()
            if 'error' in data:
                progress_label.config(text=data['error'])
            else:
                progress_label.config(text=data['message'])
        except Exception as e:
            progress_label.config(text=str(e))

    t = threading.Thread(target=download)
    t.start()

window = tk.Tk()
window.title('MP3 Downloader')

canvas = tk.Canvas(window, width=500, height=400)
canvas.pack()

# Your Tkinter GUI code here...

window.mainloop()
