from getpass import getpass

from nessusapi.session import Session

def authenticate():
    print("Connecting to Nessus API")
    host=_prompt("Host", "127.0.0.1")
    port=_prompt("Port", "8834")
    Session(_prompt("Username"),
            _prompt("Password", hidden=True),
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
            
