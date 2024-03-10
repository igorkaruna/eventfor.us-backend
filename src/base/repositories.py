from typing import Generic, Type, TypeVar

from django.db import models
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


ModelType = TypeVar("ModelType", bound=models.Model)


class BaseRepository(Generic[ModelType]):
    model: Type[ModelType]

    def __init__(self, model: Type[ModelType]):
        self.model = model

    @classmethod
    def get(cls, **kwargs) -> ModelType:
        return get_object_or_404(cls.model, **kwargs)

    @classmethod
    def get_all(cls) -> QuerySet[ModelType]:
        return cls.model.objects.all()

    @classmethod
    def get_by_id(cls, pk: str) -> ModelType:
        return cls.model.objects.get(pk=pk)

    @classmethod
    def create(cls, **kwargs) -> ModelType:
        return cls.model.objects.create(**kwargs)

    @classmethod
    def filter(cls, **kwargs) -> QuerySet[ModelType]:
        return cls.model.objects.filter(**kwargs)

    @staticmethod
    def update(instance: ModelType, **kwargs) -> ModelType:
        for attr, value in kwargs.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    @staticmethod
    def delete(instance: ModelType) -> None:
        instance.delete()
