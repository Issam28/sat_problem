__author__ = 'chakib'
import random
import asyncio
import time


class sat:
    def __init__(self, clauses=[]):
        self.clauses = clauses.copy()
        self.maxi = -1
        for i in clauses:
            for j in i:
                if abs(j) > self.maxi: self.maxi = abs(j)

    def interpreter(self, interpretation):
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

    def gsatparallel(self, maxiteration=100, maxflip=30, nbcores=4):
        l = []
        loop = asyncio.get_event_loop()
        x = int(maxiteration / nbcores)
        tasks = [asyncio.async(self.gsat_par(l, x, maxflip)) for _ in range(nbcores)]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        # print(l)
        return max(l, key=lambda x: max(x))

    @asyncio.coroutine
    def gsat_par(self, solutions=[], maxiteration=100, maxflip=30):
        solution = self.generate_solution()
        initial = self.interpreter(solution)
        l = initial
        testsolution = solution
        for i in range(maxiteration):
            # TODO la parallisation de cette boucle
            for j in range(maxflip):
                if l.count(False) == 0: break
                var = self.get_random_var(l)
                testsolution[var] = not testsolution[var]
                l1 = self.interpreter(testsolution)
                if sum(l1) > sum(l):
                    l = l1
                else:
                    testsolution[var] = not testsolution[var]
            if sum(l) > sum(initial):
                solution = testsolution.copy()
                initial = l.copy()

            testsolution = self.generate_solution()
            l = self.interpreter(testsolution)
        solutions.append(solution)
        return solution


    def gsat(self, maxiteration=100, maxflip=30):
        solution = self.generate_solution()
        initial = self.interpreter(solution)
        l = initial
        testsolution = solution
        for i in range(maxiteration):
            # TODO la parallisation de cette boucle
            for j in range(maxflip):
                if l.count(False) == 0: break
                var = self.get_random_var(l)
                testsolution[var] = not testsolution[var]
                l1 = self.interpreter(testsolution)
                if sum(l1) > sum(l):
                    l = l1
                else:
                    testsolution[var] = not testsolution[var]
            if sum(l) > sum(initial):
                solution = testsolution.copy()
                initial = l.copy()

            testsolution = self.generate_solution()
            l = self.interpreter(testsolution)

        return solution

    def get_random_var(self, evaluation):

        c = evaluation.index(False)
        i = abs(random.choice(self.clauses[c])) - 1
        return i


    def generate_problem(self, max_clauses=10, max_vars=10):
        l = []
        self.maxi = max_clauses
        x = list(range(-max_vars, max_vars + 1))
        x.remove(0)

        for i in range(max_clauses):
            l.append([random.choice(x) for _ in range(random.randint(3, max_vars / 2))])
        self.clauses = l
        return l

    def parser(self, nf):
        with open(nf, "r") as f:
            maxi = -1
            l = []
            for s in f.readlines():
                s = s.split()
                try:
                    int(s[0])
                    c, maxi2 = self.getclause(s)
                    if maxi2 > maxi: maxi = maxi2
                    l.append(c)
                except ValueError:
                    continue
            self.clauses = l
            self.maxi = maxi
            return l

    def getclause(self, s):
        maxi = -1
        l = []
        for i in s:
            if int(i) > maxi: maxi = abs(int(i))
            l.append(int(i))
        l.remove(0)
        return l, maxi


l = sat()

l.generate_problem(1000, 100)

#print(len(l.clauses))
# print(l.generate_problem(100, 50))
# print(l.maxi)
# print(x)
s = l.parser("bench.cnf")
debut = time.clock()
x = l.gsatparallel(100, 50, 2)
temp = time.clock() - debut
print(temp)
print(sum(l.interpreter(x)))
print(s)
# print(i)


