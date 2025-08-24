"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from random import randint
from typing import TYPE_CHECKING
import evennia
from evennia.objects.objects import DefaultCharacter
from evennia.typeclasses.attributes import AttributeProperty

from .objects import ObjectParent


class Character(ObjectParent, DefaultCharacter):
    """
    The Character just re-implements some of the Object's methods and hooks
    to represent a Character entity in-game.

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Object child classes like this.

    """
    pass


class TimepitCharacter:
    # Is this a player character?
    is_pc = True
    
    # The strength attribute - effects damage
    strength = AttributeProperty(5, category="stat")

    # the actual tp of the Character
    tp = AttributeProperty(30, category="stat")


    # the maximum tp of the Character
    tp_max = AttributeProperty(30, category="stat")

    # automatic retaliation when attacked
    auto_retaliate = AttributeProperty(True, category="stat")

    def roll_damage(self):
        return randint(1, 6) + self.strength

    def heal(self, tp):
        """
        Heal tp amount of health, not allowing to exeed the maximum tp
        """
        damage = self.tp_max - self.tp
        healed = min(damage, tp)
        self.tp += healed
        self.msg(f"Du hast dich um {healed} geheilt.")

    def at_attacked(self, attacker, **kwargs):
        """Called when beeing attacked and combat starts."""
        pass

    def at_damage(self, damage, attacker=None):
        self.tp -= damage

    def at_defeat(self):
        """Called when defeated. This means death at the moment."""
        self.at_death()

    def at_death(self):
        """Called when this thing dies."""
        pass


class TimepitNPC(TimepitCharacter):
    is_pc = False
    is_aggro = AttributeProperty(False, category="stat")

class TimepitMob(TimepitNPC):
    is_pc = False
