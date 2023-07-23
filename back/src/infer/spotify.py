import os
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from src.utils import check_substring
from src.log.Logger import get_spotify_logger

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

        seary_query = title + " " + artist
        result = sp.search(seary_query, limit=3, type="track")

        for idx in range(3):
            # res_release_date = result["tracks"]["items"][idx]["album"]["release_date"]
            res_artist_name = result["tracks"]["items"][idx]["artists"][0]["name"]
            res_title = result["tracks"]["items"][idx]["name"]
            url = result["tracks"]["items"][idx]["preview_url"]

            if res_title != title and res_artist_name != artist:
                if not (check_substring(res_title, title) and check_substring(res_artist_name, artist)):
                    logger.warning(
                        {
                            "song_id": df.iloc[i]["song_id"],
                            "spotify_title": res_title,
                            "spotify_artist": res_artist_name,
                            "genie_title": title,
                            "genie_artist": artist,
                        }
                    )
                    url = None
                else:
                    logger.info(
                        {
                            "song_id": df.iloc[i]["song_id"],
                            "spotify_title": res_title,
                            "spotify_artist": res_artist_name,
                            "genie_title": title,
                            "genie_artist": artist,
                        }
                    )

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
                logger.info({"song_id": df.iloc[i]["song_id"], "music_url": url})
                break
            else:
                logger.warning({"song_id": df.iloc[i]["song_id"], "music_url": url})

    df = pd.DataFrame(urls)
    return df
