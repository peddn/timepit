from evennia import search_object, create_object

from typeclasses.scripts import Script
from typeclasses.objects import Object

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
    def add_fight(self, attacker, defender, is_retaliation=False):
        self.start()
        self.db.fights[attacker] = defender
        defender.at_attacked(attacker, is_retaliation=is_retaliation)

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

            attacker.msg(f"Du attackierst {defender}.")
            defender.msg(f"{attacker} attackiert dich.")
            attacker.location.msg_contents(f"{attacker} attackiert {defender}.", exclude=[attacker, defender])

            damage = attacker.roll_damage()
            defender.at_damage(damage, attacker)

            attacker.msg(f"Du verursachst {damage} Schaden an {defender}")
            defender.msg(f"{attacker} verusacht {damage} an dir.")
            attacker.location.msg_contents(f"{attacker} verursacht {damage} Schaden an {defender}.", exclude=[attacker, defender])

            if defender.tp < 0:
                attacker.msg(f"Du hast {defender} getötet.")
                attacker.location.msg_contents(f"{attacker} hat {defender} getötet.", exclude=[attacker, defender])
                defender.at_defeat()
                self.remove_fight(attacker)
                if not defender.is_pc:
                    body = create_object(Object, key=f"Die Leiche von {defender}.", location=defender.location)
                    body.desc = "Eine übel zugerichtete Leiche."
                    defender.delete()
