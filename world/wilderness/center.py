from evennia.contrib.grid import wilderness

from world.wilderness.wilderness import BaseMapProvider, WildernessManager

# --- Karten: 12 Zeilen × 21 Zeichen ---

WALK_MAP = """
xxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxx
xxxxxxxxx.....xxxxxxx
xxxxxxx...........xxx
xxxxxx.............xx
xxxxx...............x
xxxxx...............x
xxxxxx.............xx
xxxxxxx...........xxx
xxxxxxxxx.....xxxxxxx
xxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxx
"""

DISP_MAP = """
~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~.....~~~~~~~
~~~~~~~...........~~~
~~~~~~.............~~
~~~~~......x........~
~~~~~...............~
~~~~~~.......oOoOo.~~
~~~~~~~...oOoOoOOo~~~
~~~~~~~~~..OoO~~~~~~~
~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~
"""

DESC_MAP = """
xxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxx
xxxxxxxxx.....xxxxxxx
xxxxxxx...........xxx
xxxxxx.............xx
xxxxx...............x
xxxxx...............x
xxxxxx.......wwwww.xx
xxxxxxx...wwwwwwwwxxx
xxxxxxxxx..wwwxxxxxxx
xxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxx
"""

DESC_MAPPING = {
    ".": "Du läufst über eine flache Grasebene.",
    "w": "Du läufts durch einen dichten, düsteren Wald.",
    "x": "Du solltest auf keinen Fall hier sein.",
}

class CenterMapProvider(BaseMapProvider):
    def __init__(self):
        super().__init__()
        # manager mit richtiger größe anlegen
        self.manager = WildernessManager(width=21, height=12)
        self.manager.add_display_map(DISP_MAP)
        self.manager.add_walkable_map(WALK_MAP, walkable_chars={"."})
        self.manager.add_description_map(DESC_MAP, mapping=DESC_MAPPING)
        self.manager.build_tiles()

    def is_valid_coordinates(self, wilderness, coordinates):
        x, y = coordinates
        # prüft walkable vom tile
        return self.manager.get_tile(x, y).walkable

    def get_location_name(self, coordinates):
        return "Auf Center"

    def at_prepare_room(self, coordinates, caller, room):
        x, y = coordinates

        # 9x7 sichtfenster um die aktuelle position
        view = self.manager.get_map_view(cx=x, cy=y, width=9, height=7)

        tile = self.manager.get_tile(x, y)

        desc = tile.description or "Du stehst hier im Nirgendwo."
        room.ndb.active_desc = f"{desc}\n\n{view}"

        # dynamischer Ausgang bei bestimmter Koordinate
        if (x, y) == (11, 6):
            room.ndb.active_desc += "\n\nHier kannst du mit 'betrete void' zurück ins Nichts."
            room.ndb.dest_room = "void"
            room.cmdset.add("world.wilderness.wilderness_cmd.WildernessLeaveCmdSet")
        else:
            room.ndb.dest_room = None
            room.cmdset.remove("world.wilderness.wilderness_cmd.WildernessLeaveCmdSet")
