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
- `python BlackJack.py -d 2 -s 3 -l 6 -u 7 -m 100 -n 100000`