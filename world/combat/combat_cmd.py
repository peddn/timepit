import re

from evennia import CmdSet, search_object, GLOBAL_SCRIPTS
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
            room.msg_contents(f"{caller.key} beginnt {target.key} anzugreifen.", exclude=[caller, target])
            combat_manager = GLOBAL_SCRIPTS.combat_manager
            combat_manager.add_fight(caller, target)

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

        combat_manager = GLOBAL_SCRIPTS.combat_manager
        target = combat_manager.db.fights[caller]

        caller.msg(f"Du hörst auf, {target.key} zu attackieren.")
        target.msg(f"{caller.key} hört auf, dich zu attackieren.")
        room.msg_contents(f"{caller.key} hört auf {target.key} zu attackieren.", exclude=[caller, target])
        combat_manager.remove_fight(caller)

class CombatCmdSet(CmdSet):
    """
    Enthält Befehl für Wilderness rein
    """
    def at_cmdset_creation(self):
        self.add(CmdAttackiere())
        self.add(CmdAufgeben())
