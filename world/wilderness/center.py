from typing import Dict
from .wilderness import BaseMapProvider

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

WALK_CHARS = {"."}

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

DESC_MAPPING: Dict[str, str] = {
    ".": "Du läufst über eine flache Grasebene.",
    "w": "Du läufst durch einen dichten, düsteren Wald.",
    "x": "Du solltest auf keinen Fall hier sein.",
}

class CenterMapProvider(BaseMapProvider):
    def __init__(self):
        super().__init__(
            width=21,
            height=12,
            display_map=DISP_MAP,
            walkable_map=WALK_MAP,
            walkable_chars=WALK_CHARS,
            description_map=DESC_MAP,
            desc_mapping=DESC_MAPPING,
            view_size=(9, 7),
        )

    def get_location_name(self, coordinates):
        return "Auf Center"

    def at_prepare_room_extra(self, coordinates, caller, room) -> None:
        x, y = coordinates
        if (x, y) == (11, 6):
            room.ndb.active_desc += "\n\nHier kannst du mit 'betrete void' zurück ins Nichts."
            room.ndb.dest_room = "void"
            room.cmdset.add("world.wilderness.wilderness_cmd.WildernessLeaveCmdSet")
        else:
            room.ndb.dest_room = None
            room.cmdset.remove("world.wilderness.wilderness_cmd.WildernessLeaveCmdSet")
