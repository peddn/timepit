from evennia.contrib.grid.wilderness import WildernessRoom

class BaseWildernessRoom(WildernessRoom):
    """
    Ein universeller Wilderness-Raum.
    Erweiterbar für alle Maps.
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.tags.add("wilderness")
