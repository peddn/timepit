from evennia import default_cmds

class CmdHomeDE(default_cmds.CmdHome):
    """
    Bewege dich zur dem Ort, den dein Charakter als Zuhause gesetzt hat.

    Usage:
      heim

    Teleportiert dich nach Hause.
    """

    key = "heim"
    aliases = ["home"]

    def func(self):
        """Kopie von CmdHome.func, aber mit deutscher Ausgabe."""
        caller = self.caller
        home = caller.home
        if not home:
            caller.msg("Du hast kein Zuhause!")
        elif home == caller.location:
            caller.msg("Du bist doch bereits Zuhause!")
        else:
            caller.msg("Zuhause ist es am schönsten...")
            caller.move_to(home, move_type="teleport")
