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
        """
        Update the object's state.
        """
        pass

    @classmethod
    def unregister(cls, instance: "Updatable"):
        cls._updatable_registry.remove(instance)

    @classmethod
    def update_all(cls):
        """
        Update the state of all updatable objects.
        """
        for instance in cls._updatable_registry:
            instance.update()
