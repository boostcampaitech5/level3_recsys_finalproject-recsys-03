from mongoengine import Document, StringField
from ...dto.artist import Artist


class ArtistDocument(Document):
    genie_id = StringField(required=True, unique=True)
    name = StringField(required=True)

    def to_dto(self) -> Artist:
        return Artist(id=str(self.id), genie_id=self.genie_id, name=self.name)
