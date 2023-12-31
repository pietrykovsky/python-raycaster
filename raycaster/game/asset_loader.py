import os
import pygame

from raycaster.core import Settings


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

            cls.GAME_PATH = os.path.dirname(os.path.abspath(__file__))
            cls.ROOT_PATH = os.path.dirname(cls.GAME_PATH)
            cls.ASSETS_PATH = os.path.join(cls.ROOT_PATH, "assets")
            cls.WALL_TEXTURES_PATH = os.path.join(cls.ASSETS_PATH, "walls")
            cls.OBJECTS_SPRITES_PATH = os.path.join(cls.ASSETS_PATH, "objects")
            cls.STATIC_SPRITES_PATH = os.path.join(cls.OBJECTS_SPRITES_PATH, "static")
            cls.ANIMATED_SPRITES_PATH = os.path.join(
                cls.OBJECTS_SPRITES_PATH, "animated"
            )

            cls._walls = cls._load_walls_textures()
            cls._static_objects = cls._load_static_sprites()
            cls._animated_objects = cls._load_animated_sprites()
        return cls._instance

    @property
    def wall_textures(self) -> dict[int, pygame.Surface]:
        return self._walls.copy()

    @property
    def static_objects(self) -> dict[int, pygame.Surface]:
        return self._static_objects.copy()

    @property
    def animated_objects(self) -> dict[int, list[pygame.Surface]]:
        return self._animated_objects.copy()

    @classmethod
    def _resize_to_cell_size(cls, surface: pygame.Surface) -> pygame.Surface:
        """
        Resizes the given surface to the cell size.
        """
        cell_size = Settings().CELL_SIZE
        s_width, s_height = surface.get_size()
        s_ratio = s_width / s_height
        s_width, s_height = (
            (int(cell_size * s_ratio), cell_size)
            if s_width < s_height
            else (int(cell_size / s_ratio), cell_size)
        )
        return pygame.transform.scale(surface, (s_width, s_height))

    @classmethod
    def _load_walls_textures(cls) -> dict[int, pygame.Surface]:
        """
        Loads all wall textures from the assets/walls directory.
        """
        walls = {}
        for file in os.listdir(cls.WALL_TEXTURES_PATH):
            file_path = os.path.join(cls.WALL_TEXTURES_PATH, file)
            key = int(os.path.splitext(file)[0])
            surface = pygame.image.load(file_path).convert()
            walls[key] = cls._resize_to_cell_size(surface)
        return walls

    @classmethod
    def _load_static_sprites(cls) -> dict[str, pygame.Surface]:
        """
        Loads all static sprites from the assets/objects/static directory.
        """
        static_objects = {}
        for file in os.listdir(cls.STATIC_SPRITES_PATH):
            file_path = os.path.join(cls.STATIC_SPRITES_PATH, file)
            key = str(os.path.splitext(file)[0])
            surface = pygame.image.load(file_path).convert_alpha()
            static_objects[key] = cls._resize_to_cell_size(surface)
        return static_objects

    @classmethod
    def _load_animated_sprites(cls) -> dict[str, list[pygame.Surface]]:
        """
        Loads all animated sprites from the assets/objects/animated directory.
        """
        animated_objects = {}
        for dir in os.listdir(cls.ANIMATED_SPRITES_PATH):
            dir_path = os.path.join(cls.ANIMATED_SPRITES_PATH, dir)
            animated_objects[dir] = []
            files = os.listdir(dir_path)
            files.sort()
            for file in files:
                file_path = os.path.join(dir_path, file)
                surface = pygame.image.load(file_path).convert_alpha()
                surface = cls._resize_to_cell_size(surface)
                animated_objects[dir].append(surface)
        return animated_objects
