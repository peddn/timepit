from evennia.contrib.grid.wilderness import WildernessMapProvider
from .wilderness_tc import BaseWildernessRoom

class BaseMapProvider(WildernessMapProvider):
    """
    Eine universelle MapProvider-Basisklasse, die die Room-Typeclass setzt.
    """
    room_typeclass = BaseWildernessRoom


class Tile:
    """
    Repräsentiert ein Feld auf der Karte mit allen Infos
    aus den unterschiedlichen Layern.
    """
    def __init__(self):
        self.symbol = " "         # aus display_map
        self.walkable = False     # aus walkable_map
        self.description = ""     # aus description_map

    def __repr__(self):
        return f"Tile('{self.symbol}', walkable={self.walkable})"


class WildernessManager:
    """
    Verwaltet Karten-Layer und baut daraus eine 2D-Matrix aus Tiles.
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.display_map = []
        self.walkable_map = []
        self.description_map = []
        self.tiles = []  # endgültige Tile-Matrix

        self._description_mapping: dict[str, str] = {}
        self._walkable_chars: set[str] = set()

    # ---------------- Hilfsmethode ----------------

    def _validate_map(self, mapstring: str) -> list[list[str]]:
        lines = [list(line) for line in mapstring.strip().splitlines()]

        if len(lines) != self.height:
            raise ValueError(f"Map hat {len(lines)} Zeilen, erwartet: {self.height}")
        for i, line in enumerate(lines):
            if len(line) != self.width:
                raise ValueError(
                    f"Zeile {i} hat {len(line)} Spalten, erwartet: {self.width}"
                )

        return lines

    # ---------------- Layer hinzufügen ----------------

    def add_display_map(self, mapstring: str):
        self.display_map = self._validate_map(mapstring)

    def add_walkable_map(self, mapstring: str, walkable_chars: set[str]):
        self.walkable_map = self._validate_map(mapstring)
        self._walkable_chars = walkable_chars

    def add_description_map(self, mapstring: str, mapping: dict[str, str]):
        self.description_map = self._validate_map(mapstring)
        self._description_mapping = mapping

    # ---------------- Tiles bauen ----------------

    def build_tiles(self):
        if not self.display_map:
            raise ValueError("Keine display_map gesetzt.")
        if not self.walkable_map:
            raise ValueError("Keine walkable_map gesetzt.")
        if not self.description_map:
            raise ValueError("Keine description_map gesetzt.")

        self.tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                t = Tile()
                t.symbol = self.display_map[y][x]
                t.walkable = self.walkable_map[y][x] in self._walkable_chars
                code = self.description_map[y][x]
                t.description = self._description_mapping.get(code, "")
                row.append(t)
            self.tiles.append(row)

    # ---------------- Zugriffsmethoden ----------------

    def get_tile(self, x: int, y: int) -> Tile:
        if not self.tiles:
            raise ValueError("Tiles noch nicht gebaut – rufe build_tiles() auf.")
        return self.tiles[y][x]

    def get_map_view(self, cx: int, cy: int, width: int, height: int) -> str:
        """
        Gibt einen Ausschnitt als ASCII-String zurück.
        Die Koordinate (cx, cy) liegt im Zentrum und wird mit '@' markiert.
        """
        if not self.tiles:
            raise ValueError("Tiles noch nicht gebaut – rufe build_tiles() auf.")

        half_w = width // 2
        half_h = height // 2

        start_x = cx - half_w
        start_y = cy - half_h

        lines = []
        for row in range(start_y, start_y + height):
            chars = []
            for col in range(start_x, start_x + width):
                if row == cy and col == cx:
                    # Spielerposition markieren
                    chars.append("@")
                elif 0 <= row < self.height and 0 <= col < self.width:
                    chars.append(self.tiles[row][col].symbol)
                else:
                    chars.append(" ")  # außerhalb der Map
            lines.append("".join(chars))
        return "\n".join(lines)
