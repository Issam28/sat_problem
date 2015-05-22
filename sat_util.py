__author__ = 'chakib'
import random



class sat:
    def __init__(self, clauses=[]):
        self.clauses = clauses.copy()
        self.maxi = -1
        for i in clauses:
            for j in i:
                if abs(j) > self.maxi: self.maxi = abs(j)

    def interpreter(self, interpretation):
        cpt = 0
        return [self.satisfait(c, interpretation) for c in self.clauses]

    def satisfait(self, c, interpretation):
        var = False
        for i in c:
            if i < 0:
                var = var or not interpretation[abs(i) - 1]
            else:
                var = var or interpretation[abs(i) - 1]
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
                var = random.randint(0, self.maxi - 1)
                testsolution[var] = not testsolution[var]
                l1 = self.interpreter(testsolution)
                if sum(l1) > sum(l):
                    l = l1
                else:
                    testsolution[var] = not testsolution[var]

            if sum(l) > sum(initial):
                solution = testsolution
                initial = l
        return solution

    def generate_problem(self, max_clauses=10, max_vars=10):
        l = []
        self.maxi = max_clauses
        x = list(range(-max_vars, max_vars + 1))
        x.remove(0)

        for i in range(max_clauses):
            l.append([random.choice(x) for _ in range(random.randint(3, max_vars / 2))])
        self.clauses = l
        return l


l = sat()
print(l.generate_problem(100, 50))
print(l.maxi)
x = l.gsat(400, 20)
print(x)
print(x.count(True))
# print(i)


