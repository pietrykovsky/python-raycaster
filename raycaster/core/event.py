from typing import Callable


class Event:
    def __init__(self):
        self._event_handler = []

    def __iadd__(self, event: Callable) -> "Event":
        self._event_handler.append(event)
        return self
    
    def __isub__(self, event: Callable) -> "Event":
        self._event_handler.remove(event)
        return self
    
    def invoke(self, *args, **kwargs) -> None:
        """
        Invokes all registered events.
        """
        for event in self._event_handler:
            event(*args, **kwargs)
    