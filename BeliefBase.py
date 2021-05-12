from convertToCnf import convertToCNF


# Clauses for every belief, the class counts all negations as negatives
class Clause:
    def __init__(self, c):
        self.positves = []
        self.negatives = []
        for i in c:
            if c[i] == "~":
                self.negatives.append(c[i])
            else:
                self.positves.append(c[i])


# Belief class convert to cnf and then creates a clause instance
class Belief:
    def __init__(self, cnf):
        self.clauses = []
        c = Clause(convertToCNF(cnf))
        self.clauses.append(c)


# Belief base class has an array with all beliefs
# includes functions to add, delete and clear the base
class BeliefBase:
    def __init__(self):
        self.beliefs = []

    def add(self, object):
        self.beliefs.append(object)

    def delete(self, object):
        for b in self.beliefs:
            self.beliefs.remove(object)

    def clear(self):
        self.beliefs = []
