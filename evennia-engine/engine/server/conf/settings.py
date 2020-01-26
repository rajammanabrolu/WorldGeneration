r"""
Evennia settings file.

The available options are found in the default settings file found
here:

c:\users\will\source\repos\mud\evennia\evennia\settings_default.py

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

# some name
SERVERNAME = "GT EILAB"
WEBSERVER_PORTS = [(80, 4005)]
# enable guest accounts
GUEST_ENABLED = True
DEBUG = False
IN_GAME_ERRORS = False

# this pw validator just filters for standard characters
# we don't need / care about any others
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'evennia.server.validators.EvenniaPasswordValidator'}]

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
