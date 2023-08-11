from mongoengine import DateTimeField, signals
from datetime import datetime


def round_millisecond(dt: datetime):
    return dt.replace(microsecond=round(dt.microsecond, -3))


def utcnow():
    now = datetime.utcnow()
    return round_millisecond(now)


def update_updated_at(sender, document):
    document.updated_at = utcnow()


class CreatedAtMixin:
    created_at = DateTimeField(default=utcnow)
    meta = {"abstract": True}


class UpdatedAtMixin:
    updated_at = DateTimeField(default=utcnow)
    meta = {"abstract": True}


signals.pre_save.connect(update_updated_at, sender=UpdatedAtMixin)
