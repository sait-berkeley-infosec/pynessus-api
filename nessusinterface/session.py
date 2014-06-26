from nessusapi.session import Session
from getpass import getpass

def authenticate():
    Session( prompt("Username"),
             prompt("Password", hidden=True),
             prompt("Host", "127.0.0.1"),
             prompt("Port", "8834") )

def prompt(text, default=None, hidden=False):
    choice = ""
    while choice == "":
        prompt = "{0}{1}: ".format(text, " (default: {0})".format(default) if default else "")
        if hidden:
            choice = getpass(prompt)
        else:
            choice = raw_input(prompt)

        if choice == "" and default is not None:
            return default
    return choice
            
