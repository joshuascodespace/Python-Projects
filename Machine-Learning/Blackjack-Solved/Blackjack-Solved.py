import numpy as np
import random
import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
# %matplotlib inline # Necessary for notebook environments
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns


# solving the black jack game

# the face values for a suit
# ace through nine, ten, jack, queen, king
# note that 1=ace
suit = ([1] + list(range(2,10)) + [10] * 4)

# a deck of cards consists of four suits: diamonds, clubs, hearts, spades
deck = suit * 4
random.shuffle(deck)     # a random permutation

# to simulate an infinite deck, we can sample with replacement
def deal_cards(n):
    return random.choices(deck, k=n)

# note that it's quite possible (in fact it's common) to have more than
# one ace in a hand, but it's not possible to have two "usable" aces.
# 0/1 = no/yes
def usable_ace(hand):
    return (1 in hand and sum(hand) <= 11) * 1

def score(hand):
    return sum(hand) + usable_ace(hand) * 10

# simulate an episode of blackjack according to policy π
def blackjack(π, ϵ = 0.05):
    player = deal_cards(2)
    player_sum = score(player)
    dealer = deal_cards(2)
    dealer_sum = score(dealer)

    while player_sum < 12:
        new_card = deal_cards(1)[0]
        player.append(new_card)
        player_sum = score(player)
        
    actions = []
    states = []
    
    if player_sum == 21:
        states.append([player_sum, dealer[1], usable_ace(player)])
        actions.append(1)
        if dealer_sum == 21:
            return states, actions, 0.0
        else:
            return states, actions, 1.0

    while(True):
        states.append([player_sum, dealer[1], usable_ace(player)])
        # Player can only make decision based on second card drawn by dealer.
        action = π[player_sum - 12, dealer[1] - 1, usable_ace(player)]
        if random.random() < ϵ:
            action = random.choices([0,1])[0]
        actions.append(action)
        if action == 1:
            break
        else:
            new_card = deal_cards(1)[0]
            player.append(new_card)
            player_sum = score(player)
            if player_sum > 21:
                return states, actions, -1.0
            if player_sum == 21:
                if dealer_sum == 21:
                    return states, actions, 0.0
                else:
                    return states, actions, 1.0
    
    while dealer_sum < 17:
        new_card = deal_cards(1)[0]
        dealer.append(new_card)
        dealer_sum = score(dealer)
    
    if dealer_sum > 21 or player_sum > dealer_sum:
        return states, actions, 1.0
    elif dealer_sum > player_sum:
        return states, actions, -1.0
    else:
        return states, actions, 0.0
        



    


# this is on-policy every-visit MC control because we do not check for
# 1st visits to states; however, for the game of blackjack, it's not
# possible to visit the same state twice in an episode. you could have
# an ace being counted as 11, and then later being counted as 1, but
# the indicator for a usable ace is part of the state.  also, note
# that we maintain exploration of nonoptimal actions in the function
# blackjack().
def MC(q, qn, π):
    for i in range(int(10e6)):
        if i % 100000 == 0:
            print("episode ", i)
        states, actions, r = blackjack(π)
        assert(len(states) == len(actions))
        assert( r in [-1.0, 0.0, 1.0])
        T = len(states)
        for t in range(T):
            x=0

            player_hand = states[t][0] - 12
            dealer_hand = states[t][1] - 1
            usable_ace = states [t][2]
            action = actions[t]
            qn[player_hand,dealer_hand,usable_ace,action] += 1
            q[player_hand, dealer_hand, usable_ace, action] += (r - q[player_hand, dealer_hand, usable_ace, action])/qn[player_hand, dealer_hand, usable_ace, action]

            allidx = [j for j in [0,1] if q[player_hand, dealer_hand, usable_ace, j] == np.max(q[player_hand, dealer_hand, usable_ace, :])]
            assert(allidx in [ [0], [1], [0,1]])
            if len(allidx) > 1:
                idx = random.choices(allidx)[0]
            else:
                idx = allidx[0]

            π[player_hand, dealer_hand, usable_ace] = idx
            # since this is every-visit MC, the reward at the end
            # of the episode is the return for each state visited, and
            # there is no discounting, the direction of iteration over
            # the episode should not matter.
            
        


# the state space consists of
# the player's sum 12:21,
# the dealer's showing card 1:10,
# and indicator for usable ace no/yes=1/2
# for a total of 200 possible states.
# the action is hit/stick=1/2

# the initial policy is to stick when the player's sum is 20 or 21, otherwise hit
π = np.full((10, 10, 2), 0)
π[8:10,:,:] = 1           # stick when sum is 20 or 21
q = np.zeros((10, 10, 2, 2))    # q(state=(player,dealer,usable), action)
qn = np.zeros((10, 10, 2, 2))   # to hold the number of observations
MC(q, qn, π)


player_string = [str(i) for i in range(12, 22)]  
dealer_string = [str(i) for i in range(1,11)]
player_int = np.arange(12,22)
dealer_int = np.arange(1,11)


# plot the optimal policy
z = π[:,:,1]

plt.figure(figsize=(20,20))
plt.title("Usable ace")
pl1 = sns.heatmap(pd.DataFrame(z, index=player_string, columns=dealer_string))
plt.xlabel("Dealer showing")
plt.ylabel("Player sum")
plt.savefig("BJ-Solution-Usable-Ace-2D.pdf",format="pdf")

plt.figure(figsize=(20,20))
plt.title("No usable ace")
z = π[:,:,0]
pl2 = sns.heatmap(pd.DataFrame(z, index=player_string, columns=dealer_string))
plt.xlabel("Dealer showing")
plt.ylabel("Player sum")
plt.savefig("BJ-Solution-No-Usable-Ace-2D.pdf",format="pdf")

# plot(pl1,pl2)
# obtain the state-value function v from the action-value function q
v = np.zeros((10, 10, 2))
for pl in range((q.shape)[0]):
    for de in range ((q.shape)[1]):
        for us in range((q.shape)[2]):
            v[pl,de,us] = np.max(q[pl,de,us,:])
        
    
fig1 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
X, Y = np.meshgrid(dealer_int, player_int)
Z = v[:, :, 1].astype(float)  # Values corresponding to "usable ace"
ax1.plot_surface(X, Y, Z, cmap='viridis')
ax1.set_xlabel("Dealer showing")
ax1.set_ylabel("Player sum")
ax1.set_zlabel("Value")
ax1.set_title("Usable ace")
ax1.set_zlim(-1.0, 1.0)
plt.savefig("BJ-Solution-Usable-Ace-3D.pdf",format="pdf")

fig2 = plt.figure()
ax2 = fig2.add_subplot(111, projection='3d')
Z = v[:, :, 0] 
ax2.plot_surface(X, Y, Z, cmap='viridis')
ax2.set_xlabel("Dealer showing")
ax2.set_ylabel("Player sum")
ax2.set_zlabel("Value")
ax2.set_title("No usable ace")
ax2.set_zlim(-1.0, 1.0)
plt.savefig("BJ-Solution-No-Usable-Ace-3D.pdf",format="pdf")