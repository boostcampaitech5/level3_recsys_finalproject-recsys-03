from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    ListField,
    ReferenceField,
    BooleanField,
    EmbeddedDocumentField,
    ValidationError,
)
from ...dto.model import Inference, SongsElement
from .user import UserDocument
from .playlist import PlaylistDocument
from .song import SongDocument


class SongsElementEmbeddedDocument(EmbeddedDocument):
    song = ReferenceField(SongDocument, required=True)
    is_like = BooleanField(required=True, default=False)

    def to_dto(self) -> SongsElement:
        return SongsElement(song=self.song, is_like=self.is_like)


def should_have_at_least_one_genre(genres: list[str]):
    if len(genres) <= 0:
        raise ValidationError("Inference should have at least one genere")


def should_have_at_least_one_song(songs: list[SongsElementEmbeddedDocument]):
    if len(songs) <= 0:
        raise ValidationError("Inference should have at least one song")


class InferenceDocument(Document):
    user = ReferenceField(UserDocument, required=True)
    query_img_url = StringField(required=True)
    playlists = ListField(
        ReferenceField(PlaylistDocument),
        required=True,
    )
    songs = ListField(
        EmbeddedDocumentField(SongsElementEmbeddedDocument),
        required=True,
        validation=should_have_at_least_one_song,
    )
    genres = ListField(
        StringField(),
        required=True,
        validation=should_have_at_least_one_genre,
    )

    def to_dto(self) -> Inference:
        return Inference(
            id=str(self.id),
            user=self.user.to_dto(),
            query_img_url=self.query_img_url,
            playlists=[playlist.to_dto() for playlist in self.playlists],
            songs=[song.to_dto() for song in self.songs],
            genres=self.genres,
        )
