from ..document import PlaylistDocument
from ..exception import NotFoundPlaylistException
from ...dto.model import Playlist, Song
from .common import find_song_docs_by_dto


class PlaylistRepository:
    def create_playlist(self, genie_id: str, title: str, like_cnt: int, view_cnt: int, tags: list[str], songs: list[Song], img_url: str) -> Playlist:
        song_docs = find_song_docs_by_dto(songs)
        playlist = PlaylistDocument(genie_id=genie_id, title=title, like_cnt=like_cnt, view_cnt=view_cnt, tags=tags, songs=song_docs, img_url=img_url)
        saved: PlaylistDocument = playlist.save()
        return saved.to_dto()

    def delete_by_genie_id(self, genie_id: str) -> None:
        playlist: PlaylistDocument = PlaylistDocument.objects(genie_id=genie_id)

        if not playlist:
            raise NotFoundPlaylistException(f"Can't find playlist document: genie_id={genie_id}")

        playlist.delete()

    def find_by_genie_id(self, genie_id: str) -> Playlist:
        playlist: PlaylistDocument = PlaylistDocument.objects(genie_id=genie_id).first()

        if not playlist:
            return None

        return playlist.to_dto()

    def find_all(self) -> list[Playlist]:
        playlists: list[PlaylistDocument] = list(PlaylistDocument.objects)
        return [playlist.to_dto() for playlist in playlists]
