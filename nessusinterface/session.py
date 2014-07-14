from getpass import getpass
import os

from nessusapi.session import Session

def authenticate():
    print("Connecting to Nessus API")
    host=os.getenv('NESSUS_HOST') or _prompt("Host", "127.0.0.1")
    port=os.getenv('NESSUS_PORT') or _prompt("Port", "8834")
    Session(os.getenv('NESSUS_USER') or _prompt("Username"),
            os.getenv('NESSUS_PASS') or _prompt("Password", hidden=True),
            host,
            port)

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
            
