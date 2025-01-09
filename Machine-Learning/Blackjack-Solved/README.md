This program users Reinforcement Learning to discover an optimal policy for blackjack. In other words, the output of this program tells a person the best move to make at any point in a game of blackjack. 

There are three pieces of information the program takes into account:
- The player's current sum
- The dealer's card showing
- Whether the player has a usable ace. An ace is counted towards the player's sum as an 11 and it is noted that the player could treat this as a 1 as well. If the player must treat it as a 1 to not surpass 21, it is not treated as usable.

### `Blackjack-Solved.py`
This implements a game of blackjack and iterates through it, evaluating which moves over 10 million games tended to be associated with victory, and which didn't.

### `BJ-Solution-No-Usable_Ace-2D.py`
Shows whether to hit or stick when the player doesn't have a usable ace based on algorithm.

### `BJ-Solution-Usable_Ace-2D.py`
Shows whether to hit or stick when the player does have a usable ace based on algorithm.

### `BJ-Solution-No-Usable_Ace-3D.py`
Shows how likely a player is to win at any given playing state when they have no usable ace, with 1 being 100% of winning and -1 being 100% chance of losing.

### `BJ-Solution-Usable_Ace-3D.py`
Shows how likely a player is to win at any given playing state when they have a usable ace, with 1 being 100% of winning and -1 being 100% chance of losing.