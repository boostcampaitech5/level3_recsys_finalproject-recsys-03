from mongoengine import Document, StringField, ReferenceField, DateField, IntField, URLField
from ...dto.model import Song
from .artist import ArtistDocument


class SongDocument(Document):
    genie_id = StringField(required=True, unique=True)
    title = StringField(required=True)
    artist = ReferenceField(ArtistDocument, required=True)
    released_date = DateField(required=True)
    like_cnt = IntField(required=True)
    spotify_url = URLField()

    def to_dto(self) -> Song:
        return Song(
            id=str(self.id),
            genie_id=self.genie_id,
            title=self.title,
            artist=self.artist.to_dto(),
            released_date=self.released_date,
            like_cnt=self.like_cnt,
            spotify_url=self.spotify_url,
        )
