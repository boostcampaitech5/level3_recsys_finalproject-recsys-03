import pandas as pd
from typing import List
from huggingface_hub import Repository
from src.infer.preprocess import SongPreprocesser


class SongIdExtractor:
    def __init__(self, is_data_pull: bool):
        self.is_data_pull = is_data_pull
        self.song_processor = SongPreprocesser(self.is_data_pull)
        self.playlist, self.song_info = self.song_processor.get_dataframes()

    def get_song_info(self, pl_id_list: list, sim_list: list, user_genres: list):
        result = self.result_to_df(pl_id_list, sim_list)

        pl = pd.merge(result, self.playlist)
        pl["matched_rate"] = pl.matched / pl.tag_cnt
        pl = pl.drop(["tag_cnt", "matched"], axis=1)
        pl_song = self.spread_songs(pl)

        self.info = pd.merge(pl_song, self.song_info)
        self.info["user_genre"] = self.info["genre"].apply(lambda x: x in user_genres)

        result_df = self.get_sorted_info(self.info)
        rec_songs = result_df[:][["song_id", "song_title", "artist_name", "album_title", "release_date"]]
        return rec_songs

    def get_sorted_info(self, df: pd.DataFrame):
        n = df.shape[0]
        cols = df.columns
        date = [i * 3 for i in range(n)]
        pop = [(i * 3) + 1 for i in range(n)]
        sim = [(i * 3) + 2 for i in range(n)]

        result_values = [[0] * len(cols)] * (n * 3)
        result_df = pd.DataFrame(result_values, columns=cols)

        by_date = df.sort_values(by=["user_genre", "release_date"], ascending=False)
        by_pop = df.sort_values(by=["user_genre", "listener_cnt"], ascending=False)
        by_sim = df.sort_values(by=["sim", "listener_cnt"], ascending=False)

        result_df.iloc[date, :] = by_date.reset_index(drop=True)
        result_df.iloc[pop, :] = by_pop.reset_index(drop=True)
        result_df.iloc[sim, :] = by_sim.reset_index(drop=True)

        result_df = result_df.drop_duplicates(["song_id"]).reset_index(drop=True)

        return result_df

    def result_to_df(self, id_list: List[int], sim_list: List[float]) -> pd.DataFrame:
        model_result = pd.DataFrame({"playlist_id": id_list, "cos_sim": sim_list})
        model_result = model_result.groupby("playlist_id").agg({"cos_sim": [max, len]}).reset_index()
        model_result.columns = ["playlist_id", "cos_sim", "matched"]
        return model_result

    def spread_songs(self, df: pd.DataFrame) -> pd.DataFrame:
        pl_id = []
        song_id = []
        sim = []
        pl_match = []

        for id in df.playlist_id:
            i, s, song_list, mr = df[df.playlist_id == id].values.flatten()
            for song in song_list:
                pl_id.append(i)
                sim.append(s)
                song_id.append(int(song))
                pl_match.append(mr)
        pl_song = pd.DataFrame({"song_id": song_id, "playlist_id": pl_id, "sim": sim, "pl_match": pl_match})
        return pl_song
