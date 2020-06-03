from pulp import LpProblem, LpMaximize, lpSum, LpVariable, LpStatus, LpAffineExpression, allcombinations
from itertools import product

if __name__ == "__main__":
    # tab = [
        # [5, -1, -2, -3],
        # [-1, 5, -1, -2],
        # [-2, -1, 5, -1],
        # [-3, -2, -1, 5]
    # ]

    # tab = [
        # [-1/2, -1, -1, -1],
        # [0, 0, -1, -1],
        # [-1, 0, 0, -1],
        # [-1, -1, 0, 0],
        # [-1, -1, -1, 0]
    # ]

    tab = [
        [0, -1, -1],
        [0, 0, -1],
        [-1, 0, 0],
        [-1, -1, 0],
    ]

    prob = LpProblem("Test1", LpMaximize)

    t = LpVariable('t', cat='Continuous')

    nb_strat1 = len(tab)
    nb_strat2 = len(tab[0])

    print(nb_strat1, nb_strat2)

    var1 = [LpVariable('x'+str(i), lowBound=0, cat='Continuous') for i in range(nb_strat1)]
    # var2 = [LpVariable('y'+str(i), lowBound=0, upBound=1, cat='Continuous') for i in range(4)]

    for j in range(nb_strat2):
        prob += [var1[i] * tab[i][j] for i in range(nb_strat1)] >= t

    prob += lpSum(var1) == 1, "Somme des proba"

    prob += LpAffineExpression(t)

    print()
    print(prob.constraints)

    prob.solve()

    print("Status:", LpStatus[prob.status])

    for v in prob.variables():
        print(v.name, "=", v.varValue)
