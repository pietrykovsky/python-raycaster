from abc import ABC, abstractmethod


class Updatable(ABC):
    """Abstract class for updateable objects."""

    _registry = []

    def __new__(cls):
        instance = super(Updatable, cls).__new__(cls)
        cls._registry.append(instance)
        return instance

    @abstractmethod
    def update(self):
        pass

    @classmethod
    def update_all(cls):
        for instance in cls._registry:
            instance.update()
