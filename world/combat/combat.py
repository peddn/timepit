from typeclasses.scripts import Script

class CombatScript(Script):

    def at_script_creation(self):
        self.key = "combat_script"
        self.desc = "A combat script"
        self.interval = 1
        self.persistent = False

    def at_repeat(self, **_):
        self.obj.msg('Ick hau dir!')
