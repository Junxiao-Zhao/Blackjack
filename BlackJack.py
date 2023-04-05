import numpy as np
from random import choices


class BlackJack:

    def __init__(self, n_dice: int, n_side: int, l_target: int, u_target: int,
                 n_game: int, m: float) -> None:
        """The Black Jack Game

        :param n_dice: the number of dices
        :param n_side: the number of sides each dice
        :param l_target: the lower bound of winning
        :param u_target: the upper bound of winning
        :param n_game: the number of games
        :param m: the hyperparameter
        """

        self.n_dice = n_dice
        self.n_side = n_side
        self.l_target = l_target
        self.u_target = u_target
        self.n_game = n_game
        self.m = m
        self.lose_count = np.zeros((l_target, l_target, n_dice + 1))
        self.win_count = np.zeros((l_target, l_target, n_dice + 1))

    def each_turn(self, my_count: int, your_count: int, my_player: list,
                  your_player: list) -> tuple:
        """Calculate num of dices and total for each player in each turn

        :param my_count: total of current player
        :param your_count: total of opponent
        :param my_player: current player's previous (x, y, j)
        :param your_player: opponent's previous (x, y, j)
        :return: updated total of current player after this turn, winner, and loser
        """

        num_d = self.choose_dice(my_count,
                                 your_count)  # choose the number of dices
        result = sum(choices(range(1, self.n_side + 1),
                             k=num_d))  # sum of this turn
        my_player.append((my_count, your_count, num_d))  # update state
        my_count += result  # update total

        winner = loser = None
        if my_count >= self.l_target and my_count <= self.u_target:  # player win
            winner = my_player
            loser = your_player
        elif my_count > self.u_target:  # player lose
            winner = your_player
            loser = my_player

        return my_count, winner, loser

    def play(self) -> None:
        """Play the game n times"""

        for _ in range(self.n_game):
            self.play_once()

    def play_once(self) -> None:
        """Play the game once"""

        player1, player2 = [], []
        count1 = count2 = 0
        winner = loser = None

        while True:

            count1, winner, loser = self.each_turn(count1, count2, player1,
                                                   player2)
            if winner is not None:
                break

            count2, winner, loser = self.each_turn(count2, count1, player2,
                                                   player1)
            if winner is not None:
                break

        for x, y, j in winner:
            self.win_count[x, y, j] += 1

        for x, y, j in loser:
            self.lose_count[x, y, j] += 1

    def choose_dice(self, x: int, y: int) -> int:
        """Choose the number of dices with largest probability of winning

        :param x: the current point count for the player about to play
        :param y: the point count for the opponent
        :return: the num of dices
        """

        k = len(self.lose_count[x][y]) - 1  # n_dices
        b, f_b = 0, 0.5  # the value of j with the highest value of f_j
        fj_list = [0]
        t = 0  # the total number of games that have gone through state (x, y)

        for j in range(1, k + 1):  # calculate f_j
            denom = self.win_count[x, y, j] + self.lose_count[x, y, j]
            f_j = self.win_count[x, y, j] / denom if denom > 0 else 0.5

            fj_list.append(f_j)
            t += denom

            if f_j > f_b:
                b, f_b = j, f_j

        g = sum(fj_list) - f_b  # sum over all j that are not b
        p_b = (t * f_b + self.m) / (t * f_b + k * self.m)
        pj_list = [0]

        for j in range(1, len(fj_list)):  # calculate p_j
            if j != b:
                p_j = (1 - p_b) * (t * fj_list[j] +
                                   self.m) / (g * t + (k - 1) * self.m)
                pj_list.append(p_j)
            else:
                pj_list.append(p_b)
        print(pj_list)
        return np.argmax(pj_list)  # the num max prob


if __name__ == "__main__":
    lose_count = np.array([[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                            [0, 0, 0, 0]],
                           [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                            [0, 0, 0, 0]],
                           [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                            [0, 2, 1, 1]]])
    win_count = np.array([[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                           [0, 0, 0, 0]],
                          [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                           [0, 0, 0, 0]],
                          [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                           [0, 0, 3, 1]]])
    """ lose_count = np.zeros((15, 15, 3))
    win_count = np.zeros((15, 15, 3))
    print(choose_dice(2, 3, lose_count, win_count, 4))
    play_game(2, 6, 15, 17, lose_count, win_count, 4) """

    g = BlackJack(2, 6, 15, 17, 10, 4)
    for i in range(10):
        g.play_once()
