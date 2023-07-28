import os
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from src.infer.utils import check_substring, check_string
from src.log.logger import get_spotify_logger

logger = get_spotify_logger()


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
        release_date = df.iloc[i]["release_date"]

        seary_query = title + " " + artist
        result = sp.search(seary_query, limit=4, type="track")
        res_score = -1
        url = ""

        for item in result["tracks"]["items"]:
            try:
                res_release_date = item["album"]["release_date"]
                res_artist_name = item["artists"][0]["name"]
                res_title = item["name"]
                res_url = item["preview_url"]
            except TypeError:
                pass

            if not res_url:
                continue

            now_score = (
                check_string(res_title, title) / 2
                + check_substring(res_title, title)
                + check_substring(res_artist_name, artist)
                + (res_release_date == release_date)
            )
            logger.info(
                {"now_score": now_score, "spotify_title": res_title, "spotify_artist": res_artist_name, "genie_title": title, "genie_artist": artist}
            )

            if now_score > res_score:
                url = res_url
                res_score = now_score

        if res_score <= 2:
            url = None

        try:
            if (not url) and (result["tracks"]["items"][0]["album"]["release_date"] == release_date):
                url = result["tracks"]["items"][0]["preview_url"]
        except IndexError:
            pass

        if url:
            urls.append(
                {
                    "song_id": df.iloc[i]["song_id"],
                    "song_title": df.iloc[i]["song_title"],
                    "artist_name": df.iloc[i]["artist_name"],
                    "album_title": df.iloc[i]["album_title"],
                    "music_url": url,
                }
            )
            logger.info(
                {
                    "song_id": df.iloc[i]["song_id"],
                    "music_url": url,
                }
            )
        else:
            logger.warning({"song_id": df.iloc[i]["song_id"], "music_url": url})

    df = pd.DataFrame(urls)
    return df
