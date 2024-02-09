from typing import Generic, Type, TypeVar

from django.db import models
from django.db.models import QuerySet

ModelType = TypeVar("ModelType", bound=models.Model)


class BaseRepository(Generic[ModelType]):
    model: Type[ModelType]

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_all(self) -> QuerySet[ModelType]:
        return self.model.objects.all()

    def get_by_id(self, pk: str) -> ModelType:
        return self.model.objects.get(pk=pk)

    def create(self, **kwargs) -> ModelType:
        return self.model.objects.create(**kwargs)

    def filter(self, **kwargs) -> QuerySet[ModelType]:
        return self.model.objects.filter(**kwargs)

    @staticmethod
    def update(instance: ModelType, **kwargs) -> ModelType:
        for attr, value in kwargs.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    @staticmethod
    def delete(instance: ModelType) -> None:
        instance.delete()
