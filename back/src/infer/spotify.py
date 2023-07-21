import os
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials


def get_spotify_url(df: pd.DataFrame, top_k: int) -> pd.DataFrame:
    cid = os.environ["SPOTIFY_CID"]
    secret = os.environ["SPOTIFY_PWD"]
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    urls = []
    for i in range(df.shape[0]):
        if len(urls) == top_k:
            break
        else:
            title = df.iloc[i]["song_title"]
            artist = df.iloc[i]["artist_name"]

            seary_query = title + " " + artist
            result = sp.search(seary_query, limit=1, type="track")
            url = result["tracks"]["items"][0]["preview_url"]

            if url:
                urls.append(
                    {
                        "song_id": df.iloc[i]["song_id"],
                        "youtube_key": df.iloc[i]["youtube_key"],
                        "song_title": df.iloc[i]["song_title"],
                        "artist_name": df.iloc[i]["artist_name"],
                        "album_title": df.iloc[i]["album_title"],
                        "music_url": url,
                    }
                )

    df = pd.DataFrame(urls)
    return df
