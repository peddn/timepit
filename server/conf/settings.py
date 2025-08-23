r"""
Evennia settings file.

The available options are found in the default settings file found
here:

https://www.evennia.com/docs/latest/Setup/Settings-Default.html

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "timepit"

<<<<<<< HEAD
# Internationalization
USE_I18N = True
LANGUAGE_CODE = 'de-de'
=======
GAME_SLOGAN = "Deutsches Fantasy MUD"

TIME_ZONE = "Europe/Berlin"

CONNECTION_SCREEN_MODULE = "server.conf.connection_screens"

COMMAND_PARSER = "evennia.commands.cmdparser.cmdparser"

######################################################################
# Default command sets and commands
######################################################################

# Command set used on session before account has logged in
CMDSET_UNLOGGEDIN = "commands.default_cmdsets.UnloggedinCmdSet"
# (Note that changing these three following cmdset paths will only affect NEW
# created characters/objects, not those already in play. So if you want to
# change this and have it apply to every object, it's recommended you do it
# before having created a lot of objects (or simply reset the database after
# the change for simplicity)).
# Command set used on the logged-in session
CMDSET_SESSION = "commands.default_cmdsets.SessionCmdSet"
# Default set for logged in account with characters (fallback)
CMDSET_CHARACTER = "commands.default_cmdsets.CharacterCmdSet"
# Command set for accounts without a character (ooc)
CMDSET_ACCOUNT = "commands.default_cmdsets.AccountCmdSet"

# Location to search for cmdsets if full path not given
CMDSET_PATHS = ["commands", "evennia", "evennia.contrib"]
# Fallbacks for cmdset paths that fail to load. Note that if you change the path for your
# default cmdsets, you will also need to copy CMDSET_FALLBACKS after your change in your
# settings file for it to detect the change.
CMDSET_FALLBACKS = {
    CMDSET_CHARACTER: "evennia.commands.default.cmdset_character.CharacterCmdSet",
    CMDSET_ACCOUNT: "evennia.commands.default.cmdset_account.AccountCmdSet",
    CMDSET_SESSION: "evennia.commands.default.cmdset_session.SessionCmdSet",
    CMDSET_UNLOGGEDIN: "evennia.commands.default.cmdset_unloggedin.UnloggedinCmdSet",
}
# Parent class for all default commands. Changing this class will
# modify all default commands, so do so carefully.
COMMAND_DEFAULT_CLASS = "evennia.commands.default.muxcommand.MuxCommand"
# Command.arg_regex is a regular expression desribing how the arguments
# to the command must be structured for the command to match a given user
# input. By default the command-name should end with a space or / (since the
# default commands uses MuxCommand and /switches). Note that the extra \n
# is necessary for use with batchprocessor.
COMMAND_DEFAULT_ARG_REGEX = r"^[ /]|\n|$"
# By default, Command.msg will only send data to the Session calling
# the Command in the first place. If set, Command.msg will instead return
# data to all Sessions connected to the Account/Character associated with
# calling the Command. This may be more intuitive for users in certain
# multisession modes.
COMMAND_DEFAULT_MSG_ALL_SESSIONS = False
# The default lockstring of a command.
COMMAND_DEFAULT_LOCKS = ""


######################################################################
# Default Account setup and access
######################################################################

# Different Multisession modes allow a player (=account) to connect to the
# game simultaneously with multiple clients (=sessions).
#  0 - single session per account (if reconnecting, disconnect old session)
#  1 - multiple sessions per account, all sessions share output
#  2 - multiple sessions per account, one session allowed per puppet
#  3 - multiple sessions per account, multiple sessions per puppet (share output)
#      session getting the same data.
MULTISESSION_MODE = 0
# Whether we should create a character with the same name as the account when
# a new account is created. Together with AUTO_PUPPET_ON_LOGIN, this mimics
# a legacy MUD, where there is no difference between account and character.
AUTO_CREATE_CHARACTER_WITH_ACCOUNT = True
# Whether an account should auto-puppet the last puppeted puppet when logging in. This
# will only work if the session/puppet combination can be determined (usually
# MULTISESSION_MODE 0 or 1), otherwise, the player will end up OOC. Use
# MULTISESSION_MODE=0, AUTO_CREATE_CHARACTER_WITH_ACCOUNT=True and this value to
# mimic a legacy mud with minimal difference between Account and Character. Disable
# this and AUTO_PUPPET to get a chargen/character select screen on login.
AUTO_PUPPET_ON_LOGIN = True
# How many *different* characters an account can puppet *at the same time*. A value
# above 1 only makes a difference together with MULTISESSION_MODE > 1.
MAX_NR_SIMULTANEOUS_PUPPETS = 1
# The maximum number of characters allowed by be created by the default ooc
# char-creation command. This can be seen as how big of a 'stable' of characters
# an account can have (not how many you can puppet at the same time). Set to
# None for no limit.
MAX_NR_CHARACTERS = 1
# The access hierarchy, in climbing order. A higher permission in the
# hierarchy includes access of all levels below it. Used by the perm()/pperm()
# lock functions, which accepts both plural and singular (Admin & Admins)
PERMISSION_HIERARCHY = [
    "Guest",  # note-only used if GUEST_ENABLED=True
    "Player",
    "Helper",
    "Builder",
    "Admin",
    "Developer",
]
# The default permission given to all new accounts
PERMISSION_ACCOUNT_DEFAULT = "Player"
# Default sizes for client window (in number of characters), if client
# is not supplying this on its own
CLIENT_DEFAULT_WIDTH = 78
# telnet standard height is 24; does anyone use such low-res displays anymore?
CLIENT_DEFAULT_HEIGHT = 45
# Set rate limits per-IP on account creations and login attempts. Set limits
# to None to disable.
CREATION_THROTTLE_LIMIT = 2
CREATION_THROTTLE_TIMEOUT = 10 * 60
LOGIN_THROTTLE_LIMIT = 5
LOGIN_THROTTLE_TIMEOUT = 5 * 60
# Certain characters, like html tags, line breaks and tabs are stripped
# from user input for commands using the `evennia.utils.strip_unsafe_input` helper
# since they can be exploitative. This list defines Account-level permissions
# (and higher) that bypass this stripping. It is used as a fallback if a
# specific list of perms are not given to the helper function.
INPUT_CLEANUP_BYPASS_PERMISSIONS = ["Builder"]

######################################################################
# External Connections
######################################################################

# Note: You do *not* have to make your MUD open to
# the public to use the external connections, they
# operate as long as you have an internet connection,
# just like stand-alone chat clients.

# The Evennia Game Index is a dynamic listing of Evennia games. You can add your game
# to this list also if it is in closed pre-alpha development.
GAME_INDEX_ENABLED = False
# This dict
GAME_INDEX_LISTING = {
    "game_name": "Mygame",  # usually SERVERNAME
    "game_status": "pre-alpha",  # pre-alpha, alpha, beta or launched
    "short_description": "",  # could be GAME_SLOGAN
    "long_description": "",
    "listing_contact": "",  # email
    "telnet_hostname": "",  # mygame.com
    "telnet_port": "",  # 1234
    "game_website": "",  # http://mygame.com
    "web_client_url": "",  # http://mygame.com/webclient
}
# Evennia can connect to external IRC channels and
# echo what is said on the channel to IRC and vice
# versa. Obs - make sure the IRC network allows bots.
# When enabled, command @irc2chan will be available in-game
# IRC requires that you have twisted.words installed.
IRC_ENABLED = False
# RSS allows to connect RSS feeds (from forum updates, blogs etc) to
# an in-game channel. The channel will be updated when the rss feed
# updates. Use @rss2chan in game to connect if this setting is
# active. OBS: RSS support requires the python-feedparser package to
# be installed (through package manager or from the website
# http://code.google.com/p/feedparser/)
RSS_ENABLED = False
RSS_UPDATE_INTERVAL = 60 * 10  # 10 minutes
# Grapevine (grapevine.haus) is a network for listing MUDs as well as allow
# users of said MUDs to communicate with each other on shared channels. To use,
# your game must first be registered by logging in and creating a game entry at
# https://grapevine.haus. Evennia links grapevine channels to in-game channels
# with the @grapevine2chan command, available once this flag is set
# Grapevine requires installing the pyopenssl library (pip install pyopenssl)
GRAPEVINE_ENABLED = False
# Grapevine channels to allow connection to. See https://grapevine.haus/chat
# for the available channels. Only channels in this list can be linked to in-game
# channels later.
GRAPEVINE_CHANNELS = ["gossip", "testing"]
# Grapevine authentication. Register your game at https://grapevine.haus to get
# them. These are secret and should thus be overridden in secret_settings file
GRAPEVINE_CLIENT_ID = ""
GRAPEVINE_CLIENT_SECRET = ""
# Discord (discord.com) is a popular communication service for many, especially
# for game communities. Evennia's channels can be connected to Discord channels
# and relay messages between Evennia and Discord. To use, you will need to create
# your own Discord application and bot.
# Discord also requires installing the pyopenssl library.
# Full step-by-step instructions are available in the official Evennia documentation.
DISCORD_ENABLED = False
# The Intents bitmask required by Discord bots to request particular API permissions.
# By default, this includes the basic guild status and message read/write flags.
DISCORD_BOT_INTENTS = 105985
# The authentication token for the Discord bot. This should be kept secret and
# put in your secret_settings file.
DISCORD_BOT_TOKEN = None
# The account typeclass which the Evennia-side Discord relay bot will use.
DISCORD_BOT_CLASS = "evennia.accounts.bots.DiscordBot"
>>>>>>> 42ed9d6 (settings update)


######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
