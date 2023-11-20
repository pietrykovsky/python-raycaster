import os
import pygame

from settings import Settings


class AssetLoader:
    _instance = None

    # TEXTURES RELATED
    ROOT_PATH: str
    ASSETS_PATH: str
    WALL_TEXTURES_PATH: str
    OBJECTS_SPRITES_PATH: str

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls.ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
            cls.ASSETS_PATH = os.path.join(cls.ROOT_PATH, "assets")
            cls.WALL_TEXTURES_PATH = os.path.join(cls.ASSETS_PATH, "walls")
            cls.OBJECTS_SPRITES_PATH = os.path.join(cls.ASSETS_PATH, "objects")
            cls.STATIC_SPRITES_PATH = os.path.join(cls.OBJECTS_SPRITES_PATH, "static")

            cls._walls = cls._load_walls_textures()
            cls._static_objects = cls._load_static_sprites()
        return cls._instance

    @property
    def wall_textures(self) -> dict[int, pygame.Surface]:
        return self._walls.copy()

    @property
    def static_objects(self) -> dict[int, pygame.Surface]:
        return self._static_objects.copy()

    @classmethod
    def _load_walls_textures(cls):
        """
        Loads all wall textures from the assets/walls directory.
        """
        walls = {}
        cell_size = Settings().CELL_SIZE
        for file in os.listdir(cls.WALL_TEXTURES_PATH):
            file_path = os.path.join(cls.WALL_TEXTURES_PATH, file)
            key = int(os.path.splitext(file)[0])
            surface = pygame.image.load(file_path).convert()
            walls[key] = pygame.transform.scale(surface, (cell_size, cell_size))
        return walls

    @classmethod
    def _load_static_sprites(cls):
        """
        Loads all wall textures from the assets/walls directory.
        """
        static_objects = {}
        cell_size = Settings().CELL_SIZE
        for file in os.listdir(cls.STATIC_SPRITES_PATH):
            file_path = os.path.join(cls.STATIC_SPRITES_PATH, file)
            key = str(os.path.splitext(file)[0])
            surface = pygame.image.load(file_path).convert()
            static_objects[key] = pygame.transform.scale(
                surface, (cell_size, cell_size)
            )
        return static_objects
