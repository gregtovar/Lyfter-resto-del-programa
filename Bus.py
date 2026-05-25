#
# 
# 
#   BUS APPLICATION - 
# 
# 
# 
#   ********** COLORS FUNCTION *********
# 
def colors():
    return {
        "CYAN":   "\033[96m",
        "BLUE":   "\033[94m",
        "GREEN":  "\033[92m",
        "YELLOW": "\033[93m",
        "RED":    "\033[91m",
        "PURPLE": "\033[95m",
        "BOLD":   "\033[1m",
        "DIM":    "\033[2m",
        "RESET":  "\033[0m",
    }
 
 

#
#   ********** PERSON CLASS  *********
#
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age  = age
 
    def __str__(self):
        return f"{self.name} (age {self.age})"
 
 
#
#   ********** BUS CLASS  *********
#
class Bus:
    def __init__(self, max_passengers):
        self.max_passengers = max_passengers
        self.passengers     = []
 
    def add_passenger(self, person, c):
        if len(self.passengers) >= self.max_passengers:
            print(f"\n  {c['RED']}✖  Bus is full! Cannot board {person.name}.{c['RESET']}")
        else:
            self.passengers.append(person)
            count = len(self.passengers)
            print(f"  {c['GREEN']}✔  {person.name} boarded.  "
                  f"{c['DIM']}({count}/{self.max_passengers} seats taken){c['RESET']}")
 
    def remove_passenger(self, name, c):
        for person in self.passengers:
            if person.name.lower() == name.lower():
                self.passengers.remove(person)
                count = len(self.passengers)
                print(f"  {c['YELLOW']}✔  {person.name} got off.  "
                      f"{c['DIM']}({count}/{self.max_passengers} seats taken){c['RESET']}")
                return
        print(f"\n  {c['RED']}✖  No passenger named '{name}' found on the bus.{c['RESET']}")
 
    def show_passengers(self, c):
        bar = "─" * 38
        print(f"\n  {c['BLUE']}{bar}{c['RESET']}")
        print(f"  {c['BOLD']}{c['PURPLE']}  🚌  Passengers on board  "
              f"{c['DIM']}({len(self.passengers)}/{self.max_passengers}){c['RESET']}")
        print(f"  {c['BLUE']}{bar}{c['RESET']}")
        if not self.passengers:
            print(f"  {c['DIM']}  (no passengers){c['RESET']}")
        else:
            for i, p in enumerate(self.passengers, 1):
                print(f"  {c['DIM']}  {i}.{c['RESET']}  {c['CYAN']}{p}{c['RESET']}")
        print(f"  {c['BLUE']}{bar}{c['RESET']}\n")
 
 
#
#   ********** INPUT  *********
#
def ask_person(c):
    print(f"\n  {c['DIM']}  Enter passenger details:{c['RESET']}")
    name = input(f"  {c['YELLOW']}👤  Name   » {c['RESET']}").strip()
    while True:
        try:
            age = int(input(f"  {c['YELLOW']}🎂  Age    » {c['RESET']}"))
            if age <= 0:
                print(f"  {c['RED']}✖  Age must be greater than 0.{c['RESET']}")
                continue
            break
        except ValueError:
            print(f"  {c['RED']}✖  Please enter a valid number.{c['RESET']}")
    return Person(name, age)
 
 
def ask_remove_name(c):
    return input(f"\n  {c['YELLOW']}👤  Passenger to remove » {c['RESET']}").strip()
 
 
def ask_max_passengers(c):
    while True:
        try:
            n = int(input(f"  {c['YELLOW']}🚌  Max passengers » {c['RESET']}"))
            if n <= 0:
                print(f"  {c['RED']}✖  Must be greater than 0.{c['RESET']}")
                continue
            return n
        except ValueError:
            print(f"  {c['RED']}✖  Please enter a valid number.{c['RESET']}")
 
 
def show_menu(c):
    print(f"  {c['BLUE']}{'─' * 38}{c['RESET']}")
    print(f"  {c['BOLD']}  1.{c['RESET']}  Board a passenger")
    print(f"  {c['BOLD']}  2.{c['RESET']}  Remove a passenger")
    print(f"  {c['BOLD']}  3.{c['RESET']}  Show all passengers")
    print(f"  {c['BOLD']}  4.{c['RESET']}  Exit")
    print(f"  {c['BLUE']}{'─' * 38}{c['RESET']}")
    return input(f"\n  {c['CYAN']}  Option » {c['RESET']}").strip()
 
 
#
#   ********** MAIN  *********
#
c = colors()
 
print(f"\n  {c['BOLD']}{c['PURPLE']}✦  Bus Passenger Manager  ✦{c['RESET']}")
print(f"\n  {c['DIM']}  How many seats does the bus have?{c['RESET']}")
 
bus = Bus(ask_max_passengers(c))
 
while True:
    print()
    choice = show_menu(c)
 
    if choice == "1":
        person = ask_person(c)
        bus.add_passenger(person, c)
 
    elif choice == "2":
        name = ask_remove_name(c)
        bus.remove_passenger(name, c)
 
    elif choice == "3":
        bus.show_passengers(c)
 
    elif choice == "4":
        print(f"\n  {c['PURPLE']}  Goodbye! 🚌💨{c['RESET']}\n")
        break
 
    else:
        print(f"\n  {c['RED']}✖  Invalid option. Please choose 1–4.{c['RESET']}")



#
#   ********** END OF MAIN2
#  *********
#