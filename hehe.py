import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

# Set up Spotipy with your credentials
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id="08e2d80fcc3746bea6f8df1505f91394",
        client_secret="13ea042e88ce4b23bbd5c37e4087f6ff",
    )
)


# List of songs to download
songs_to_search = [
    "How Do I Say Goodbye - Dean Lewis",
    "Disfruto - Carla Morrison",
    "Viva La Vida - Coldplay",
    "Night Changes - One Direction",
    "Take Me to Church - Hozier",
    "Despacito - Luis Fonsi and Daddy Yankee",
    "Stereo Hearts - Gym Class Heroes",
    "Let Her Go - Passenger",
    "Another Love - Tom Odell",
]


# Function to search for a song on Spotify
def search_song(song_name):
    results = sp.search(q=song_name, limit=1)
    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        song_info = {
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "preview_url": track["preview_url"],
        }
        return song_info
    else:
        return None


# Function to download the song preview
def download_song(song_info):
    if not os.path.exists("songs"):
        os.makedirs("songs")

    song_name = song_info["name"]
    artist_name = song_info["artist"]
    preview_url = song_info["preview_url"]

    if preview_url:
        response = requests.get(preview_url)
        file_path = os.path.join("songs", f"{song_name}.mp3")

        with open(file_path, "wb") as file:
            file.write(response.content)

        # Set the ID3 tags
        audio = MP3(file_path, ID3=EasyID3)
        audio["artist"] = artist_name
        audio["title"] = song_name
        audio.save()

        print(f"Downloaded and tagged: {song_name} by {artist_name}")
    else:
        print(f"No preview available for {song_name} by {artist_name}")


if __name__ == "__main__":
    for song in songs_to_search:
        song_info = search_song(song)
        if song_info:
            download_song(song_info)
        else:
            print(f"Song not found: {song}")
