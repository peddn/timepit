from typing import Set, Dict

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


class WildernessManager:
    """
    Verwalter für drei Layer (Display/Walkable/Description) auf Basis von MapMatrix.
    Map-Strings + width/height + Mapping werden im Konstruktor übergeben.
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
        self._width: int = width
        self._height: int = height

        self.display: MapMatrix = MapMatrix(display_map)
        self.walkable: MapMatrix = MapMatrix(walkable_map)
        self.description: MapMatrix = MapMatrix(description_map)

        # Größen prüfen
        for name, mm in [
            ("display_map", self.display),
            ("walkable_map", self.walkable),
            ("description_map", self.description),
        ]:
            if mm.width != self._width or mm.height != self._height:
                raise ValueError(
                    f"{name} hat Größe {mm.width}x{mm.height}, "
                    f"erwartet: {self._width}x{self._height}"
                )

        self._walkable_chars: Set[str] = set(walkable_chars)
        self._desc_mapping: Dict[str, str] = dict(desc_mapping)

    # ---------------- Abfragen ----------------

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def is_valid_coordinates(self, x: int, y: int) -> bool:
        ch = self.walkable.get(x, y)
        return ch in self._walkable_chars

    def get_symbol(self, x: int, y: int) -> str:
        return self.display.get(x, y)

    def get_description(self, x: int, y: int) -> str:
        code = self.description.get(x, y)
        return self._desc_mapping.get(code, "")

    def get_tile_info(self, x: int, y: int) -> dict:
        return {
            "x": x,
            "y": y,
            "symbol": self.get_symbol(x, y),
            "walkable": self.is_valid_coordinates(x, y),
            "description": self.get_description(x, y),
        }

    # ---------------- Rendering ----------------

    def render_view(self, cx: int, cy: int, width: int, height: int) -> str:
        """
        Spieleransicht: Ausschnitt um (cx,cy), '@' in der Mitte.
        Anzeige: Norden oben, Westen links. Ränder werden mit Leerzeichen gefüllt.
        """
        return self.display.render_view(cx, cy, width, height)
