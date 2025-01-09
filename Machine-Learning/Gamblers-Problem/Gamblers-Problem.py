import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

output_file_name = "Gamblers-Problem-Output.txt"
output_file_handler = open(output_file_name, 'w')

S = list(range(101))  # states 0 and 100 are terminal

# value iteration for the gambler's problem.
# V is the value function
# π is the policy
# ph is the probability of heads
def value_iteration(V, π, ph):
    γ = 1.0    # discount factor
    θ = 1e-6   # tolerance for convergence
    
    nstates = len(V)

    while(True):
        old_V = np.zeros(len(V))
        old_V[100] = 1.0 # Will not be altered in the loop, since state 100 is not a start_state

        # You cannot transition out of a state with 0 or 100 dollars.
        for start_state in range(1, nstates - 1):
            nactions = min(start_state, 100 - start_state) + 1 # Per the textbook problem
            old_V[start_state] = V[start_state]
            
            # You can gamble any amount of money up until what you have.
            q = np.zeros(nactions) 

            # You can gamble any amount of money up until what you have.
            for action in range(nactions):

                # Either gambled money was lost, or gambled money was double.
                for did_win in range(2):
                    # Adds action to start state if the user won; subtracts action to start state if they lost
                    new_state = start_state + (did_win * 2 - 1) * (action)
                    
                    # The probability of losing is 1 - ph; the probability of winning is ph
                    new_state_probability = (1 - ph) * (1 - did_win) + ph * did_win
                    q[action] += new_state_probability * (γ * V[new_state])
            greedy_action = np.argmax(q)
            π[start_state] = greedy_action
            V[start_state] = q[greedy_action]
                
        V_diff = np.abs(V - old_V)
        if np.max(V_diff) < θ:
            break

    
    return V, π
    # output the optimal value function and a deterministic policy


π = np.zeros(len(S))
V = np.zeros(len(S))  # will hold the value function
# note that zero is a (terminal) state, so if the state is s, then
# the index into V is s+1
V[100] = 1
V, π = value_iteration(V, π, 0.4)

print(V, file=output_file_handler)
print(π, file=output_file_handler)

output_file_handler.close()

plt.figure(num=0, dpi=120)
plt.plot(S, V)
plt.xlabel("Capital")
plt.ylabel("Value estimates")
plt.savefig("Value-Estimates.pdf", format="pdf")

plt.figure(num=1, dpi=120)
plt.plot(S, π)
plt.xlabel("Capital")
plt.ylabel("Amount to bet")
plt.savefig("Amount-to-Bet.pdf", format="pdf")
