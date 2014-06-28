from nessusapi.session import Session
from getpass import getpass

def authenticate():
    Session(_prompt("Username"),
            _prompt("Password", hidden=True),
            _prompt("Host", "127.0.0.1"),
            _prompt("Port", "8834"))

def _prompt(text, default=None, hidden=False):
    choice = ""
    while choice == "":
        prompt = "{0}{1}: ".format(text, " (default: {0})".format(default) if default else "")
        if hidden:
            choice = getpass(prompt)
        else:
            choice = raw_input(prompt)

        if not choice and default is not None:
            return default
    return choice
            
