from django.db import models
from django.db.models import QuerySet


class EventManager(models.Manager):
    def with_related(self, *args: str) -> QuerySet:
        select_related_fields = ["creator", "category"] + list(args)
        return self.select_related(*set(select_related_fields))
