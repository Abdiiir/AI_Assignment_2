from convertToCnf import convertToCNF
from sympy.logic.boolalg import to_cnf


# Clauses for every belief, the class counts all negations as negatives
class Clause:
    def __init__(self, c=""):
        self.positves = []
        self.negatives = []
        while c:
            print(c)
            if c[0] == "(" or c[0] == ")" or c[0] == "|":
                c = c[1:]
                continue
            elif c[0] == "~":
                print("-----------")
                self.negatives.append(c[1])
                c = c[2:]
            else:
                self.positves.append(c[0])
                c = c[1:]

    def __str__(self):
        return (str("positives: ") + str(self.positves) + str("\nnegatives: ") + str(self.negatives) + "\n")

    def __eq__(self, other):
        if len(self.positves) != len(other.positves) or len(self.negatives) != len(other.negatives):
            return False
        # ensure each positive symbol has a match
        for symbol1 in self.positves:
            match = False
            for symbol2 in other.positves:
                if symbol1 == symbol2:
                    match = True
                    break
            if not(match):
                return False
        # ensure each negative symbol has a match
        for symbol1 in self.negatives:
            match = False
            for symbol2 in other.negatives:
                if symbol1 == symbol2:
                    match = True
                    break
            if not(match):
                return False
        return True

    def copy(c):
        result = Clause()
        for symbol in c.positves:
            result.positves.append(symbol)
        for symbol in c.negatives:
            result.negatives.append(symbol)
        return result

    def del_positive_symbol(self, s):
        self.positves.remove(s)

    def del_negative_symbol(self, s):
        self.negatives.remove(s)

    def combine_clauses(c1, c2):
        result = Clause()
        result.positves.extend(c1.positves)
        result.positves.extend(c2.positves)
        result.negatives.extend(c1.negatives)
        result.negatives.extend(c2.negatives)
        return result

    def resolve(c1, c2):
        c1_2 = Clause.copy(c1)
        c2_2 = Clause.copy(c2)
        for s1 in c1_2.positves:
            for s2 in c2_2.negatives:
                if s1 == s2 and s1 in c1_2.positves:
                    c1_2.del_positive_symbol(s1)
                    c2_2.del_negative_symbol(s2)
        for s1 in c1_2.negatives:
            for s2 in c2_2.positves:
                if s1 == s2 and s2 in c2_2.positves:
                    c1_2.del_negative_symbol(s1)
                    c2_2.del_positive_symbol(s2)
        for s1 in c1_2.positves:
            for s2 in c2_2.positves:
                if s1 == s2 and s1 in c1_2.positves:
                    c2_2.del_positive_symbol(s2)
        for s1 in c1_2.negatives:
            for s2 in c2_2.negatives:
                if s1 == s2 and s1 in c1_2.negatives:
                    c2_2.del_negative_symbol(s2)
        result = Clause.combine_clauses(c1_2, c2_2)
        return result


# Belief class convert to cnf
# and then creates a class instance for each clause
class Belief:
    def __init__(self, cnf, negate_belief=True):
        self.clauses = []
        self.cnf3 = cnf
        cnf = convertToCNF(cnf)
        print(cnf)
        if not(negate_belief):
            for i in range(cnf.count("&") + 1):
                if cnf.find("&") != -1:
                    temp_cnf = cnf[:cnf.find("&")]
                else:
                    temp_cnf = cnf
                cnf = cnf[cnf.find("&") + 1:]
                c = Clause(temp_cnf)
                self.clauses.append(c)
        else:
            print("ELSE")
            cnf2 = "~(" + cnf + ")"
            cnf2 = str(to_cnf(cnf2))
            print(cnf2)
            for i in range(cnf2.count("&") + 1):
                print(i)
                print(cnf2.find("&"))
                if cnf2.find("&") != -1:
                    temp_cnf = cnf2[:cnf2.find("&")]
                else:
                    temp_cnf = cnf2
                print(temp_cnf)
                cnf2 = cnf2[cnf2.find("&") + 1:]
                # print("temp", temp_cnf)
                # print("cnf", cnf2)
                c = Clause(temp_cnf)
                # print(c.negatives, c.positves)
                self.clauses.append(c)
        print("done0")

    def __str__(self):
        out = '{'
        for ele in self.clauses:
            out = out + str(ele) + ', '
        return out[:len(out) - 2] + '}'


# Belief base class has an array with all beliefs
# includes functions to add, delete and clear the base
class BeliefBase:
    def __init__(self):
        self.beliefs = []

    def add(self, bel):
        self.beliefs.append(bel)

    def LogicalEntailment(self, belief):
        # create negation of the belief
        print(belief.cnf3)
        negated_belief = Belief(belief.cnf3, True)
        print("done1")
        BaseClauses = []
        resolved_clauses = []
        BaseClauses.extend(negated_belief.clauses)
        for b in self.beliefs:
            BaseClauses.extend(b.clauses)
        add_clause = True
        while add_clause:
            add_clause = False
            for c1 in BaseClauses:
                for c2 in BaseClauses:
                    if c1 != c2 and (c1, c2) not in resolved_clauses:
                        result = Clause.resolve(c1, c2)
                        if len(result.negatives) == 0 and len(result.positves):
                            print("IS TRUE")
                            return True
                        add_clause2 = True
                        for c3 in BaseClauses:
                            if result == c3:
                                add_clause2 = False
                        if add_clause2:
                            add_clause = True
                            BaseClauses.append(result)
                            resolved_clauses.append((c1, c2))
        print("FAKE NEWS")
        return False

    def delete(self, bel):
        for b in self.beliefs:
            self.beliefs.remove(bel)

    def clear(self):
        self.beliefs = []

    def __str__(self):
        out = '{'
        for ele in self.beliefs:
            out = out + str(ele) + ', '
        return out[:len(out) - 2] + '}'


# n1 = Belief("(~a|b)&(~b|a)&((a|~c)&(b|~c))", negate_belief=False)
n1 = Belief("(p)", negate_belief=False)
n2 = Belief("(q)", negate_belief=False)
# n2 = Belief("(a<->b)&(c->(a&b))&a", negate_belief=False)
# n3 = Belief("a&(b->c)&((a|a<->b)|((a->b))<->(c->d))", negate_belief=False)
bb = BeliefBase()
bb.add(n1)
# bb.add(n2)
bb.LogicalEntailment(n2)

print(bb)
