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

        # position du troll : 0 => au milieu, -mp position du chateau du joueur 1
        self.t = t

        # nombre de case depuis le centre jusqu'a la tour
        self.mp = mp

        # dictionnaire qui contient toutes les conf deja cree pour evite de tout recalculer
        self.dic = dic
        dic["" + str(x) + " " + str(y) + " " + str(t)] = self

        self.resolu = False
        self.val = None

        # distribution de proba que devra jouer le joueur 1 avec cette configuration
        self.strat1 = np.zeros((x))
        # la partie joueur 2 ne fonctionne pas
        self.strat2 = np.zeros((y))

        # tableau contenant les valeurs de toutes les possibilites a partir de la conf
        # sert pour resoudre le simplex
        self.eval_tab = np.zeros((x, y))

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

                self.eval_tab[i-1, j-1] = conf.eval()

    def resolve(self):
        prob = LpProblem("Conf_" + str(self.x) + "_" + str(self.y) + "_" + str(self.t), LpMaximize)

        # variable a maximiser
        val = LpVariable('val', cat='Continuous')

        nb_strat1 = self.x
        nb_strat2 = self.y

        # distribution de prob des strats a calculer
        var1 = [LpVariable(''+str(i), lowBound=0, cat='Continuous') for i in range(nb_strat1)]

        for j in range(nb_strat2):
            prob += [var1[i] * self.eval_tab[i][j] for i in range(nb_strat1)] >= val

        prob += lpSum(var1) == 1, "Somme des proba"

        # precision dans le probleme qu'on veut maximiser val
        prob += LpAffineExpression(val)

        prob.solve()

        self.resolu = True

        for i, v in enumerate(prob.variables()):
            if v.name == "val":
                self.val = v.varValue
            else:
                self.strat1[int(v.name)] = v.varValue

    def eval(self):
        if self.resolu:
            return self.val

        # le troll est sur la tour du joueur 2
        if self.t >= self.mp:
            self.val = 1
        # le troll est sur la tour du joueur 1
        elif self.t <= -self.mp:
            self.val = -1

        # le joueur 1 n'a plus de pierre
        elif self.x == 0:

            # on check ou le troll se trouve apres avoir depense les pierres de l'autre joueur
            if self.t - self.y == 0:
                self.val = 0
            elif self.t - self.y > 0:
                self.val = 1
            elif self.t - self.y < 0:
                self.val = -1

        # le joueur 2 n'a plus de pierre
        elif self.y == 0:

            # on check ou le troll se trouve apres avoir depense les pierres de l'autre joueur
            if self.x + self.t == 0:
                self.val = 0
            elif self.t + self.x > 0:
                self.val = 1
            elif self.t + self.x < 0:
                self.val = -1

        else:
            # ce n'est pas un cas simple : il faut donc evaluer la config avec un simplex
            self.get_possible_conf()
            self.resolve()

        self.resolu = True
        return self.val

# ========================================================================================================

if __name__ == "__main__":
    m = 7
    mp = m // 2
    p = 15

    dic = {}

    conf_base = Conf(p, p, 0, mp, dic)

    val = conf_base.eval()

    print()
    print("Val du jeu: ", val)
    print(conf_base.strat1)
