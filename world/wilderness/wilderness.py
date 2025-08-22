from evennia.contrib.grid.wilderness import WildernessMapProvider
from .wilderness_tc import BaseWildernessRoom

class BaseMapProvider(WildernessMapProvider):
    """
    Eine universelle MapProvider-Basisklasse, die die Room-Typeclass setzt.
    """
    room_typeclass = BaseWildernessRoom
