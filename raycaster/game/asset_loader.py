import os
import pygame

from raycaster.core import Settings
from raycaster.const import AnimationType, WeaponRepresentation


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
            cls.ENEMIES_SPRITES_PATH = os.path.join(cls.OBJECTS_SPRITES_PATH, "enemies")
            cls.WEAPONS_PATH = os.path.join(cls.OBJECTS_SPRITES_PATH, "weapons")
            cls.FONTS_PATH = os.path.join(cls.ASSETS_PATH, "fonts")
            cls.DOOM_FONT_PATH = os.path.join(cls.FONTS_PATH, "DooM.ttf")
            cls.CTA_DIR_PATH = os.path.join(cls.ASSETS_PATH, "call_to_action")

            cls._walls = cls._load_walls_textures()
            cls._static_objects = cls._load_static_sprites()
            cls._animated_objects = cls._load_animated_sprites()
            cls._enemies = cls._load_enemies()
            cls._weapons = cls._load_weapons()
            cls._cta_screens = cls._load_cta_screens()

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

    @property
    def enemies(self) -> dict[str, dict[AnimationType, list[pygame.Surface]]]:
        return self._enemies.copy()

    @property
    def weapons(self) -> dict[str, dict[str, list[pygame.Surface] | pygame.Surface]]:
        return self._weapons.copy()

    @property
    def game_over_cta(self) -> pygame.Surface:
        return self._cta_screens["game_over"]

    @property
    def victory_cta(self) -> pygame.Surface:
        return self._cta_screens["victory"]

    @property
    def start_game_cta(self) -> pygame.Surface:
        return self._cta_screens["start"]

    @classmethod
    def load_doom_font(cls, size: int) -> pygame.font.Font:
        """
        Loads the font from the assets/fonts directory.
        """
        font_path = cls.DOOM_FONT_PATH
        return pygame.font.Font(font_path, size)

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
            animated_objects[dir] = cls._load_sprites_to_list(
                animated_objects[dir], dir_path
            )
        return animated_objects

    @classmethod
    def _load_enemies(cls) -> dict[str, dict[AnimationType, list[pygame.Surface]]]:
        """
        Loads all enemies from the assets/objects/enemies directory.
        """
        enemies = {}
        for dir in os.listdir(cls.ENEMIES_SPRITES_PATH):
            dir_path = os.path.join(cls.ENEMIES_SPRITES_PATH, dir)
            enemies[dir] = {}
            for anim_type in AnimationType:
                enemies[dir][anim_type] = []
                anim_dir_path = os.path.join(dir_path, anim_type.value)
                enemies[dir][anim_type] = cls._load_sprites_to_list(
                    enemies[dir][anim_type], anim_dir_path
                )
        return enemies

    @classmethod
    def _load_weapons(
        cls,
    ) -> dict[str, dict[str, list[pygame.Surface] | pygame.Surface]]:
        """
        Loads all weapons from the assets/objects/weapons directory.
        """
        weapons = {}
        for dir in os.listdir(cls.WEAPONS_PATH):
            dir_path = os.path.join(cls.WEAPONS_PATH, dir)
            gui = WeaponRepresentation.GUI.value
            sprite = WeaponRepresentation.SPRITE.value
            gui_path = os.path.join(dir_path, gui)
            sprite_path = os.path.join(dir_path, sprite)
            weapons[dir] = {}
            weapons[dir][gui] = []
            weapons[dir][gui] = cls._load_sprites_to_list(
                weapons[dir][gui], gui_path, resize_to_cell_size=False
            )
            weapons[dir][gui] = [
                cls._resize_weapon_gui_representation(surface)
                for surface in weapons[dir][gui]
            ]
            weapons[dir][sprite] = []
            weapons[dir][sprite] = cls._load_sprites_to_list(
                weapons[dir][sprite], sprite_path
            )[0]
        return weapons

    @classmethod
    def _load_sprites_to_list(
        cls, collection: list, dir_path: str, resize_to_cell_size=True
    ) -> list[pygame.Surface]:
        """
        Loads all sprites from the given path and appends them to the given collection.
        """
        files = os.listdir(dir_path)
        files.sort()
        for file in files:
            file_path = os.path.join(dir_path, file)
            surface = pygame.image.load(file_path).convert_alpha()
            if resize_to_cell_size:
                surface = cls._resize_to_cell_size(surface)
            collection.append(surface)
        return collection

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
    def _resize_weapon_gui_representation(
        cls, surface: pygame.Surface
    ) -> pygame.Surface:
        """
        Resizes the weapon's gui representation to half of the screen height.
        """
        dest_height = Settings().SCREEN_HEIGHT // 2
        width, height = surface.get_size()
        ratio = dest_height / height
        dest_width = int(width * ratio)
        surface = pygame.transform.scale(surface, (dest_width, dest_height))
 
        return surface

    @classmethod
    def _load_cta_screens(cls) -> pygame.Surface:
        """
        Loads background image from the background_image directory.
        """
        screens = {}
        for file in os.listdir(cls.CTA_DIR_PATH):
            file_path = os.path.join(cls.CTA_DIR_PATH, file)
            key = str(os.path.splitext(file)[0])
            surface = pygame.image.load(file_path).convert()
            screens[key] = surface
        return screens
