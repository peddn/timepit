from evennia import search_object

from typeclasses.scripts import Script

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
        self.start()
        self.db.fights[attacker] = defender

    def remove_fight(self, attacker):
        self.db.fights.pop(attacker, None)
        # TODO: bei null Kämpfen, das script stoppen

    # --- Tick ---
    def at_repeat(self, **_):
        elendil = search_object("Elendil")
        elendil[0].msg("TICK from combat_manager")
        for (attacker, defender) in self.db.fights:
            attacker.msg(f"Du greifts {defender.key} an.")
            defender.msg(f"Du verteidigts dich gegen eine Attacke von {attacker.key}.")
            attacker.location.msg("{attacker.key} greift {defender.key} an.")
