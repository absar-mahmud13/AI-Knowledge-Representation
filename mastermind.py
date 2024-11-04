from logic import *

# Define colors and initialize a list to hold the symbols for each color-position pair.
colors = ["red", "blue", "green", "yellow"]
symbols = []

# Generate symbols for each color at each position.
for i in range(4):
    for color in colors:
        symbols.append(Symbol(f"{color}{i}"))

# Initialize the knowledge base as an And object.
knowledge = And()

# Each color must occupy exactly one position.
for color in colors:
    knowledge.add(Or(
        Symbol(f"{color}0"),
        Symbol(f"{color}1"),
        Symbol(f"{color}2"),
        Symbol(f"{color}3")
    ))

# Each color can occupy only one position (no two positions for the same color).
for color in colors:
    for i in range(4):
        for j in range(4):
            if i != j:
                knowledge.add(Implication(
                    Symbol(f"{color}{i}"), Not(Symbol(f"{color}{j}"))
                ))

# Each position can have only one color (no two colors in the same position).
for i in range(4):
    for c1 in colors:
        for c2 in colors:
            if c1 != c2:
                knowledge.add(Implication(
                    Symbol(f"{c1}{i}"), Not(Symbol(f"{c2}{i}"))
                ))

# Define specific constraints about possible arrangements:
# One of these color arrangements is true in the model.
knowledge.add(Or(
    And(Symbol("red0"), Symbol("blue1"), Not(Symbol("green2")), Not(Symbol("yellow3"))),
    And(Symbol("red0"), Symbol("green2"), Not(Symbol("blue1")), Not(Symbol("yellow3"))),
    And(Symbol("red0"), Symbol("yellow3"), Not(Symbol("blue1")), Not(Symbol("green2"))),
    And(Symbol("blue1"), Symbol("green2"), Not(Symbol("red0")), Not(Symbol("yellow3"))),
    And(Symbol("blue1"), Symbol("yellow3"), Not(Symbol("red0")), Not(Symbol("green2"))),
    And(Symbol("green2"), Symbol("yellow3"), Not(Symbol("red0")), Not(Symbol("blue1")))
))

# Additional specific constraints:
knowledge.add(And(
    Not(Symbol("blue0")),
    Not(Symbol("red1")),
    Not(Symbol("green2")),
    Not(Symbol("yellow3"))
))

# Evaluate each symbol to determine if it is entailed by the knowledge base.
for symbol in symbols:
    if model_check(knowledge, symbol):
        print(symbol)  # Print symbols that are entailed by the knowledge base.
