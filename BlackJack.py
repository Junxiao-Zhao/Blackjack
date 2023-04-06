import argparse
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
        :param n_game: the number of times to play
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

        probs = self.choose_dice(my_count, your_count)
        num_d = choices(range(self.n_dice + 1),
                        probs)[0]  # choose the number of dices
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
        """Play the game n times and write the output the file"""

        for i in range(self.n_game):
            print("Round %d" % i)
            self.play_once()

        correct_dices = np.zeros((self.l_target, self.l_target))
        related_prob = np.zeros((self.l_target, self.l_target))

        for x in range(self.l_target):
            for y in range(self.l_target):
                j = np.argmax(self.choose_dice(x, y))
                correct_dices[x, y] = j
                denom = self.win_count[x, y, j] + self.lose_count[x, y, j]
                prob_win = self.win_count[x, y, j] / denom if denom > 0 else 0
                related_prob[x, y] = prob_win

        with open("prog3_output.txt", 'w') as f:
            f.write(
                f"Game: NDice={self.n_dice}, NSides={self.n_side}, LTarget={self.l_target}, UTarget={self.u_target}\n\n"
            )
            f.write("Exact solution:\n\nPLAY =\n")
            np.savetxt(f, correct_dices, fmt="\t%d")
            f.write('\nPROB =\n')
            np.savetxt(f, related_prob, fmt='\t%.4f')

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

    def choose_dice(self, x: int, y: int) -> list:
        """Choose the number of dices with largest probability of winning

        :param x: the current point count for the player about to play
        :param y: the point count for the opponent
        :return: a list of winning probability
        """

        k = self.n_dice  # n_dices
        b, f_b = 0, 0  # the value of j with the highest value of f_j
        fj_list = []
        t = 0  # the total number of games that have gone through state (x, y)

        for j in range(k + 1):  # calculate f_j
            denom = self.win_count[x, y, j] + self.lose_count[x, y, j]
            f_j = self.win_count[x, y, j] / denom if denom > 0 else 0.5

            fj_list.append(f_j)
            t += denom

            if f_j > f_b:
                b, f_b = j, f_j

        g = sum(fj_list) - f_b  # sum over all j that are not b
        p_b = (t * f_b + self.m) / (t * f_b + k * self.m)
        pj_list = []

        for j in range(len(fj_list)):  # calculate p_j
            if j != b:
                p_j = (1 - p_b) * (t * fj_list[j] +
                                   self.m) / (g * t + (k - 1) * self.m)
                pj_list.append(p_j)
            else:
                pj_list.append(p_b)

        return pj_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A program learns to play Blackjack")
    parser.add_argument("-d",
                        nargs=1,
                        type=int,
                        required=True,
                        help="the number of dices")
    parser.add_argument("-s",
                        nargs=1,
                        type=int,
                        required=True,
                        help="the number of sides each dice")
    parser.add_argument("-l",
                        nargs=1,
                        type=int,
                        required=True,
                        help="the lower bound of winning")
    parser.add_argument("-u",
                        nargs=1,
                        type=int,
                        required=True,
                        help="the upper bound of winning")
    parser.add_argument("-m",
                        nargs=1,
                        type=int,
                        required=True,
                        help="the hyperparameter")
    parser.add_argument("-n",
                        nargs=1,
                        type=int,
                        required=True,
                        help="the number of times to play")
    args = parser.parse_args()

    g = BlackJack(n_dice=args.d[0],
                  n_side=args.s[0],
                  l_target=args.l[0],
                  u_target=args.u[0],
                  m=args.m[0],
                  n_game=args.n[0])
    g.play()
