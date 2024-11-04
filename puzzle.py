from logic import *

# Define the list of people and houses.
people = ["Gilderoy", "Pomona", "Minerva", "Horace"]
houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

# Initialize a list to store symbols for each person-house pair.
symbols = []

# Create the knowledge base.
knowledge = And()

# Generate symbols for each person-house combination.
for person in people:
    for house in houses:
        symbols.append(Symbol(f"{person}{house}"))

# Each person must belong to one of the houses.
for person in people:
    knowledge.add(Or(
        Symbol(f"{person}Gryffindor"),
        Symbol(f"{person}Hufflepuff"),
        Symbol(f"{person}Ravenclaw"),
        Symbol(f"{person}Slytherin")
    ))

# Ensure each person is assigned to only one house.
for person in people:
    for h1 in houses:
        for h2 in houses:
            if h1 != h2:
                knowledge.add(
                    Implication(Symbol(f"{person}{h1}"), Not(Symbol(f"{person}{h2}")))
                )

# Ensure each house has only one person.
for house in houses:
    for p1 in people:
        for p2 in people:
            if p1 != p2:
                knowledge.add(
                    Implication(Symbol(f"{p1}{house}"), Not(Symbol(f"{p2}{house}")))
                )

# Additional clues:
# Gilderoy belongs to Gryffindor or Ravenclaw.
knowledge.add(
    Or(Symbol("GilderoyGryffindor"), Symbol("GilderoyRavenclaw"))
)

# Pomona is not in Slytherin.
knowledge.add(
    Not(Symbol("PomonaSlytherin"))
)

# Minerva belongs to Gryffindor.
knowledge.add(
    Symbol("MinervaGryffindor")
)

# Check and print the entailed symbols based on the knowledge base.
for symbol in symbols:
    if model_check(knowledge, symbol):
        print(symbol)  # Print symbols that are entailed by the knowledge base.
