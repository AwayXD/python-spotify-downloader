import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv
import subprocess
import os
import threading

root = tb.Window(themename="darkly")
root.title("Spotify Downloader")
root.geometry("650x520")
root.resizable(False, False)

frame = tb.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

tb.Label(frame, text="Spotify Credentials", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 10))

tb.Label(frame, text="Client ID:").pack(anchor="w")
client_id_entry = tb.Entry(frame, width=60)
client_id_entry.pack(pady=5)

tb.Label(frame, text="Client Secret:").pack(anchor="w")
client_secret_entry = tb.Entry(frame, width=60, show="*")
client_secret_entry.pack(pady=5)

tb.Label(frame, text="Redirect URI:").pack(anchor="w")
redirect_entry = tb.Entry(frame, width=60)
redirect_entry.insert(0, "http://127.0.0.1:9090/callback")
redirect_entry.pack(pady=5)

tb.Label(frame, text="Spotify Playlist URL", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(20, 10))
playlist_entry = tb.Entry(frame, width=60)
playlist_entry.pack(pady=5)

status_label = tb.Label(frame, text="", bootstyle="success")
status_label.pack(pady=(15, 5))

song_label = tb.Label(frame, text="", wraplength=600, bootstyle="info")
song_label.pack()

def export_and_download():
    playlist_url = playlist_entry.get().strip()
    client_id = client_id_entry.get().strip()
    client_secret = client_secret_entry.get().strip()
    redirect_uri = redirect_entry.get().strip()

    if not playlist_url or not client_id or not client_secret:
        messagebox.showerror("Missing Info", "Please fill in all required fields.")
        return

    def task():
        try:
            status_label.config(text=" Authenticating with Spotify...")
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope="playlist-read-private"
            ))

            playlist_id = playlist_url.split("playlist/")[1].split("?")[0]
            results = sp.playlist_items(playlist_id)

            tracks = []
            for item in results['items']:
                track = item['track']
                name = track['name']
                artist = track['artists'][0]['name']
                tracks.append([name, artist])

            save_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                     filetypes=[("CSV Files", "*.csv")],
                                                     title="Save Playlist As")
            if not save_path:
                status_label.config(text="Export canceled.")
                return

            with open(save_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Track", "Artist"])
                writer.writerows(tracks)

            status_label.config(text=" Playlist exported to CSV.")

            download_folder = filedialog.askdirectory(title="Select Folder to Save Songs")
            if not download_folder:
                status_label.config(text="Download canceled.")
                return

            for name, artist in tracks:
                query = f"{name} {artist}"
                song_label.config(text=f" Downloading: {query}")
                try:
                    subprocess.run([
                        "yt-dlp",
                        f"ytsearch1:{query}",
                        "--extract-audio",
                        "--audio-format", "mp3",
                        "--output", os.path.join(download_folder, "%(title)s.%(ext)s")
                    ], check=True)
                except subprocess.CalledProcessError as err:
                    print(f"Failed to download {query}: {err}")

            song_label.config(text="")
            status_label.config(text=" All songs downloaded successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            status_label.config(text="")

    threading.Thread(target=task).start()

export_btn = tb.Button(frame, text="Export + Download", bootstyle="success-outline", width=30, command=export_and_download)
export_btn.pack(pady=25)

root.mainloop()
