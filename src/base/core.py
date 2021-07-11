import sys
import requests
import xml.etree.cElementTree as etree
import html.parser

from requests import Response
from xml.etree.ElementTree import Element

htmlparser = html.parser.HTMLParser()

class Runnable(object):

    def __init__(self) -> None:
        super().__init__()

    def run(self):
        pass

class Module(Runnable):

    def __init__(self, name: str) -> None:
        super().__init__()

        self._name = name
        self.options = []

    def show_options(self):
        pass

    def show_help(self):
        print(" Please read documentation for help")

    def react(self, input: str):
        pass

    def get_name(self):
        return self._name

    def set_name(self, name: str):
        self._name = name

    def get_option(self, index: int):
        return self.options[index]

    def set_option(self, index: int, val):
        self.options[index] = val

class Shell(Runnable):

    def __init__(self, prompt: str) -> None:
        super().__init__()

        self.PROMPT = prompt
        self.module_name = None
        self.module = None

    def react(self, input: str):
        pass

    def get_prompt(self):
        if self.module_name == None:
            return f" ┌─(root@{self.PROMPT})─[~]\n └───$ " # fancy styled prompt 
        else:
            return f" ┌─(root@{self.PROMPT}#{self.module_name})─[~]\n └───$ "

    def back(self):
        if self.module_name != None:
            self.module_name = None

    def get_module(self) -> Module:
        return self.module

class BaseModule(Module):
    def __init__(self, name: str, amount: int) -> None:
        super().__init__(name)

        for i in range(amount):
            self.options.append(" ")

    def react(self, input: str):
        a = input.split(" ")
        if a[0] == "set":
            self._set_(a)
        elif a[0] == "run" or a[0] == "exploit":
            self.run()
        elif a[0] == "show":
            if a[1] == "options":
                self.show_options()
        elif a[0] == "-h":
            self.show_help()  

    def _set_(self, a: str):
        pass

    def print_table(self, length_option: int, length_req: int, length_value: int, values: list):
        def formatted(name: str, req: str, val: str) -> str: 
            return f" │ {name}" + " "*(length_option - len(name)) + f"  │ {req}" + " "*(length_req - len(req)) + f"  │ {val}" + " "*(length_value - len(val)) + "  │"

        print(f"\n Showing options for {self.get_name()}:\n")
        print(" ┌─" + "─"*(length_option + 2) + "┬─" + "─"*(length_req + 2) + "┬─" + "─"*(length_value + 2) + "┐")
        print(formatted(values[0][0], values[0][1], values[0][2]))
        print(" ├─" + "─"*(length_option + 2) + "┼─" + "─"*(length_req + 2) + "┼─" + "─"*(length_value + 2) + "┤")
        for i, v in enumerate(values): # I don't know why
            if i != 0:
                print(formatted(values[i][0], values[i][1], values[i][2]))

        print(" └─" + "─"*(length_option + 2) + "┴─" + "─"*(length_req + 2) + "┴─" + "─"*(length_value + 2) + "┘")
        print("\n")

    def len_of(self, names: list) -> int:
            i = 0
            for name in names:
                name += "  "
                if (len(name) > i):
                    i = len(name)
            return i + 2

def parse(f: str) -> Element:
    try:
        return etree.fromstring(f)
    except:
        pass
        #debug("[!] Error while parsing...")

def check_ip_back(ip: str) -> bool:
    for i in ip.split(sep="."):
        if (int(i) >= 1 and int(i) <= 255):
            debug("\t" + i + " -> okay")
        else:
            print("[!] Unexpected input at '", i, "' in address")
            return False
    return True

def fetch_url(url: str) -> Response:
    try:
        return requests.get(url)
    except:
        debug("[!] Error: Fetching incomplete.")
        return None

def debug(msg: str) -> None:
    '''
    Prints the current Message as a debug-Message. This method is oly activated when the debug mode
    is enabled (do that with run or exploit -d)
    '''
    print(msg)

def quit() -> None:
    print("Quitting...")
    sys.exit(0)

def error(msg: str):
    print(f" [!] {msg}")

def log(msg: str):
    print(f" [*] {msg}")

def nonNull(c) -> bool:
        return c != None and c != ""
