import os
import re
import ast
import pandas as pd
from collections import Counter
from typing import List
from huggingface_hub import Repository

from src.utils import str2list


class SongIdExtractor:
    def __init__(self, k: int, is_data_pull: bool):
        self.k = k
        self.is_data_pull = is_data_pull
        
        self.set_path()
        self.load_data()
        
    def set_path(self):
        self.HUB_PATH = "./hub"
        self.CSV_PATH = os.path.join(self.HUB_PATH, "CsvFiles")
        
    def load_data(self):
        if self.is_data_pull:
            Repository(local_dir = self.CSV_PATH).git_pull()
            
        csv_files = os.listdir(self.CSV_PATH)
        csv_files = [file for file in csv_files if '.csv' in file]
        for file in csv_files:
            if "playlists" in file:
                self.playlist = pd.read_csv(os.path.join(self.CSV_PATH, file))
            elif "songs_detail" in file:
                self.song_detail = pd.read_csv(os.path.join(self.CSV_PATH, file))
            elif "songs_v" in file:
                self.songs = pd.read_csv(os.path.join(self.CSV_PATH, file))
            elif "keys" in file:
                self.youtube = pd.read_csv(os.path.join(self.CSV_PATH, file))
            elif "genre" in file:
                self.new_genre = pd.read_csv(os.path.join(self.CSV_PATH, file))
            else:
                raise Exception(f"Wrong File {file} is detected !!!")
            
    def get_song_info(self, pl_id_list: list, sim_list: list, user_genres: list) -> pd.DataFrame:
        sim_list = [1/sim for sim in sim_list]
        model_result = self.result_to_df(pl_id_list, sim_list)

        pl_result = self.playlist.loc[self.playlist['playlist_id'].isin(pl_id_list)][['playlist_id','playlist_songs','num_of_songs','playlist_view', 'playlist_likecount','tag_sit_cnt', 'tag_mood_cnt', 'tag_weather_cnt' ]]
        pl_result = pl_result.reset_index(drop = True)
        
        self.count_tag_types(pl_result)
        str2list(pl_result, ['playlist_songs'])
        
        pl = pd.merge(model_result, pl_result)
        pl['match_rate'] = pl.matched/pl.tag_cnt
        pl = pl.drop(["matched", "tag_sit_cnt", "tag_mood_cnt", "tag_weather_cnt", "tag_cnt"], axis=1)
        
        pl_song = self.spread_songs(pl)
        self.youtube.columns = [col.lower() for col in self.youtube.columns]
        self.youtube["song_id"] = self.youtube["song_id"].apply(lambda x: str(int(x)))
        
        self.songs = self.songs[["SONG_TITLE", "SONG_ID", "ARTIST_NAME", "ALBUM_TITLE"]]
        self.songs["SONG_ID"] = self.songs["SONG_ID"].apply(lambda x: str(int(x)))
        
        self.song_detail = self.song_detail[self.song_detail.SONG_ID.isna() == False]
        self.song_detail = self.song_detail.reset_index(drop=True)
        
        self.song_detail = self.song_detail[["SONG_ID", "LISTENER_CNT","INFO_GENRE", "PLAY_CNT", "SONG_LIKE"]]
        self.song_detail["SONG_ID"] = self.song_detail["SONG_ID"].apply(lambda x: str(int(x)))
                
        song_info = pd.merge(self.song_detail, self.songs)
        song_info.columns = [col.lower() for col in song_info.columns]
        
        merged = pd.merge(pl_song, song_info)
        
        song_info['info_genre'].apply(lambda x: re.search(r'[\w-]+',x).group()).unique()
        
        merged = pd.merge(merged, self.new_genre)
        merged = pd.merge(merged, self.youtube)
        
        merged['user_genre'] = merged['genre'].apply(lambda x: x in user_genres)
        merged['song_favor'] = (merged.song_like/merged.play_cnt)
        merged['pl_favor'] = merged.pl_like/merged.pl_view
        
        merged = merged[["playlist_id","sim","song_id", "pl_match", "song_title","genre", "user_genre", "pl_favor", "song_favor", "youtube_key", "artist_name", "album_title"]]
        
        self.min_max_scale(merged, "sim")
        self.min_max_scale(merged, "pl_favor")
        self.min_max_scale(merged, "song_favor")
        merged['favor_score'] = merged.song_favor + merged.pl_favor
        
        merged['pl_score'] = merged.pl_favor + merged.pl_match + (1/merged.pl_match)
        rec_result = merged.sort_values(by = ["user_genre", "pl_score", "favor_score"], ascending=False).reset_index(drop=True)
        rec_songs = rec_result[:6][['song_id', 'youtube_key', 'song_title', 'artist_name', 'album_title']]
        
        return rec_songs
    
    def result_to_df(self, id_list : List[int], sim_list:List[float]) -> pd.DataFrame:
        model_result = pd.DataFrame({'playlist_id':id_list, 'cos_sim':sim_list})
        model_result = model_result.groupby('playlist_id').agg({'cos_sim': [max,len]}).reset_index()
        model_result.columns = ['playlist_id', 'cos_sim', 'matched']
        return model_result
    
    def count_tag_types(self, df:pd.DataFrame) -> None:
        df['tag_sit_cnt'] = df['tag_sit_cnt'].apply(lambda x: min(x, 1))
        df['tag_mood_cnt'] = df['tag_mood_cnt'].apply(lambda x: min(x, 1))
        df['tag_weather_cnt'] = df['tag_weather_cnt'].apply(lambda x: min(x, 1))
        df['tag_cnt'] = df.tag_sit_cnt + df.tag_mood_cnt + df.tag_weather_cnt
        
    def spread_songs(self, df: pd.DataFrame) -> pd.DataFrame:
        pl_id = []
        sim = []
        song_id = []
        pl_view = []
        pl_like = []
        pl_match = []

        for id in df.playlist_id:
            i,s, song_list, _, v, l, mr = df[df.playlist_id == id].values.flatten()
            for song in song_list:
                pl_id.append(i)
                sim.append(s)
                song_id.append(song)
                pl_view.append(v)
                pl_like.append(l)
                pl_match.append(mr)
        pl_song = pd.DataFrame(
        {"playlist_id" : pl_id,
        "sim" : sim,
        "song_id" : song_id,
        "pl_view": pl_view,
        "pl_like" : pl_like,
        "pl_match" : pl_match}
        )  

        return pl_song
    
    def min_max_scale(self, df, col:str):
        min_val = min(df[col])
        max_val = max(df[col])
        df[col] = df[col].apply(lambda x: round((x-min_val)/(max_val-min_val), 2))
