from typing import Tuple, Set, Dict
from evennia.contrib.grid.wilderness import WildernessMapProvider
from .wilderness_tc import BaseWildernessRoom


# ---------- Core helpers ----------
class MapMatrix:
    """
    ASCII-Map → 2D-Matrix mit (0,0) = unten links.
    """
    def __init__(self, mapstring: str):
        lines = mapstring.strip().splitlines()
        lines = list(reversed(lines))  # südlichste Zeile zuerst
        self.height = len(lines)
        self.width = max((len(line) for line in lines), default=0)
        self.matrix: list[list[str]] = []
        for line in lines:
            row = list(line)
            if len(row) < self.width:
                row.extend(" " * (self.width - len(row)))
            self.matrix.append(row)

    def get(self, x: int, y: int) -> str:
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.matrix[y][x]
        return " "

    def __str__(self) -> str:
        return "\n".join("".join(self.matrix[y]) for y in range(self.height - 1, -1, -1))

    def render_view(self, cx: int, cy: int, width: int, height: int) -> str:
        hw, hh = width // 2, height // 2
        start_x, end_x = cx - hw, cx + hw
        start_y, end_y = cy - hh, cy + hh

        lines = []
        for y in range(end_y, start_y - 1, -1):       # oben → unten
            row = []
            for x in range(start_x, end_x + 1):       # west → ost
                row.append("@" if (x == cx and y == cy) else self.get(x, y))
            lines.append("".join(row))
        return "\n".join(lines)

class WildernessManager:
    """
    Drei Layer (Display/Walkable/Description) auf MapMatrix-Basis.
    """
    def __init__(
        self,
        width: int,
        height: int,
        display_map: str,
        walkable_map: str,
        description_map: str,
        walkable_chars: Set[str],
        desc_mapping: Dict[str, str],
    ):
        self._width = width
        self._height = height

        self.display = MapMatrix(display_map)
        self.walkable = MapMatrix(walkable_map)
        self.description = MapMatrix(description_map)

        for name, mm in (("display_map", self.display), ("walkable_map", self.walkable), ("description_map", self.description)):
            if (mm.width, mm.height) != (self._width, self._height):
                raise ValueError(f"{name} hat Größe {mm.width}x{mm.height}, erwartet: {self._width}x{self._height}")

        self._walkable_chars = set(walkable_chars)
        self._desc_mapping = dict(desc_mapping)

    @property
    def width(self) -> int: return self._width
    @property
    def height(self) -> int: return self._height

    def is_valid_coordinates(self, x: int, y: int) -> bool:
        return self.walkable.get(x, y) in self._walkable_chars

    def get_description(self, x: int, y: int) -> str:
        return self._desc_mapping.get(self.description.get(x, y), "")

    def render_view(self, cx: int, cy: int, width: int, height: int) -> str:
        return self.display.render_view(cx, cy, width, height)


# ---------- Base provider (constructor takes map data) ----------
class BaseMapProvider(WildernessMapProvider):
    """
    Wiederverwendbare Basisklasse. Karten-/Mapping-Daten werden im Konstruktor
    übergeben; konkrete Provider (z. B. Center) rufen super().__init__(...) mit ihren
    Maps/Parametern auf und überschreiben nur noch Namens-/Spezial-Hooks.
    """
    room_typeclass = BaseWildernessRoom

    def __init__(
        self,
        *,
        width: int,
        height: int,
        display_map: str,
        walkable_map: str,
        description_map: str,
        walkable_chars: Set[str],
        desc_mapping: Dict[str, str],
        view_size: Tuple[int, int] = (9, 7),
    ):
        super().__init__()
        self.manager = WildernessManager(
            width=width,
            height=height,
            display_map=display_map,
            walkable_map=walkable_map,
            description_map=description_map,
            walkable_chars=walkable_chars,
            desc_mapping=desc_mapping,
        )
        self._view_size = view_size

    # ---- Hooks (können überschrieben werden) ----
    def get_location_name(self, coordinates) -> str:
        return "Wilderness"

    def at_prepare_room_extra(self, coordinates, caller, room) -> None:
        # für exits/cmdsets/zusatztext im konkreten Provider
        pass

    # ---- Generische Implementierungen ----
    def is_valid_coordinates(self, wilderness, coordinates):
        x, y = coordinates
        return self.manager.is_valid_coordinates(x, y)

    def at_prepare_room(self, coordinates, caller, room):
        x, y = coordinates
        vw, vh = self._view_size
        view = self.manager.render_view(cx=x, cy=y, width=vw, height=vh)
        desc = self.manager.get_description(x, y) or "Du stehst hier im Nirgendwo."
        room.ndb.active_desc = f"{desc}\n\n{view}"
        self.at_prepare_room_extra(coordinates, caller, room)
