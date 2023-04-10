# A program that learns to play "Blackjack"
A program that learns to play a variant of the card game "Blackjack" in the same way as the AlphaZero program.

### Game
- Two players alternately roll dice, and keep track of their total across turns. 
- They are each trying to reach a sum that lies in a specified target, between a fixed low value and high value. 
- If a player reaches a score in the target range, they immediately win; If they exceed the high value, they immediately lose.
- The players can choose the number of dice to roll on each turn, between 1 and a fixed maximum.

### Usage
    usage: BlackJack.py [-h] -d D -s S -l L -u U -m M -n N

    A program learns to play Blackjack

    optional arguments:
    -h, --help  show this help message and exit
    -d D        the number of dices
    -s S        the number of sides each dice
    -l L        the lower bound of winning
    -u U        the upper bound of winning
    -m M        the hyperparameter
    -n N        the number of times to play

### Example
- Input: `python BlackJack.py -d 2 -s 3 -l 6 -u 7 -m 100 -n 100000`
- Output: the correct number of dice to roll in each state and the corresponding probability. See [output.txt](./output.txt).