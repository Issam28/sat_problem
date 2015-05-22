__author__ = 'chakib'
import random


"""
wdghgfxhfgxh dsfgdfgdfg
"""


class sat:
    def __init__(self, clauses):
        self.clauses = clauses.copy()
        self.maxi = -1;
        for i in clauses:
            for j in i:
                if abs(j) > self.maxi: self.maxi = abs(j)

    def interpreter(self, interpretation):
        cpt = 0
        return [self.satisfait(c, interpretation) for c in self.clauses]

    def satisfait(self, c, interpretation):
        var = False
        for i in c:
            if c[i] < 0:
                var = var or not interpretation[abs(c[i])]
            else:
                var = var or interpretation[abs(c[i])]
            if var: return True
        return False

    def generate_solution(self):
        return [bool(random.getrandbits(1)) for _ in range(self.maxi)]


    def gsat(self, maxiteration=100, maxflip=30):
        solution = self.generate_solution()
        initial = self.interpreter(solution)

        for i in range(maxiteration):
            testsolution = self.generate_solution()
            j = 0
            l = self.interpreter(testsolution)

            for j in range(maxflip):
                var = random.randint(self.maxi)
                testsolution[var] = not testsolution[var]
                l1 = self.interpreter(testsolution)
                if sum(l1) > sum(l):
                    l = l1
                else:
                    testsolution[var] = not testsolution[var]

            if sum(l) > sum(initial):
                solution = testsolution
                initial = l


c = [[1, -2], [1, 0]]
s = sat(c)
i = s.interpreter([True, False, True])
print(i)
# print(i)


