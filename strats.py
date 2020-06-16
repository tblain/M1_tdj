import numpy as np
from conf import Conf


class Strategie:

    def __init__(self, nb_stones1=15, nb_stones2=15, nb_cases=7, history=None, player=1):
        self.nb_stones = max(nb_stones1, nb_stones2)
        self.nb_cases = nb_cases
        self.history = history
        self.player = player

        if player == 0:
            self.adversary = 1
        else:
            self.adversary = 0


class Strategie_naive_always_1(Strategie):
    """
    always play 1 stone
    """

    def __init__(self, nb_stones, nb_cases, history, player):
        super().__init__(nb_stones, nb_cases, history, player)

    def launch_stones(self, nb_step):
        return 1


class Strategie_naive_always_2(Strategie):
    """
    always play 2 stones
    """

    def __init__(self, nb_stones, nb_cases, history, player):
        super().__init__(nb_stones, nb_cases, history, player)

    def launch_stones(self, nb_step):
        return min(2, self.nb_stones)


class Strategie_naive_plus_one(Strategie):
    """
    play one stone more than the previous amount from the other player
    """

    def __init__(self, nb_stones, nb_cases, history, player):
        super().__init__(nb_stones, nb_cases, history, player)

    def launch_stones(self, nb_step):
        if nb_step == 0:
            return 2
        else:
            return min(self.history[nb_step-1, self.adversary] + 1, self.nb_stones)


class Strategie_naive_defensive(Strategie):
    """
    play 1 stone more that adversary previous amount if the troll is in its territory
    else play 2 stones
    """

    def __init__(self, nb_stones1, nb_stones2, nb_cases, history, player):
        super().__init__(nb_stones1, nb_stones2, nb_cases, history, player)
        self.middle_case = nb_cases // 2

    def launch_stones(self, nb_step):
        if nb_step == 0:
            return 2
        else:
            if (self.player == 1 and self.history[nb_step, 2] >= 0) or (self.player == 2 and self.history[nb_step, 2] <= 0):
                return max(min(self.history[nb_step-1, self.adversary] + 1, self.nb_stones), 1)
            else:
                return min(2, self.nb_stones)


class Strategie_prudente(Strategie):
    """
    Joue en suivant la strategie prudente calculee avec les theories des jeux
    """

    def __init__(self, nb_stones1, nb_stones2, nb_cases, history, player):
        super().__init__(nb_stones1, nb_stones2, nb_cases, history, player)
        self.dic = {}
        self.conf = Conf(nb_stones1, nb_stones2, history[0][2], nb_cases // 2, self.dic)
        self.conf.eval()
        print()
        print("gain: ", self.conf.eval())
        print()
        self.nb_p1 = nb_stones1
        self.nb_p2 = nb_stones2

    def launch_stones(self, nb_step):
        # on met a jour la conf par rapport au choix de l'autre et du notre
        if nb_step > 0:
            self.nb_p1 -= self.history[nb_step-1, 0]
            self.nb_p2 -= self.history[nb_step-1, 1]
            t = self.history[nb_step, 2]

            self.conf = self.dic.get("" + str(self.nb_p1) + " " + str(self.nb_p2) + " " + str(t), -1)
            assert not self.conf == -1

        print("Distribution de strategie: ", self.conf.strat1)
        p = np.random.choice(self.nb_p1, 1, p=self.conf.strat1[::1])

        return p[0] + 1
