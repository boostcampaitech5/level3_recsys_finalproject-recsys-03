from ..document import SongDocument
from ...dto.model import Artist, Song
from ..exception import NotFoundSongException
from .common import find_artist_doc_by_dto
from datetime import datetime


class SongRepository:
    def create_song(self, genie_id: str, title: str, artist: Artist, released_date: datetime, like_cnt: int, spotify_url: str) -> Song:
        song = SongDocument(
            genie_id=genie_id,
            title=title,
            artist=find_artist_doc_by_dto(artist),
            released_date=released_date,
            like_cnt=like_cnt,
            spotify_url=spotify_url,
        )
        saved: SongDocument = song.save()
        return saved.to_dto()

    def delete_by_genie_id(self, genie_id: str) -> None:
        query_set = SongDocument.objects(genie_id=genie_id)

        if not query_set:
            raise NotFoundSongException(f"Can't find song document: genie_id={genie_id}")

        query_set.delete()

    def find_by_genie_id(self, genie_id: str) -> Song | None:
        song: SongDocument = SongDocument.objects(genie_id=genie_id).first()

        if not song:
            return None

        return song.to_dto()

    def find_all(self) -> list[Song]:
        songs: list[SongDocument] = list(SongDocument.objects)
        return [song.to_dto() for song in songs]
