from convertToCnf import convertToCNF
from sympy.logic.boolalg import to_cnf
from copy import deepcopy as deepcopy
from queue import Queue


class IQueue(Queue):
    
    def to_list(self):
        """
         Queue to list.
        """
        with self.mutex:
            return list(self.queue)

    def __contains__(self, item):
        """
        Allows for in operations on queue.
        """
        with self.mutex:
            return item in self.queue
        
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
        if len(self.positves) != len(other.positves) or len(self.negatives) != len(other.negatives) or set(self.positves) != set(other.positves) and set(self.negatives) != set(other.negatives):
            return False
        return True

    def clause_copy(c):
        result = Clause()
        result.positves.extend(c.positves)
        result.negatives.extend(c.negatives)
        return result

    def delete_pos(self, s):
        self.positves.remove(s)

    def delete_neg(self, s):
        self.negatives.remove(s)

    def combine_clauses(c1, c2):
        CombinedClause = Clause()
        CombinedClause.positves.extend(c1.positves+c2.positves)
        CombinedClause.negatives.extend(c1.negatives+c2.negatives)
        return CombinedClause

    def resolve(c1, c2):
        #Copy to not alter the original clause
        c1_2 = Clause.clause_copy(c1)
        c2_2 = Clause.clause_copy(c2)
        for s1 in c1_2.positves:
            if s1 in c2_2.negatives:
                c1_2.delete_pos(s1)
                c2_2.delete_neg(s1)
        for s1 in c1_2.negatives:
            if s1 in c2_2.positves:
                c1_2.delete_neg(s1)
                c2_2.delete_pos(s1)
        for s1 in c1_2.positves:
            if s1 in c2_2.positves:
                c2_2.delete_pos(s1)
        for s1 in c1_2.negatives:
            if s1 in c2_2.negatives:
                c2_2.delete_neg(s1)
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
        for belief in self.beliefs:
            same_belief = True
        for c1,c2 in zip(belief.clauses,bel.clauses):
            if c1 != c2:
                same_belief = False
        if same_belief:
            self.beliefs.remove(belief)
        
        # HUH???? 
        #for b in self.beliefs:
        #    self.beliefs.remove(bel)

    def clear(self):
        self.beliefs = []

    def __str__(self):
        out = '{'
        for ele in self.beliefs:
            out = out + str(ele) + ', '
        return out[:len(out) - 2] + '}'


    def contract(self, b, mode):
        remainders = self.remainders(b)
        if mode == 'full-meet':
            self.beliefs = BeliefBase.fullMeet(remainders).beliefs
        elif mode == 'maxichoice':
            self.beliefs = remainders[0].beliefs

    def remainders(self, b):
        frontier = IQueue()
        expanded = IQueue()
        frontier.put(self)
        remainders = []
        max = 0
        while True:
        
            if frontier.empty():
      #          print("remainders")
      #          print(remainders)
                return remainders
            n = frontier.get()
            expanded.put(n)
            if not n.LogicalEntailment(b) and n not in remainders:
                if max > 0:
                    if len(n.beliefs) == max:
                        remainders.append(n)
                else:
                    max = len(n.beliefs)
                    remainders.append(n)
            for belief in n.beliefs:
                n_copy = deepcopy(n)
                n_copy.delete(belief)
                if n_copy not in frontier and n_copy not in expanded and max == 0:
                    frontier.put(n_copy)
                    
    def fullMeet(beliefBases):
        b_2 = BeliefBase()
        if len(beliefBases) > 0:
            if len(beliefBases) == 1:
                return beliefBases[0]
            start_b = beliefBases[0]
            for bb in beliefBases[1:]:
                for belief1 in start_b.beliefs:
                    for belief2 in bb.beliefs:
                        if belief1 == belief2:
                            b_2.add_belief(belief1)    
        return b_2



# n1 = Belief("(~a|b)&(~b|a)&((a|~c)&(b|~c))", negate_belief=False)
n1 = Belief("(p -> q)", negate_belief=False)
n2 = Belief("(p -> w)", negate_belief=False)
n3 = Belief("(w -> q)", negate_belief=False)
# n2 = Belief("(a<->b)&(c->(a&b))&a", negate_belief=False)
# n3 = Belief("a&(b->c)&((a|a<->b)|((a->b))<->(c->d))", negate_belief=False)
bb = BeliefBase()
bb.add(n1)
bb.add(n2)
# bb.add(n2)
#bb.LogicalEntailment(n2)
#bb.remainders(n2)
bb.contract(n3,mode="maxichoice")
print("bb")
print(bb)
