import math
from functools import partial
from ..db import Playlist, Song
from pydantic import BaseModel


class PlaylistInfo(BaseModel):
    playlist: Playlist
    sim: float
    matched: int


class SongInfo(BaseModel):
    song: Song
    sim: float


class SongExtractor:
    def extract_songs(self, playlists: list[Playlist], sim_list: list[float], selected_genres: list[str]) -> list[Song]:
        playlist_infos = self._convert_playlist_infos(playlists, sim_list)

        # matched_rates = [pl_info.matched / len(pl_info.playlist.tags) for pl_info in playlist_infos]
        song_infos = self._spread_song_infos(playlist_infos)

        sorted_ = self._sorted_info(song_infos, selected_genres)
        dropped_duplicated = self._drop_duplicate_from_song_infos(sorted_)
        dropped_no_spotify_url = self._drop_song_infos_with_no_spotify_url(dropped_duplicated)

        return [song_info.song for song_info in dropped_no_spotify_url]

    def _convert_playlist_infos(self, playlists: list[Playlist], sim_list: list[float]) -> list[PlaylistInfo]:
        playlist_id2info = {}
        for playlist, sim in zip(playlists, sim_list):
            if pl_info := playlist_id2info.get(playlist.id):
                pl_info.sim = max(pl_info.sim, sim)
                pl_info.matched += 1
            else:
                playlist_id2info[playlist.id] = PlaylistInfo(playlist=playlist, sim=math.inf, matched=0)

        return playlist_id2info.values()

    def _spread_song_infos(self, pl_infos: list[PlaylistInfo]) -> list[SongInfo]:
        song_infos = []

        for pl_info in pl_infos:
            song_infos += [SongInfo(song=song, sim=pl_info.sim) for song in pl_info.playlist.songs]

        return song_infos

    def _sorted_info(self, song_infos: list[SongInfo], selected_genres: list[str]) -> list[SongInfo]:
        sorted_ = [None] * len(song_infos)
        sorted_[::3] = sorted(song_infos[::3], key=partial(self._sort_song_info_by_release_date_asc, selected_genres=selected_genres), reverse=True)
        sorted_[1::3] = sorted(
            song_infos[1:][::3], key=partial(self._sort_song_info_by_popularity_asc, selected_genres=selected_genres), reverse=True
        )
        sorted_[2::3] = sorted(song_infos[2:][::3], key=self._sort_song_info_by_similarity_asc, reverse=True)

        return sorted_

    @classmethod
    def _sort_song_info_by_release_date_asc(cls, song_info: SongInfo, selected_genres: list[str]):
        is_matched_genres = any(genre in song_info.song.genres for genre in selected_genres)
        return (is_matched_genres, song_info.song.album.released_date)

    @classmethod
    def _sort_song_info_by_popularity_asc(cls, song_info: SongInfo, selected_genres: list[str]):
        is_matched_genres = any(genre in song_info.song.genres for genre in selected_genres)
        return (is_matched_genres, song_info.song.listener_cnt)

    @classmethod
    def _sort_song_info_by_similarity_asc(cls, song_info: SongInfo):
        return (song_info.sim, song_info.song.listener_cnt)

    def _drop_duplicate_from_song_infos(self, song_infos: list[SongInfo]) -> list[SongInfo]:
        song_id2infos = {}
        for song_info in song_infos:
            song_id2infos[song_info.song.id] = song_info

        return song_id2infos.values()

    def _drop_song_infos_with_no_spotify_url(self, song_infos: list[SongInfo]) -> list[SongInfo]:
        return [song_info for song_info in song_infos if song_info.song.spotify_url]
