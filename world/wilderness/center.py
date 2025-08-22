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
    "w": "Du läufst durch einen dichten, düsteren Wald.",
    "x": "Du solltest auf keinen Fall hier sein.",
}

class CenterMapProvider(BaseMapProvider):
    def __init__(self):
        super().__init__()
        self.manager = WildernessManager(
            width=21,
            height=12,
            display_map=DISP_MAP,
            walkable_map=WALK_MAP,
            description_map=DESC_MAP,
            walkable_chars={"."},
            desc_mapping=DESC_MAPPING,
        )

    def is_valid_coordinates(self, wilderness, coordinates):
        x, y = coordinates
        return self.manager.is_valid_coordinates(x, y)

    def get_location_name(self, coordinates):
        return "Auf Center"

    def at_prepare_room(self, coordinates, caller, room):
        x, y = coordinates

        view = self.manager.render_view(cx=x, cy=y, width=9, height=7)
        desc = self.manager.get_description(x, y) or "Du stehst hier im Nirgendwo."
        room.ndb.active_desc = f"{desc}\n\n{view}"

        if (x, y) == (11, 6):
            room.ndb.active_desc += "\n\nHier kannst du mit 'betrete void' zurück ins Nichts."
            room.ndb.dest_room = "void"
            room.cmdset.add("world.wilderness.wilderness_cmd.WildernessLeaveCmdSet")
        else:
            room.ndb.dest_room = None
            room.cmdset.remove("world.wilderness.wilderness_cmd.WildernessLeaveCmdSet")
