All code either fully created by me or translated by myself into python from another person's pre-existing Julia program. Did not write most comments myself.

### Blackjack-Solved
This program users Reinforcement Learning to discover an optimal policy for blackjack. In other words, the output of this program tells a person the best move to make at any point in a game of blackjack. 

### Gamblers-Problem
This program uses reinforcement learning to find the best decisions for a gambler to make at any given time in the following situation: 

A gambler bets an amount of money and then flips a coin. If the coin lands head, the gambler doubles the money bet. If the coin lands tails, the gambler loses the money bet. The gambler's goal is to get 100 cents, in which case they win. The gambler must bet until they either run out of money, or reach this sum.

### K-Means-Clustering
Implements K-Means-Clustering to categorize data into four different groups

### Neural-Network
Implements a neural network that learns to correctly identify hand-written digits. Finite Differencing is then used to test the accuracy of the gradient descent used in this neural network.

### Q-Learning
Implements Q-Learning to solve a problem in which a person wishes to move from one point on a grid to another point on a grid. While doing so, the person wishes to avoid certain areas on the grid.

### Recycling-Robot
Finds the most optimal policy for a robot who's goal is to recycle. At any given point, the robot can wait in place for someone to give it recycling, move around to look for recycling, or recharge itself so it doesn't run out of battery. If the robot searches for recycling, it might lower its battery. This isn't true for any other decisions. At any point, the robot is either at a low energy state, a high energy state, or out of batteries in which a human must recharge the robot. This last possibility is strongly discouraged by the policy.
