from convertToCnf import convertToCNF


# Clauses for every belief, the class counts all negations as negatives
class Clause:
    def __init__(self, c):
        self.positves = []
        self.negatives = []
        while c:
            print(c[0])
            if c[0] == "(" or c[0] == ")" or c[0] == "|":
                c = c[1:]
                continue
            elif c[0] == "~":
                print("!")
                self.negatives.append(c[1])
                c = c[2:]
            else:
                self.positves.append(c[0])
                c = c[1:]

    def __str__(self):
        return(str("positives: ")+str(self.positves)+str("\nnegatives: ")+str(self.negatives)+"\n")


# Belief class convert to cnf
# and then creates a class instance for each clause
class Belief:
    def __init__(self, cnf):
        self.clauses = []
        cnf = convertToCNF(cnf)
        print(cnf)
        for i in range(cnf.count("&")+1):
            print(1)
            temp_cnf = cnf[:cnf.find("&")]
            cnf = cnf[cnf.find("&")+1:]
            print("temp", temp_cnf)
            print("cnf", cnf)
            c = Clause(temp_cnf)
            self.clauses.append(c)

    def __str__(self):
        out = '{'
        for ele in self.clauses:
            out = out + str(ele) + ', '
        return out[:len(out)-2] + '}'


# Belief base class has an array with all beliefs
# includes functions to add, delete and clear the base
class BeliefBase:
    def __init__(self):
        self.beliefs = []

    def add(self, bel):
        self.beliefs.append(bel)

    def delete(self, bel):
        for b in self.beliefs:
            self.beliefs.remove(bel)

    def clear(self):
        self.beliefs = []

    def __str__(self):
        out = '{'
        for ele in self.beliefs:
            out = out + str(ele) + ', '
        return out[:len(out)-2] + '}'


# n1 = Belief("(~a|b)&(~b|a)&((a|~c)&(b|~c))")
n2 = Belief("(a<->b)&(c->(a&b))")
# n3 = Belief("a&(b->c)&((a|a<->b)|((a->b))<->(c->d))")
bb = BeliefBase()
# bb.add(n1)
bb.add(n2)
# bb.add(n3)
print(bb)
