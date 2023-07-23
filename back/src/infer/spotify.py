import os
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from src.utils import check_substring


def get_spotify_url(df: pd.DataFrame, top_k: int) -> pd.DataFrame:
    cid = os.environ["SPOTIFY_CID"]
    secret = os.environ["SPOTIFY_PWD"]
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    urls = []
    for i in range(df.shape[0]):
        if len(urls) == top_k:
            break

        title = df.iloc[i]["song_title"]
        artist = df.iloc[i]["artist_name"]

        seary_query = title + " " + artist
        result = sp.search(seary_query, limit=4, type="track")

        for idx in range(4):
            res_release_date = result["tracks"]["items"][idx]["album"]["release_date"]
            res_artist_name = result["tracks"]["items"][idx]["artists"][0]["name"]
            res_title = result["tracks"]["items"][idx]["name"]
            url = result["tracks"]["items"][idx]["preview_url"]

            if res_title != title and res_artist_name != artist:
                print(f"spotify : {res_title},  {res_artist_name}")
                print(f"genie : {title},  {artist}")
                if not (check_substring(res_title, title) and check_substring(res_artist_name, artist)):
                    print("wrong!!")
                    print(f"spotify : {res_title},  {res_artist_name}")
                    print(f"genie : {title},  {artist}")
                    print("-----------------------------------------------")
                    url = None

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
                break

    df = pd.DataFrame(urls)
    return df
