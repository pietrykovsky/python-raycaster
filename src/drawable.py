from abc import ABC, abstractmethod


class Drawable(ABC):
    """Abstract class for drawable objects."""

    _registry = []

    def __new__(cls):
        instance = super(Drawable, cls).__new__(cls)
        cls._registry.append(instance)
        return instance

    @abstractmethod
    def draw(self):
        pass

    @classmethod
    def draw_all(cls):
        for instance in cls._registry:
            instance.draw()
