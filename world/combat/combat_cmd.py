import re

from evennia import CmdSet, search_object, search_script
from evennia.contrib.grid import wilderness
from commands.command import Command

class CmdAttackiere(Command):
    """
    Greife etwas an.
    """
    key = "attackiere"
    aliases = ["atta"]
    locks = "cmd:all()"

    def parse(self):
        targets = re.sub(r"\s+", " ", self.args).strip().split()
        self.target = targets[0] if targets else None

    def func(self):
        caller = self.caller
        room = self.obj

        if not self.target:
            caller.msg("Wen oder was willst du attakieren?")
            return

        for item in caller.location.contents:
            caller.msg(item.key)

        target = caller.search(self.target.lower(), candidates=caller.location.contents)

        if not target:
            caller.msg(f"'{self.target}' gibt es hier wohl nicht. Such dir ein anderes Opfer.")
        else:
            caller.msg(f"Du beginnst {target.key} anzugreifen.")
            target.msg(f"{caller.key} beginnt dich anzugreifen.")
            room.msg(f"{caller.key} beginnt {target.key} anzugreifen.")
            combat_script = search_script("combat_script")
            combat_script.add_fight(caller, target)

class CmdAufgeben(Command):
    """
    Verlasse eine Wilderness.
    """
    key = "aufgeben"
    aliases = ["aufg"]
    locks = "cmd:all()"

    def parse(self):
        pass

    def func(self):
        caller = self.caller
        room = self.obj

        caller.msg(f"Du stoppst deine Attacke.")
        room.msg(f"{caller.key} stoppt seine Attacke.")
        combat_script = search_script("combat_script")
        combat_script.remove_fight(caller)

class CombatCmdSet(CmdSet):
    """
    Enthält Befehl für Wilderness rein
    """
    def at_cmdset_creation(self):
        self.add(CmdAttackiere())
        self.add(CmdAufgeben())
