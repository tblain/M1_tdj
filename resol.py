from pulp import LpProblem, LpMaximize, lpSum, LpVariable, LpStatus, LpAffineExpression
import numpy as np
from itertools import product

# ========================================================================================================

class Conf(object):

    def __init__(self, x, y, t, mp, dic):
        # nb pierre du joueur 1
        self.x = x

        # nb pierre du joueur 2
        self.y = y

        # position du troll : 0 => au milieu, -mp position du chateau du troll
        self.t = t

        # nombre de case depuis le centre jusqu'a la tour
        self.mp = mp

        # dictionnaire qui contient toutes les conf deja cree pour evite de tout recalculer
        self.dic = dic
        dic["" + str(x) + " " + str(y) + " " + str(t)] = self

        self.resolu = False
        self.val = None

        # distribution de proba que devra jouer le joueur 1 avec cette configuration
        self.strat1 = np.empty((x))
        # la partie joueur 2 ne fonctionne pas
        self.strat2 = np.empty((y))

        # tableau contenant les valeurs de toutes les possibilites a partir de la conf
        # sert pour resoudre le simplex
        self.tab = np.empty((x, y), dtype='object')
        self.eval_tab = np.empty((x, y))

    def get_possible_conf(self):
        # on parcourt toutes les quantites de pierres jouables a partie de la conf
        for (i, j) in product(range(1, self.x+1), range(1, self.y+1)):

                # coordonnees de la nouvelles conf
                x = self.x - i
                y = self.y - j

                d = 1 if i > j else -1 if i < j else 0
                t = self.t + d

                # nom dans le dictionnaire
                name = "" + str(x) + " " + str(y) + " " + str(t)

                # on regarde si la conf n'existe pas deja
                conf = self.dic.get(name, -1)

                # sinon on la cree
                if conf == -1:
                    conf = Conf(x, y, t, self.mp, self.dic)

                self.tab[x, y] = conf
                self.eval_tab[x, y] = conf.eval()

    def resolve(self):
        prob = LpProblem("Conf_" + str(self.x) + "_" + str(self.y) + "_" + str(self.t), LpMaximize)

        # variable a maximiser
        val = LpVariable('val', cat='Continuous')

        nb_strat1 = self.x
        nb_strat2 = self.y

        # distribution de prob des strats a calculer
        var1 = [LpVariable('x'+str(i), lowBound=0, cat='Continuous') for i in range(nb_strat1)]

        for j in range(nb_strat2):
            prob += [var1[i] * self.eval_tab[i][j] for i in range(nb_strat1)] >= val

        prob += lpSum(var1) == 1, "Somme des proba"

        # precision dans le probleme qu'on veut maximiser val
        prob += LpAffineExpression(val)

        # print(prob.constraints)
        # print(prob.objective)

        prob.solve()

        # print("Status:", LpStatus[prob.status])

        self.resolu = True

        for i, v in enumerate(prob.variables()):
            if i == 0:
                self.val = v.varValue
            else:
                self.strat1[i-1] = v.varValue

        if (self.x == 5 and self.y == 3 and self.t == -1) or (self.x == 4 and self.y == 3) or (self.x == 5 and self.y == 4):
            pass
            print(nb_strat1, nb_strat2, self.t, " = > ", self.val)
            print(self.eval_tab)


    def eval(self):
        if self.resolu:
            return self.val

        if self.t >= self.mp:
            self.val = 1
        elif self.t <= -self.mp:
            self.val = -1

        elif self.x == 0:

            if self.t - self.y == 0:
                self.val = 0
            elif self.t - self.y > 0:
                self.val = 1
            elif self.t - self.y < 0:
                self.val = -1

        elif self.y == 0:
            if self.x + self.t == 0:
                self.val = 0
            elif self.t + self.x > 0:
                self.val = 1
            elif self.t + self.x < 0:
                self.val = -1

        else:
            self.get_possible_conf()
            self.resolve()

        # print("val: ", self.val)
        self.resolu = True
        return self.val

# ========================================================================================================

if __name__ == "__main__":
    m = 7
    mp = m // 2
    p = 15

    dic = {}

    # conf_base = Conf(5, 4, -1, mp, dic)

    # conf_base = Conf(4, 3, -1, mp, dic)

    # conf_base = Conf(3, 0, -2, mp, dic)

    conf_base = Conf(p, p, 0, mp, dic)
    # dic['' + str(p) + " " + str(p) + " " + str(0)] = conf_base

    val = conf_base.eval()

    print()
    print("Val du jeu: ", val)
    print(conf_base.strat1)
