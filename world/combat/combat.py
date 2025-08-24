from typeclasses.scripts import Script
from random import randint

class CombatManager(Script):
    """
    Ein globaler, persistenter Tick-Kampfmanager.
    Speichert Paare (Angreifer, Ziel). Pro Tick werden ALLE Angriffe gewürfelt.
    Treffer-Schaden wird zunächst gesammelt und ERST AM TICK-ENDE angewendet.
    """
    def at_script_creation(self):
        self.key = "combat_manager"
        self.interval = 2
        self.start_delay = True
        self.persistent = True
        #self.db.fights = []  # [(attacker_obj, target_obj)]
        self.db.fights = {}

    # --- API ---
    def add_fight(self, attacker, defender):
        self.db.fights[attacker] = defender

    def remove_fight(self, attacker):
        self.db.fights.pop(attacker, None)

    # --- Tick ---
    def at_repeat(self, **_):
        if self.db.fights:
            for (attacker, defender) in self.db.fights:
                attacker.msg(f"Du greifts {defender.key} an.")
                defender.msg(f"Du verteidigts dich gegen eine Attacke von {attacker.key}.")
                attacker.location.msg("{attacker.key} greift {defender.key} an.")
