from abc import ABC, abstractmethod


class Updatable(ABC):
    """Abstract class for updatable objects."""

    _updatable_registry = []

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        cls._updatable_registry.append(instance)
        return instance

    @abstractmethod
    def update(self):
        pass

    @classmethod
    def update_all(cls):
        for instance in cls._updatable_registry:
            instance.update()
