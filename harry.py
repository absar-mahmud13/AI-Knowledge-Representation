from logic import Symbol, And, Or, Not, Implication, model_check

# Define symbols
rain = Symbol("rain")
hagrid = Symbol("hagrid")
dumbledore = Symbol("dumbledore")

# Knowledge base
knowledge = And(
    Implication(Not(rain), hagrid),
    Or(hagrid, dumbledore),
    Not(And(hagrid, dumbledore)),
    dumbledore
)

# Check if it must be raining
print(model_check(knowledge, rain))  # Expected output: True
