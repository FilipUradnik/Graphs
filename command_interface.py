import math

class Interface:
    def __init__(self):
        self.commands = [["HELP", self.get_help, ["command_name"], "shows help to other commands"]]

    def get_help(self, command):
        for x in self.commands:
            if x[0] == command:
                print(" ".join([x[0]] + x[2]))

                if len(x) > 3 and not x[3] is None:print(x[3])
                else:print("No help found")
                break

    def add_commands(self, a):
        for x in a:
            command = x[0].split()
            command, params = command[0], command[1:]
            func = x[1]
            help = x[2] if len(x) > 2 else None
            self.commands.append([command, func, params, help])

        self.menu = Menu([[x[0], x[0]] for x in self.commands])


    def command(self, i):
        i = i.strip().split()

        for command in self.commands:
            if command[0] == i[0] and len(i) <= len(command[2]) + 1:
                i = i[1:]
                params = []
                for x in command[2]:
                    param = x.split(":")
                    if len(param) > 1:param, type = param
                    else:param = param[0]; type = "str"
                    
                    if len(i):input_p, i = i[0], i[1:]
                    elif type != "array":input_p = input(param.replace('_', ' ') + ": ").replace(" ", "_")

                    if type == "array":
                        input_p = []
                        while (arr_in:=input(param.replace('_', ' ') + ": ").strip()) != "":
                            input_p.append(arr_in)

                    elif type == "str":pass
                    elif type == "float":input_p = float(input_p)
                    elif type == "int":input_p = int(input_p)
                    elif type == "bool":input_p = get_bool(input_p)

                    params.append(input_p)
                
                return command[1](*params)

    def input_from_menu(self):
        i = self.menu.run_menu()
        if i == "EXIT": return "EXIT"
        self.command(i) 
        print("")
        input("Press ENTER to continue...") 


class Menu:
    def __init__(self, menu_items, name="MENU"):
        self.menu_items = menu_items
        self.name = name
        self.max_len = max(30, len(name))
        for x in self.menu_items:
            self.max_len = max(len(x[0])+1, self.max_len)

    def fancy_print(self, *texts):
        for text in texts:
            for x in text.split("\n"):
                self.max_len = max(self.max_len, len(x)+1)
        print(""); print("-"*self.max_len)
        for text in texts:print(text); print("-"*self.max_len)

    def print_menu(self):
        self.fancy_print(
            self.name,
            "\n".join([(" "*(int(math.log10(len(self.menu_items)))+1-len(str(x+1)))) + f"{x+1}|{self.menu_items[x][0]}" for x in range(len(self.menu_items))] + [f"{len(self.menu_items)+1}|EXIT"])
        )

    def choose(self, i):
        if i.isnumeric():
            i = int(i)
            if int(i) > len(self.menu_items):return "EXIT"
        elif i.lower() == "exit":return "EXIT"

        for x in range(len(self.menu_items)):
            if i == x+1 or (isinstance(i, str) and i.lower() == self.menu_items[x][0].lower()):
                self.fancy_print(self.menu_items[x][0])
                if callable(self.menu_items[x][1]):
                    return self.menu_items[x][1]()
                return self.menu_items[x][1]
        return i

    def run_menu(self):
        self.print_menu()
        return self.choose(input("Choose: "))

    def run_loop(self):
        while True:
            if self.run_menu() == "EXIT":break
            input("Press ENTER to continue...")

def get_bool(i):
    return i.strip().lower() in ["t", "true", "y", "yes"]