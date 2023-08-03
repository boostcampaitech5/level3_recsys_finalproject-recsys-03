from ..document import PlaylistDocument
from ..exception import NotFoundPlaylistException
from ...dto.model import Playlist


class PlaylistRepository:
    def create_playlist(self, genie_id: str, name: str) -> Playlist:
        playlist = PlaylistDocument(genie_id=genie_id, name=name)
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
