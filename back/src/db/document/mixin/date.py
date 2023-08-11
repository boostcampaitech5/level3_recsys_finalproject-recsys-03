from mongoengine import DateTimeField
from datetime import datetime


def utcnow():
    now = datetime.utcnow()
    return now.replace(microsecond=round(now.microsecond, -3))


class CreatedAtMixin:
    created_at = DateTimeField(default=utcnow)
    meta = {"abstract": True}


class UpdatedAtMixin:
    updated_at = DateTimeField(default=utcnow)
    meta = {"abstract": True}
