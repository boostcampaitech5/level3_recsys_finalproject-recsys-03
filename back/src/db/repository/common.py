from mongoengine import QuerySet
from ..document import ArtistDocument, PlaylistDocument, SongDocument, UserDocument
from ...dto.model import Artist, Playlist, Song, User
from ..exception import NotFoundArtistException, NotFoundPlaylistException, NotFoundSongException, NotFoundUserException


def find_artist_doc_by_dto(artist: Artist) -> ArtistDocument:
    artist = ArtistDocument.objects(genie_id=artist.genie_id).first()

    if not artist:
        raise NotFoundArtistException(f"Can't find artist document: {artist}")

    return artist


def find_playlist_doc_by_dto(playlist: Playlist) -> PlaylistDocument:
    query_set = PlaylistDocument.objects(genie_id=playlist.genie_id)

    if not query_set:
        raise NotFoundPlaylistException(f"Can't find playlist document: {playlist}")

    return query_set.first()


def find_playlist_docs_by_dto(playlists: tuple[Playlist]) -> QuerySet:
    playlists_genie_ids = [playlists.genie_id for playlists in playlists]
    query_set = PlaylistDocument.objects(genie_id__in=playlists_genie_ids)

    if playlists and not query_set:
        raise NotFoundPlaylistException(f"Can't find playlist documents: {playlists}")

    if len(query_set) != len(playlists):
        not_found_playlists = []
        founds = list(query_set)

        for playlist in playlists:
            if playlist in founds:
                not_found_playlists.append(playlist)

        raise NotFoundPlaylistException(f"Can't find playlist documents: {not_found_playlists}")

    return query_set


def find_song_doc_by_dto(song: Song) -> SongDocument:
    query_set = SongDocument.objects(genie_id=song.genie_id)

    if not query_set:
        raise NotFoundSongException(f"Can't find song document: {song}")

    return query_set.first()


def find_song_docs_by_dto(songs: tuple[Song]) -> QuerySet:
    songs_genie_ids = [songs.genie_id for songs in songs]
    query_set = SongDocument.objects(genie_id__in=songs_genie_ids)

    if songs and not query_set:
        raise NotFoundSongException(f"Can't find song documents: {songs}")

    if len(query_set) != len(songs):
        not_found_songs = []
        founds = list(query_set)

        for song in songs:
            if song in founds:
                not_found_songs.append(song)

        raise NotFoundSongException(f"Can't find song documents: {not_found_songs}")

    return query_set


def find_user_doc_by_dto(user: User) -> UserDocument:
    query_set = UserDocument.objects(id=user.id).first()

    if not query_set:
        raise NotFoundUserException(f"Can't find user document: {user}")

    return query_set
