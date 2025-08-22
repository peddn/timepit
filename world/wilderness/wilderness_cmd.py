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

    dest_wilderness = "center"

    def parse(self):
        "Very trivial parser - takes only first word of input and ignores the rest"
        targets = re.sub(r"\s+", " ", self.args).strip().split()
        if len(targets) > 0:
            self.target = targets[0].lower()
        else:
            self.target = None


    def func(self):
        caller = self.caller

        if not self.target:
            caller.msg("Was willst du betreten?")
        elif not self.target == self.dest_wilderness:
            caller.msg(f"'{self.target}' kannst du nicht betreten.")
        else:
            caller.msg(f"Du betrittst {self.target}")
            wilderness.enter_wilderness(caller, (10, 5))
            caller.execute_cmd("look")

class CmdLeaveWilderness(Command):
    """
    Verlasse eine Wilderness.
    """
    key = "betrete"
    aliases = ["betr"]
    locks = "cmd:all()"

    dest_room = "void"

    def parse(self):
        ""
        targets = re.sub(r"\s+", " ", self.args).strip().split()
        if len(targets) > 0:
            self.target = targets[0].lower()
        else:
            self.target = None

    def func(self):
        caller = self.caller

        if not self.target:
            caller.msg("Was willst du betreten?")
        elif not self.target == self.dest_room:
            caller.msg(f"'{self.target}' kannst du nicht betreten.")
        else:
            destination_room = search_object("void")
            if len(destination_room) >= 1:
                destination_room = destination_room[0]
            else:
                caller.msg("Ziel nicht gefunden")
                return
            caller.msg(f"Du betrittst {self.target}")
            #caller.cmdset.remove("world.wilderness.wilderness_cmd.WildernessLeaveCmdSet")
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
