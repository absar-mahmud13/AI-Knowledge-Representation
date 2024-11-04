import termcolor 
from logic import *

mustard = Symbol("ColMustard")
plum = Symbol("ProfPlum")
scarlet = Symbol("MsScarlet")
characters = [mustard, plum, scarlet]

ballroom = Symbol("ballroom")
kitchen = Symbol("kitchen")
library = Symbol("library")
rooms = [ballroom, kitchen, library]

knife = Symbol("knife")
revolver = Symbol("revolver")
wrench = Symbol("wrench")
weapons = [knife, revolver, wrench]

symbols = characters + rooms + weapons

def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(And(*knowledge), symbol):
            termcolor.cprint(f"{symbol}: YES", "green")
        elif not model_check(And(*knowledge), Not(symbol)):
            print(f"{symbol}: MAYBE")

# There must be a person, room, and weapon.
knowledge = [
    Or(mustard, plum, scarlet),
    Or(ballroom, kitchen, library),
    Or(knife, revolver, wrench)
]

# Initial cards
knowledge.append(And(
    Not(mustard), Not(kitchen), Not(revolver)
))

# Unknown card
knowledge.append(Or(
    Not(scarlet), Not(library), Not(wrench)
))

# Known cards
knowledge.append(Not(plum))
knowledge.append(Not(ballroom))

check_knowledge(knowledge)
