import itertools

class Sentence():
    """
    Abstract base class for logical sentences.
    """

    def evaluate(self, model):
        """Evaluates the logical sentence given a model (dictionary of truth assignments)."""
        raise Exception("nothing to evaluate")

    def formula(self):
        """Returns string formula representing logical sentence."""
        return ""

    def symbols(self):
        """Returns a set of all symbols in the logical sentence."""
        return set()

    @classmethod
    def validate(cls, sentence):
        """Ensures the argument is a Sentence instance, raises error if not."""
        if not isinstance(sentence, Sentence):
            raise TypeError("must be a logical sentence")

    @classmethod
    def parenthesize(cls, s):
        """
        Adds parentheses around the string `s` if needed.
        Only adds parentheses if the string is not already balanced.
        """
        def balanced(s):
            """Checks if a string has balanced parentheses."""
            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False
                    count -= 1
            return count == 0

        if not len(s) or s.isalpha() or (
            s[0] == "(" and s[-1] == ")" and balanced(s[1:-1])
        ):
            return s
        else:
            return f"({s})"


class Symbol(Sentence):
    """A class representing a propositional symbol, like 'rain' or 'sun'."""

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(("symbol", self.name))

    def __repr__(self):
        return self.name

    def evaluate(self, model):
        """Returns the truth value of the symbol based on the model."""
        try:
            return bool(model[self.name])
        except KeyError:
            raise Exception(f"variable {self.name} not in model")

    def formula(self):
        """Returns the name of the symbol as its formula."""
        return self.name

    def symbols(self):
        """Returns a set containing just the symbol's name."""
        return {self.name}


class Not(Sentence):
    """A class representing logical negation of a sentence."""

    def __init__(self, operand):
        Sentence.validate(operand)
        self.operand = operand

    def __eq__(self, other):
        return isinstance(other, Not) and self.operand == other.operand

    def __hash__(self):
        return hash(("not", hash(self.operand)))

    def __repr__(self):
        return f"Not({self.operand})"

    def evaluate(self, model):
        """Returns the negation of the operand's evaluation in the model."""
        return not self.operand.evaluate(model)

    def formula(self):
        """Returns the formula for the negated sentence."""
        return "¬" + Sentence.parenthesize(self.operand.formula())

    def symbols(self):
        """Returns the set of symbols in the negated sentence."""
        return self.operand.symbols()


class And(Sentence):
    """A class representing logical conjunction (AND) of multiple sentences."""

    def __init__(self, *conjuncts):
        for conjunct in conjuncts:
            Sentence.validate(conjunct)
        self.conjuncts = list(conjuncts)

    def __eq__(self, other):
        return isinstance(other, And) and self.conjuncts == other.conjuncts

    def __hash__(self):
        return hash(("and", tuple(hash(conjunct) for conjunct in self.conjuncts)))

    def __repr__(self):
        conjunctions = ", ".join([str(conjunct) for conjunct in self.conjuncts])
        return f"And({conjunctions})"

    def add(self, conjunct):
        """Adds a new conjunct to the conjunction."""
        Sentence.validate(conjunct)
        self.conjuncts.append(conjunct)

    def evaluate(self, model):
        """Returns True if all conjuncts are true in the model."""
        return all(conjunct.evaluate(model) for conjunct in self.conjuncts)

    def formula(self):
        """Returns the formula for the conjunction."""
        if len(self.conjuncts) == 1:
            return self.conjuncts[0].formula()
        return " ∧ ".join([Sentence.parenthesize(conjunct.formula()) for conjunct in self.conjuncts])

    def symbols(self):
        """Returns the set of symbols in the conjunction."""
        return set.union(*[conjunct.symbols() for conjunct in self.conjuncts])


class Or(Sentence):
    """A class representing logical disjunction (OR) of multiple sentences."""

    def __init__(self, *disjuncts):
        for disjunct in disjuncts:
            Sentence.validate(disjunct)
        self.disjuncts = list(disjuncts)

    def __eq__(self, other):
        return isinstance(other, Or) and self.disjuncts == other.disjuncts

    def __hash__(self):
        return hash(("or", tuple(hash(disjunct) for disjunct in self.disjuncts)))

    def __repr__(self):
        disjuncts = ", ".join([str(disjunct) for disjunct in self.disjuncts])
        return f"Or({disjuncts})"

    def evaluate(self, model):
        """Returns True if at least one disjunct is true in the model."""
        return any(disjunct.evaluate(model) for disjunct in self.disjuncts)

    def formula(self):
        """Returns the formula for the disjunction."""
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].formula()
        return " ∨ ".join([Sentence.parenthesize(disjunct.formula()) for disjunct in self.disjuncts])

    def symbols(self):
        """Returns the set of symbols in the disjunction."""
        return set.union(*[disjunct.symbols() for disjunct in self.disjuncts])


class Implication(Sentence):
    """A class representing logical implication (IF-THEN) between two sentences."""

    def __init__(self, antecedent, consequent):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent

    def __eq__(self, other):
        return isinstance(other, Implication) and self.antecedent == other.antecedent and self.consequent == other.consequent

    def __hash__(self):
        return hash(("implies", hash(self.antecedent), hash(self.consequent)))

    def __repr__(self):
        return f"Implication({self.antecedent}, {self.consequent})"

    def evaluate(self, model):
        """Returns True if the implication is true in the model."""
        return (not self.antecedent.evaluate(model)) or self.consequent.evaluate(model)

    def formula(self):
        """Returns the formula for the implication."""
        antecedent = Sentence.parenthesize(self.antecedent.formula())
        consequent = Sentence.parenthesize(self.consequent.formula())
        return f"{antecedent} => {consequent}"

    def symbols(self):
        """Returns the set of symbols in the implication."""
        return set.union(self.antecedent.symbols(), self.consequent.symbols())


class Biconditional(Sentence):
    """A class representing logical biconditional (IF AND ONLY IF) between two sentences."""

    def __init__(self, left, right):
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right

    def __eq__(self, other):
        return isinstance(other, Biconditional) and self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash(("biconditional", hash(self.left), hash(self.right)))

    def __repr__(self):
        return f"Biconditional({self.left}, {self.right})"

    def evaluate(self, model):
        """Returns True if both sides are either true or both false in the model."""
        return (self.left.evaluate(model) and self.right.evaluate(model)) or (not self.left.evaluate(model) and not self.right.evaluate(model))

    def formula(self):
        """Returns the formula for the biconditional."""
        left = Sentence.parenthesize(str(self.left))
        right = Sentence.parenthesize(str(self.right))
        return f"{left} <=> {right}"

    def symbols(self):
        """Returns the set of symbols in the biconditional."""
        return set.union(self.left.symbols(), self.right.symbols())


def model_check(knowledge, query):
    """
    Checks if the knowledge base entails the query.
    """

    def check_all(knowledge, query, symbols, model):
        """
        Recursively checks if knowledge entails query for all symbol assignments.
        """

        # If model has an assignment for each symbol
        if not symbols:
            # If knowledge is true in model, query must also be true
            if knowledge.evaluate(model):
                return query.evaluate(model)
            return True
        else:
            # Choose a symbol and generate models where it's true and false
            remaining = symbols.copy()
