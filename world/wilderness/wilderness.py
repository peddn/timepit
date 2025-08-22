from evennia.contrib.grid.wilderness import WildernessMapProvider
from .wilderness_tc import BaseWildernessRoom

class BaseMapProvider(WildernessMapProvider):
    room_typeclass = BaseWildernessRoom

class Tile:
    def __init__(self):
        self.symbol = " "
        self.walkable = False
        self.description = ""

    def __repr__(self):
        return f"Tile('{self.symbol}', walkable={self.walkable})"

class WildernessManager:
    """
    Reproduziert das bewährte Verhalten deines alten MapContainer:
    - Mapstrings werden beim Laden ZEILEN-UMGEKEHRT (y=0 ist unten/Süden).
    - Rendering zeigt oben = Norden (y abwärts iterieren).
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.display_map: list[list[str]] = []
        self.walkable_map: list[list[str]] = []
        self.description_map: list[list[str]] = []
        self.tiles: list[list[Tile]] = []

        self._description_mapping: dict[str, str] = {}
        self._walkable_chars: set[str] = set()

    # ---------------- intern ----------------

    def _validate_map(self, mapstring: str) -> list[list[str]]:
        lines = [list(line) for line in mapstring.strip().splitlines()]
        # wie im alten MapContainer: invertieren, damit y=0 unten ist
        lines = list(reversed(lines))

        if len(lines) != self.height:
            raise ValueError(f"Map hat {len(lines)} Zeilen, erwartet: {self.height}")
        for i, line in enumerate(lines):
            if len(line) != self.width:
                raise ValueError(f"Zeile {i} hat {len(line)} Spalten, erwartet: {self.width}")

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
        for y in range(self.height):  # y=0 ist unten, wie Evennia rechnet
            row: list[Tile] = []
            for x in range(self.width):
                t = Tile()
                t.symbol = self.display_map[y][x]
                t.walkable = self.walkable_map[y][x] in self._walkable_chars
                code = self.description_map[y][x]
                t.description = self._description_mapping.get(code, "")
                row.append(t)
            self.tiles.append(row)

    # ---------------- Zugriff & Rendering ----------------

    def get_tile(self, x: int, y: int) -> Tile:
        if not self.tiles:
            raise ValueError("Tiles noch nicht gebaut – rufe build_tiles() auf.")
        return self.tiles[y][x]  # (0,0) unten links

    def get_map_view(self, cx: int, cy: int, width: int, height: int) -> str:
        """
        ASCII-Ausschnitt um (cx, cy), mit '@' in der Mitte.
        Anzeige-Orientierung wie im alten MapContainer:
        - oben = Norden (wir iterieren y abwärts)
        - Fenster wird an Mapränder geclamped und mit Leerzeichen gepaddet
        """
        if not self.tiles:
            raise ValueError("Tiles noch nicht gebaut – rufe build_tiles() auf.")

        if width <= 0 or height <= 0 or self.width == 0 or self.height == 0:
            return ""

        hw, hh = width // 2, height // 2
        start_x = cx - hw
        start_y = cy - hh
        end_x = cx + (width - 1 - hw)
        end_y = cy + (height - 1 - hh)

        # Clamps für den Teil, der IN der Karte liegt
        x0 = max(0, start_x)
        y0 = max(0, start_y)
        x1 = min(self.width - 1, end_x)
        y1 = min(self.height - 1, end_y)

        lines: list[str] = []

        # Top-Padding (falls Sichtfenster über Karte hinaus nach Norden geht)
        top_pad = max(0, end_y - (self.height - 1))
        if top_pad:
            lines.extend([" " * width] * top_pad)

        # y von oben (y1) nach unten (y0) – oben = Norden
        for y in range(y1, y0 - 1, -1):
            chars: list[str] = []

            # Left-Padding (falls Sichtfenster links neben der Karte beginnt)
            left_pad = max(0, 0 - start_x)
            if left_pad:
                chars.extend([" "] * left_pad)

            # sichtbarer, geclampter Bereich
            for x in range(x0, x1 + 1):
                if x == cx and y == cy:
                    chars.append("@")
                else:
                    chars.append(self.tiles[y][x].symbol)

            # Right-Padding (falls Sichtfenster rechts über die Karte hinausgeht)
            right_pad = max(0, end_x - (self.width - 1))
            if right_pad:
                chars.extend([" "] * right_pad)

            lines.append("".join(chars))

        # Bottom-Padding (falls Sichtfenster unter Karte hinaus nach Süden geht)
        bottom_pad = max(0, 0 - start_y)
        if bottom_pad:
            lines.extend([" " * width] * bottom_pad)

        return "\n".join(lines)
