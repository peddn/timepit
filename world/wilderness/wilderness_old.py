from evennia.contrib.grid.wilderness import WildernessMapProvider
from .wilderness_tc import BaseWildernessRoom

class BaseMapProvider(WildernessMapProvider):
    room_typeclass = BaseWildernessRoom


class MapMatrix:
    """
    Wandelt einen ASCII-Mapstring in eine 2D-Matrix um,
    bei der (0,0) = unten links ist.
    """

    def __init__(self, mapstring: str):
        # Zeilen aus String holen
        lines = mapstring.strip().splitlines()
        # Umkehren, damit index 0 = südlichste Zeile
        lines = list(reversed(lines))

        # Matrix bauen: matrix[y][x] = Zeichen an (x,y)
        self.height = len(lines)
        self.width = max(len(line) for line in lines) if lines else 0
        self.matrix: list[list[str]] = []

        for line in lines:
            row = list(line)
            if len(row) < self.width:  # ggf. rechts auffüllen
                row.extend(" " * (self.width - len(row)))
            self.matrix.append(row)

    def get(self, x: int, y: int) -> str:
        """
        Gibt das Zeichen an Koordinate (x,y) zurück.
        (0,0) = unten links.
        """
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.matrix[y][x]
        return " "  # außerhalb der Map

    def __str__(self) -> str:
        """
        Gibt die gesamte Map in der ursprünglichen Darstellung zurück:
        erste Zeile = Norden (oben), letzte Zeile = Süden (unten).
        """
        return "\n".join("".join(self.matrix[y]) for y in range(self.height - 1, -1, -1))

    def render_view(self, cx: int, cy: int, width: int, height: int) -> str:
        """
        Gibt den Karten-Ausschnitt für den Spieler zurück.
        Mittelpunkt (cx,cy) wird mit '@' markiert.
        Ausgabe: Norden oben, Süden unten, Westen links, Osten rechts.
        """
        hw, hh = width // 2, height // 2
        start_x, end_x = cx - hw, cx + hw
        start_y, end_y = cy - hh, cy + hh

        lines = []
        for y in range(end_y, start_y - 1, -1):  # oben nach unten
            row = []
            for x in range(start_x, end_x + 1):
                row.append("@" if (x == cx and y == cy) else self.get(x, y))
            lines.append("".join(row))
        return "\n".join(lines)
















class Tile:
    """
    Repräsentiert ein Feld auf der Karte mit allen Infos aus den Layern.
    """
    def __init__(self):
        self.symbol = " "         # aus display_map
        self.walkable = False     # aus walkable_map
        self.description = ""     # aus description_map

    def __repr__(self):
        return f"Tile('{self.symbol}', walkable={self.walkable})"


class WildernessManager:
    """
    Manager für Karten-Layer (Display/Walkable/Description) mit Evennia-kompatibler
    Y-Achse (y=0 ist Süden). Rendering zeigt oben = Norden.
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
        """
        Mapstring in Matrix umwandeln, Größe prüfen und ZEILEN UMKEHREN,
        damit y=0 unten (Süden) ist – wie in Evennia/Wilderness.
        """
        lines = [list(line) for line in mapstring.strip().splitlines()]
        lines = list(reversed(lines))  # wichtig: Süden = y0

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
        for y in range(self.height):  # y=0 ist unten (Süden)
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
        return self.tiles[y][x]  # (0,0) = unten links

    def get_map_view(self, cx: int, cy: int, width: int, height: int) -> str:
        """
        ASCII-Ausschnitt um (cx, cy), '@' in der Mitte.
        Ausgabe beginnt Unten-Links: erste Zeile = südlichste Zeile, erstes Zeichen = westlichste Spalte.
        Schneidet an Kartenrändern ab (kein Padding).
        """
        if not self.tiles:
            raise ValueError("Tiles noch nicht gebaut – rufe build_tiles() auf.")

        hw, hh = width // 2, height // 2
        start_x, end_x = cx - hw, cx + hw
        start_y, end_y = cy - hh, cy + hh

        x0 = max(0, start_x)
        x1 = min(self.width - 1, end_x)
        y0 = max(0, start_y)
        y1 = min(self.height - 1, end_y)

        lines = []
        # Von unten (Süden, kleines y) nach oben (Norden, großes y)
        for y in range(y0, y1 + 1):
            row = []
            # Von Westen (kleines x) nach Osten (großes x)
            for x in range(x0, x1 + 1):
                row.append("@" if (x == cx and y == cy) else self.tiles[y][x].symbol)
            lines.append("".join(row))

        return "\n".join(lines)
