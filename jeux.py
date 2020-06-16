import numpy as np


class Jeu(object):

    """Docstring for Jeu. """

    def __init__(self, player1=None, player2=None, nb_cases=7, nb_stones=15, troll_case=0):
        # TODO: refaire la doc
        """
        @param: strat1: strategie du joueur 1
        @param: strat2: strategie du joueur 2
        """

        self.nb_case = nb_cases
        self.mp = nb_cases // 2
        self.nb_stones = nb_stones


        # numero de la case ou se situe le troll, va de 0 a 6 (0 et 6 etant les cases des chateaux)
        self.troll_case = troll_case

        # colonne 0 : nb de pierre jouees par le joueur 1 a l'etape i
        # colonne 1 : nb de pierre jouees par le joueur 1 a l'etape i
        # colonne 2 : case sur laquelle se trouve le troll a l'etape i juste avant que les joueurs ne jouent
        self.history = np.zeros((nb_stones, 3), dtype='int16')
        self.history[0, 2] = self.troll_case

        # les players peuvent etre definies apres
        # les players sont des objets qui doivent avoir une fonction: launch stones
        self.player1 = player1(nb_stones, nb_cases, self.history, 0)
        self.player2 = player2(nb_stones, nb_cases, self.history, 1)

        self.finish = False
        self.score = 0
        self.nb_step = 0

    def step(self):
        """
        Execute un tour du jeu
        @return: le sens de deplacement du troll
        """

        self.history[self.nb_step, 2] = self.troll_case

        stones1 = self.player1.launch_stones(self.nb_step)
        stones2 = self.player2.launch_stones(self.nb_step)

        print("Joueur 1: ", self.player1.nb_stones, " / ", stones1)
        print("Joueur 2: ", self.player2.nb_stones, " / ", stones2)

        assert stones1 > 0
        assert stones2 > 0

        assert stones1 <= self.player1.nb_stones
        assert stones2 <= self.player2.nb_stones

        self.history[self.nb_step, 0] = stones1
        self.history[self.nb_step, 1] = stones2

        self.player1.nb_stones -= stones1
        self.player2.nb_stones -= stones2

        if stones1 == stones2:
            # le troll ne bouge pas
            pass
        else:
            # sens dans lequel le troll va se deplacer

            depl = 0
            if stones2 > stones1:
                depl = -1
            else:
                depl = 1

            self.troll_case += depl

            return depl

    def play(self):
        assert self.player1 is not None
        assert self.player2 is not None

        self.print_board()

        while not self.finish:
            print("================================")
            print("nb_step: ", self.nb_step, "troll: ", self.troll_case)

            self.step()
            self.print_board()
            self.check_end_of_game()

            self.nb_step += 1
            print()

        print("Score: ", self.score)
        self.print_board()
        print()

    def check_end_of_game(self):
        """
        return
        """
        if self.troll_case <= -self.mp:
            # joueur 2 gagne
            self.finish = True
            self.score = -1
        elif self.troll_case >= self.mp:
            self.finish = True
            # joueur 1 gagne
            self.score = 1
        else:
            if self.player1.nb_stones == 0:
                self.finish = True
                # on fait avancer l'autre joueur d'autant que ses pierres

                deplacement = abs(self.troll_case - (-self.mp))
                nb_depl = min(deplacement, self.player2.nb_stones)
                self.player2.nb_stones -= nb_depl
                self.troll_case -= nb_depl
                print("plus de pierre 1")

            elif self.player2.nb_stones == 0:
                self.finish = True

                # on fait avancer l'autre joueur d'autant que ses pierres
                depl_max = abs(self.troll_case - self.mp)
                nb_depl = min(depl_max, self.player1.nb_stones)
                self.player1.nb_stones -= nb_depl
                self.troll_case += nb_depl
                print("plus de pierre 2")

            if self.troll_case <= -self.mp:
                # joueur 2 gagne
                self.finish = True
                self.score = -1
            elif self.troll_case >= self.mp:
                self.finish = True
                # joueur 1 gagne
                self.score = 1
            elif self.finish:
                if self.troll_case == 0:
                    # match nul
                    self.score = 0
                elif self.troll_case > 0:
                    # joueur 1 gagne: il gagne des points par rapport aux nombre de pierre qu'il lui reste
                    self.score = 1
                else:
                    # joueur 2 gagne: il gagne des points par rapport aux nombre de pierre qu'il lui reste
                    self.score = -1

        return self.finish

    def print_board(self):
        for i in range(-self.mp, self.mp+1):
            if i == self.troll_case:
                print("T", end =" ")
            else:
                print("_", end =" ")

    # ==== Fonctions pas interessantes =============

    def set_strat1(self, strat):
        self.strat1 = strat

    def set_strat2(self, strat):
        self.strat2 = strat
