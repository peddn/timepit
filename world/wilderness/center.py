import textwrap

from evennia import create_object, search_object

from evennia.contrib.grid import wilderness

from world.wilderness.wilderness import BaseMapProvider

def _string_to_matrix(s: str):
    lines = textwrap.dedent(s).strip("\n").splitlines()
    return [list(row) for row in lines]

class MapContainer:
    def __init__(self, walk_str: str, disp_str: str, walkable_chars=None):
        walk = _string_to_matrix(walk_str)
        disp = _string_to_matrix(disp_str)

        # Immer invertieren: y=0 unten
        self.walk = list(reversed(walk))
        self.disp = list(reversed(disp))

        if len(self.walk) != len(self.disp):
            raise ValueError("walk- und disp-Karte müssen gleich viele Zeilen haben.")
        for wy, dy in zip(self.walk, self.disp):
            if len(wy) != len(dy):
                raise ValueError("walk- und disp-Karte müssen pro Zeile gleich lang sein.")

        self.height = len(self.walk)
        self.width = len(self.walk[0]) if self.height else 0
        self.walkable_chars = walkable_chars or {"."}

    def walkable_at(self, x: int, y: int) -> bool:
        if 0 <= y < self.height and 0 <= x < len(self.walk[y]):
            return self.walk[y][x] in self.walkable_chars
        return False

    def view_rect(self, cx: int, cy: int, w: int, h: int, mark: str = "@") -> str:
        if self.height == 0 or self.width == 0 or w <= 0 or h <= 0:
            return ""
        hw, hh = w // 2, h // 2
        x0, y0 = max(0, cx - hw), max(0, cy - hh)
        x1, y1 = min(self.width - 1, cx + (w - 1 - hw)), min(self.height - 1, cy + (h - 1 - hh))
        rows = []
        for y in range(y1, y0 - 1, -1):
            line = []
            max_x = len(self.disp[y]) - 1
            for x in range(x0, x1 + 1):
                ch = self.disp[y][x] if x <= max_x else " "
                line.append(mark if (x == cx and y == cy and mark) else ch)
            rows.append("".join(line))
        return "\n".join(rows)

# --- Karten: 12 Zeilen × 21 Zeichen ---

WALK_MAP = """
~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~.....~~~~~~~
~~~~~~~...........~~~
~~~~~~.............~~
~~~~~...............~
~~~~~...............~
~~~~~~.............~~
~~~~~~~...........~~~
~~~~~~~~~.....~~~~~~~
~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~
"""

DISP_MAP = """
≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
≈≈≈≈≈≈≈≈≈·····≈≈≈≈≈≈≈
≈≈≈≈≈≈≈···········≈≈≈
≈≈≈≈≈≈·············≈≈
≈≈≈≈≈······▲········≈
≈≈≈≈≈···············≈
≈≈≈≈≈≈·············≈≈
≈≈≈≈≈≈≈···········≈≈≈
≈≈≈≈≈≈≈≈≈·····≈≈≈≈≈≈≈
≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
"""

class CenterMapProvider(BaseMapProvider):

    def __init__(self):
        super().__init__()
        self.map = MapContainer(WALK_MAP, DISP_MAP, walkable_chars={"."})

    def is_valid_coordinates(self, wilderness, coordinates):
        x, y = coordinates
        return self.map.walkable_at(x, y)

    def get_location_name(self, coordinates):
        return "Auf Center"

    def at_prepare_room(self, coordinates, caller, room):
        x, y = coordinates

        view = self.map.view_rect(cx=x, cy=y, w=9, h=7, mark="@")

        room.ndb.active_desc = (
            "Du läufts über eine flache Grasebene. Am Hozizont kannst du das Meer erkennen.\n\n"
            f"{view}"
        )

        # wenn wir uns an den Koordinaten befinden, an denen ein Ausgang sein soll
        if (x, y) == (11, 6):
            room.ndb.active_desc = room.ndb.active_desc + "\n\nHier kannst du mit 'betrete void' zurück ins Nichts."
            room.ndb.dest_room = "void"
            room.cmdset.add("world.wilderness.wilderness_cmd.WildernessLeaveCmdSet")
        else:
            room.ndb.dest_room = None
            room.cmdset.remove("world.wilderness.wilderness_cmd.WildernessLeaveCmd")
