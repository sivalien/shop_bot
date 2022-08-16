from abc import ABC, abstractmethod
import functools


def singleton(cls):
    _instance = None

    @functools.wraps(cls.__init__)
    def new_init(*args, **kwargs):
        nonlocal _instance
        if _instance is None:
            _instance = cls(*args, **kwargs)
        return _instance

    return new_init
    

class Shop(ABC):
    def __init__(self, link) -> None:
        self.link = link

    @abstractmethod
    def _get_source_page(self, request: str):
        pass

    @abstractmethod
    def get_items(self, request: str, number: int = 5):
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, str):
            return self.name == __o
        if isinstance(__o, Shop):
            return self.link == __o.link
        raise TypeError

    def __hash__(self) -> int:
        return hash(self.name)
