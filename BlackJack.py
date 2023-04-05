import numpy as np
from random import randint, choices


def play_game(n_dice: int, n_side: int, l_target: int, u_target: int,
              lose_count: np.ndarray, win_count: np.ndarray, m: float):
    """Play the game once

    :param n_dice: the number of dices
    :param n_side: the sides of a dice
    :param l_target: the lower bound of winning
    :param u_target: the upper bound of winning
    :param lose_count: the num of current player lost at state (x, y)
    :param win_count: the num won at state (x, y)
    :param m: the hyperparameter
    """

    def each_turn(my_count: int, your_count: int, my_player: list,
                  your_player: list) -> tuple:
        """Calculate num of dices and total for each player in each turn

        :param my_count: total of current player
        :param your_count: total of opponent
        :param my_player: current player's previous (x, y, j)
        :param your_player: opponent's previous (x, y, j)
        :return: updated total of current player after this turn, winner, and loser
        """

        num_d = randint(1, n_dice)  # TODO: choose the max prob
        result = sum(choices(range(1, n_side + 1), k=n_dice))
        my_player.append((my_count, your_count, num_d))
        my_count += result

        winner = loser = None
        if my_count >= l_target and my_count <= u_target:  # player win
            winner = my_player
            loser = your_player
        elif my_count > u_target:  # player lose
            winner = your_player
            loser = my_player

        return my_count, winner, loser

    player1, player2 = [], []
    count1 = count2 = 0
    winner = loser = None

    while True:

        count1, winner, loser = each_turn(count1, count2, player1, player2)
        if winner is not None:
            break

        count2, winner, loser = each_turn(count2, count1, player2, player1)
        if winner is not None:
            break

    for x, y, j in winner:
        win_count[x, y, j] += 1

    for x, y, j in loser:
        lose_count[x, y, j] += 1

    print(win_count)
    print(lose_count)


def choose_dice(x: int, y: int, lose_count: np.ndarray, win_count: np.ndarray,
                m: float) -> int:
    """Choose the number of dices with largest probability of winning

    :param x: the current point count for the player about to play
    :param y: the point count for the opponent
    :param lose_count: the num of current player lost at state (x, y)
    :param win_count: the num won at state (x, y)
    :param m: the hyperparameter
    :return: the num of dices
    """

    k = len(lose_count[x][y]) - 1  # n_dices
    b, f_b = 0, 0.5  # the value of j with the highest value of f_j
    fj_list = [0]
    t = 0  # the total number of games that have gone through state (x, y)

    for j in range(1, k + 1):  # calculate f_j
        denom = win_count[x, y, j] + lose_count[x, y, j]
        f_j = win_count[x, y, j] / denom if denom > 0 else 0.5

        fj_list.append(f_j)
        t += denom

        if f_j > f_b:
            b, f_b = j, f_j

    g = sum(fj_list) - f_b  # sum over all j that are not b
    p_b = (t * f_b + m) / (t * f_b + k * m)
    pj_list = [0]

    for j in range(1, len(fj_list)):  # calculate p_j
        if j != b:
            p_j = (1 - p_b) * (t * fj_list[j] + m) / (g * t + (k - 1) * m)
            pj_list.append(p_j)
        else:
            pj_list.append(p_b)

    return np.argmax(pj_list)  # the num max prob


if __name__ == "__main__":
    """ lose_count = [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                  [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                  [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 2, 1, 1]]]
    win_count = [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                 [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                 [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 3, 1]]] """
    lose_count = np.zeros((15, 15, 3))
    win_count = np.zeros((15, 15, 3))
    # print(choose_dice(2, 3, lose_count, win_count, 4))
    play_game(2, 6, 15, 17, lose_count, win_count, 4)
