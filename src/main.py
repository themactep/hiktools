'''
Sorry, but lisence is a must:
 ________________________________________________________________________________
/                               MIT License                                      \
*                                                                                *
* Copyright (c) 2021 MatrixEditor                                                *
*                                                                                * 
* Permission is hereby granted, free of charge, to any person obtaining a copy   * 
* of this software and associated documentation files (the "Software"), to deal  *
* in the Software without restriction, including without limitation the rights   *
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      *
* copies of the Software, and to permit persons to whom the Software is          *
* furnished to do so, subject to the following conditions:                       *
*                                                                                *
* The above copyright notice and this permission notice shall be included in all *
* copies or substantial portions of the Software.                                *
*                                                                                *
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     *
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       *
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    *
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         *
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  *
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  *
* SOFTWARE.                                                                      *
\________________________________________________________________________________/

#
'''
import sys

from base import core
from injection import pwd, user
from isapi import executor

class MainShell(core.Shell):
    def __init__(self, prompt: str) -> None:
        super().__init__(prompt)

        self.modules = self.create_modules()

    def create_modules(self) -> list:
        return [pwd.UserInjectModule(), user.UserEncounterModule(),
                executor.ExecutorModule()]

    def run(self):
        while 1:
            inp = input(self.get_prompt())

            if inp != None:
                self.react(inp)

    def react(self, input: str):
        if not self.get_module():
            a = input.split(" ")
            if a[0] == "use":
                new_m = self.load(a[1])
                if new_m:
                    self.module = new_m
                    self.module_name = new_m.get_name()
                    print()
                else:
                    print(" Unkown module!\n")
            elif a[0] == "quit":
                quit()
            elif a[0] == "modules":
                self.print_modules()
            else:
                print()
        else:
            if input.split(" ")[0] == "back":
                self.module = None
                self.module_name = None
                print()
            else:
                self.get_module().react(input)
                
    def load(self, name: str) -> core.Module:
        if name != None:
            for m in self.modules:
                if m.get_name() == name:
                    return m
        return None

    def print_modules(self):
        print("\n [*] Printing all loaded modules")

        for module in self.modules:
            if module:
                print(" " + module.get_name())
        print()

print()
#print("\n ──────────────────────startofmain──────────────────────\n\n")

p = "sdk-cam"
if len(sys.argv) >= 2:
    p = str(sys.argv[1])

shell = MainShell(p)
try:
    shell.run()
except KeyboardInterrupt:
    print()
    #print("\n\n ───────────────────────endofmain───────────────────────\n")
    pass
