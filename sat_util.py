__author__ = 'chakib'
import random
import asyncio
import time
from math import ceil

class sat:
    def __init__(self, clauses=[]):
        self.clauses = clauses.copy()  # l'ensemble des clauses
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
                if s[0] == "%": break
                try:
                    int(s[0])
                    c, maxi2 = self.getclause(s)
                    if maxi2 > maxi: maxi = maxi2
                    l.append(c)
                except ValueError:
                    continue
                except:
                    break
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


def afficher_interpretation(interpretation):
    d = {i + 1: interpretation[i] for i in range(len(interpretation))}
    print("-------------------------------------")
    s = '\n'.join("%r : %s " % (key, val) for (key, val) in d.items())
    print(s)
    print("-------------------------------------")


# def afficher_solution( )
# l.generate_problem(1000, 100)

#print(len(l.clauses))
# print(l.generate_problem(100, 50))
# print(l.maxi)
# print(x)

def benchamrk(input, maxcore=2, maxmaxiter=100, maxmaxflip=50, autocalcul=False):
    with open(input + ".csv", "w") as f:

        l = sat()
        l.parser(input)
        if (autocalcul):
            maxmaxiter = l.maxi
            maxmaxflip = l.maxi * 2 / 3

        f.writelines("nb clauses ;nb variables ; nb de caluses satisfaites;temps ; maxiteration ; maxflip ; nbcores\n")
        for nbcores in range(1, maxcore + 1):
            for maxiter in range(5, maxmaxiter + 1, ceil(maxmaxiter / 5)):
                print(maxiter)
                for maxflip in range(5, maxmaxflip + 1, ceil(maxmaxflip / 5)):
                    debut = time.clock()
                    # x = l.gsatparallel(maxiter,maxflip,nbcores)
                    x = l.gsat(maxiter, maxflip)
                    temp = time.clock() - debut
                    f.writelines(str(len(l.clauses)) + ";" + str(l.maxi) + ";" + str(sum(l.interpreter(x))) + ";" + str(
                        temp) + ";" + str(maxiter) + ";" + str(maxflip) + ";" + str(nbcores) + "\n")


l = sat()
s = l.parser("benchmarks/uuf50-01000.cnf")
debut = time.clock()
x = l.gsatparallel(50, 30,4)
temp = time.clock() - debut
print("-------------------------------------")
print("nb  clauses :", len(l.clauses))
print("nb varialbes :", l.maxi)
print("nb clauses satisfaites: " + str(sum(l.interpreter(x))))
print("temps :", temp, 's')
print("-------------------------------------")
print("Solution optimal")
afficher_interpretation(x)

# print(len(l.clauses),sum(l.interpreter(x)),sep= ";")
# print(l.maxi)
# print()
#
# print(s)
# print(x)
# print(range(x))
# print(s)
#print("---------------------------------")

benchamrk("benchmarks/uf20-02.cnf",1,100,20)
