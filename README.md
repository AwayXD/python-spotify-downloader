````markdown
# Spotify Playlist Exporter

This application allows you to export a Spotify playlist to a CSV file. It provides a simple graphical interface using a dark-themed Tkinter window with `ttkbootstrap`.

## Features

- Authenticate with Spotify using your credentials.
- Export playlist tracks (name and artist) to a CSV file, then to exports through yt-dlp
- Simple and responsive GUI.

## How It Works

1. You provide your Spotify **Client ID**, **Client Secret**, and **Redirect URI**.
2. Input the Spotify playlist URL you want to export.
3. The app authenticates with Spotify and retrieves all tracks from the playlist.
4. Tracks are exported to a CSV file at your chosen location.

## Setting Up Spotify Credentials

To use this app, you need to create a Spotify application:

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
2. Log in with your Spotify account.
3. Click **Create an App** and fill in the required fields.
4. Copy the **Client ID** and **Client Secret**.
5. Set a **Redirect URI** (e.g., `http://127.0.0.1:9090/callback`) in your app settings. Make sure it matches the one you enter in the program.

### Prerequisites

Make sure you have Python 3.10+ installed. You also need the following Python packages:

- `ttkbootstrap`
- `spotipy`

### Installing Dependencies

```bash
pip install ttkbootstrap spotipy
````

### Running the Application

1. download: `exporter.py`.
2. Run the script:

```bash
python exporter.py
```

3. Fill in your Spotify credentials and playlist URL.
4. Choose the location to save the CSV file, and where to save the music.

## Notes

* Make sure your Spotify app credentials have the **playlist-read-private** scope enabled.
* Only playlists accessible to your account can be exported.
* The application runs in a separate thread to keep the UI responsive during export.

## License

feel free to fork how you like!
-away c:

```
