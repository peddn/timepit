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
        for attacker, defender in self.db.fights.items():
            if attacker.location != defender.location:
                self.remove_fight(attacker)
                attacker.msg(f"{defender} nicht gefunden. Breche Attacke ab.")
                defender.msg(f"{attacker} hat aufgehört, dich zu attackieren.")
                return
            attacker.msg(f"Du attackierst {defender.key}.")
            defender.msg(f"Du verteidigts dich gegen eine Attacke von {attacker.key}.")
            attacker.location.msg_contents(f"{attacker.key} attackiert {defender.key}.", exclude=[attacker, defender])
            damage = attacker.roll_damage()
            defender.at_damage(damage, attacker)
            attacker.msg(f"Du verursachst {damage} Schaden an {defender}")
            defender.msg(f"{attacker} verusacht {damage} an dir.")
            attacker.location.msg_contents(f"{attacker} verursacht {damage} Schaden an {defender}.", exclude=[attacker, defender])
            if defender.tp < 0:
                defender.at_defeat()
                self.remove_fight(attacker)
