from nessusapi.session import Session

def authenticate():
    Session( prompt("Username"),
             prompt("Password"),
             prompt("Host", "127.0.0.1"),
             prompt("Port", "8834") )

def prompt(text, default=None):
    choice = ""
    while choice == "":
        choice = raw_input("{0}{1}: ".format(text, " (default: {0})".format(default) if default else ""))
        if choice == "" and not default is None:
            return default
    return choice
            
