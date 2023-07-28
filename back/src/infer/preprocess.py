import os
import pandas as pd
from src.infer.utils import str2list
from huggingface_hub import Repository


class SongPreprocesser:
    def __init__(self, is_data_pull: bool):
        self.is_data_pull = is_data_pull

        self.set_path()
        self.load_data()

    def set_path(self):
        self.HUB_PATH = "./hub"
        self.CSV_PATH = os.path.join(self.HUB_PATH, "CsvFiles")

    def load_data(self):
        if self.is_data_pull:
            Repository(local_dir=self.CSV_PATH).git_pull()

        csv_files = os.listdir(self.CSV_PATH)
        csv_files = [file for file in csv_files if ".csv" in file]
        for file in csv_files:
            if "playlists" in file:
                self.playlist = pd.read_csv(os.path.join(self.CSV_PATH, file))
            elif "songs_detail" in file:
                self.song_detail = pd.read_csv(os.path.join(self.CSV_PATH, file))
            elif "songs_v" in file:
                self.songs = pd.read_csv(os.path.join(self.CSV_PATH, file))
            elif "genre" in file:
                self.genre = pd.read_csv(os.path.join(self.CSV_PATH, file))
            else:
                raise Exception(f"Wrong File {file} is detected !!!")

    def count_tag_types(self) -> None:
        tag_list = ["sit", "mood", "weather"]
        for tag in tag_list:
            self.playlist[f"tag_{tag}_cnt"] = self.playlist[f"tag_{tag}_cnt"].apply(lambda x: min(x, 1))

        self.playlist["tag_cnt"] = self.playlist.tag_sit_cnt + self.playlist.tag_mood_cnt + self.playlist.tag_weather_cnt

    def merge_songdf(self, song_detail: pd.DataFrame, songs: pd.DataFrame, genre: pd.DataFrame):
        song_detail.columns = [col.lower() for col in song_detail.columns]
        songs.columns = [col.lower() for col in songs.columns]

        merged = pd.merge(songs, song_detail)[["song_id", "song_title", "info_genre", "listener_cnt", "artist_name", "album_title", "release_date"]]
        merged = pd.merge(merged, genre).drop("info_genre", axis=1)

        merged = merged.dropna().drop_duplicates().reset_index(drop=True)
        return merged

    def get_dataframes(self) -> pd.DataFrame:
        str2list(self.playlist, ["playlist_songs"])
        self.count_tag_types()

        playlist = self.playlist[["playlist_id", "playlist_songs", "tag_cnt"]]
        song_info = self.merge_songdf(self.song_detail, self.songs, self.genre)
        return playlist, song_info
