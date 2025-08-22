import re

from evennia import CmdSet, search_object
from evennia.contrib.grid import wilderness
from commands.command import Command

class CmdEnterWilderness(Command):
    """
    Betrete eine Wilderness.
    """
    key = "betrete"
    aliases = ["betr"]
    locks = "cmd:all()"

    def parse(self):
        targets = re.sub(r"\s+", " ", self.args).strip().split()
        self.target = targets[0].lower() if targets else None

    def func(self):
        caller = self.caller
        room = self.obj

        if not self.target:
            caller.msg("Was willst du betreten?")
            return

        if not room.db.dest_wilderness:
            caller.msg("Kein Wilderness-Ziel in diesem Raum definiert.")
            return

        dest_name, coords = room.db.dest_wilderness

        if self.target != dest_name:
            caller.msg(f"'{self.target}' kannst du nicht betreten.")
            return

        caller.msg(f"Du betrittst {self.target} bei {coords}")
        wilderness.enter_wilderness(caller, coords)
        caller.execute_cmd("look")


class CmdLeaveWilderness(Command):
    """
    Verlasse eine Wilderness.
    """
    key = "betrete"
    aliases = ["betr"]
    locks = "cmd:all()"

    def parse(self):
        targets = re.sub(r"\s+", " ", self.args).strip().split()
        self.target = targets[0].lower() if targets else None

    def func(self):
        caller = self.caller
        room = self.obj

        if not self.target:
            caller.msg("Was willst du betreten?")
            return

        if not room.ndb.dest_room:
            caller.msg("Kein Zielraum in diesem Raum definiert.")
            return

        dest_room_key = room.ndb.dest_room

        if self.target != dest_room_key:
            caller.msg(f"'{self.target}' kannst du nicht betreten.")
            return

        destination_room = search_object(dest_room_key)
        if destination_room:
            destination_room = destination_room[0]
        else:
            caller.msg("Ziel nicht gefunden")
            return

        caller.msg(f"Du betrittst {self.target}")
        caller.move_to(destination_room)

class WildernessEnterCmdSet(CmdSet):
    """
    Enthält Befehl für Wilderness rein
    """
    def at_cmdset_creation(self):
        self.add(CmdEnterWilderness())

class WildernessLeaveCmdSet(CmdSet):
    """
    Enthält Befehl für Wilderness raus
    """
    def at_cmdset_creation(self):
        self.add(CmdLeaveWilderness())
