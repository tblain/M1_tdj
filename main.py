from jeux import Jeu
from strats import Strategie_naive_always_1, Strategie_naive_always_2, Strategie_naive_defensive, Strategie_naive_plus_one, Strategie_prudente

jeu = Jeu(Strategie_prudente, Strategie_naive_defensive, 23, 20, -1)

jeu.play()
