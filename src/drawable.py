from abc import ABC, abstractmethod


class Drawable(ABC):
    """Abstract class for drawable objects."""

    _drawable_registry = []

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        cls._drawable_registry.append(instance)
        return instance

    @abstractmethod
    def draw(self):
        pass

    @classmethod
    def draw_all(cls):
        for instance in cls._drawable_registry:
            instance.draw()
