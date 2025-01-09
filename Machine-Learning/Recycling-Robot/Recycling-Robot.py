import numpy as np
import pandas as pd

output_file_name = "Recycling-Robot-Output.txt"
output_file_handler = open(output_file_name, 'w')
# an implementation of value iteration to solve for the optimal policy
# for the recycling robot that is described on page 52 of the RL book.

S = [0,1]    # state is lo, hi
A = [0,1,2]  # action is search, wait, recharge

# transition probabilities when searching
# when action = search
#       lo   hi
#    -------------
# lo |  β   1-β
# hi |1-α    α
α = 0.2
β = 0.3
r_search = 5.0   # expected reward when searching
r_wait = 1.0
r_search_failed = -3.0
r_recharge = 0.0

# the 4-argument transition probabilities p(sprime,r|s,a).
# let's try to get by with the 3-argument probabilities p(sprime|s,a)
# that are shown in the table on page 52.
# the indexing is p[s, a, sprime]
p3 = np.zeros((2, 3, 2))
p3[1,0,1] = α
p3[1,0,0] = 1-α
p3[0,0,1] = 1-β
p3[0,0,0] = β
p3[1,1,1] = 1
p3[0,1,0] = 1
p3[0,2,1] = 1
# now note that when the state=hi, action=recharge will not be considered.
# we will take care of that in the value iteration function.

# an implementation of the value iteration algorithm shown on page
# 83 in the RL book.
def value_iteration(V, π):
    γ = 0.9    # discount factor
    θ = 1e-6   # tolerance for convergence
    k = 0      # ieration/sweep
    nstates, nactions = np.shape(π)
    
    while(True):
        old_V = np.zeros(np.shape(V))

        for start_state in range(nstates):
            # Need to assign values to old_V one value at a time, so changes in V don't copy over to old_V
            old_V[start_state] = V[start_state] 
            q = np.zeros(nactions)
            # Ensures that argmax doesn't consider the possibility where recharging happens in a high state
            if start_state == 2:
                q[2] = np.nan
            
            for action in range(nactions):
                
                
                for new_state in range(nstates):
                    # Only calculates new policy if we are not recharging at a high state.
                    if not (start_state == 1 and action == 2):
        
                        if (action == 1):
                            reward = r_wait
                        elif (action == 2):
                            reward = r_recharge
                        # The search only fails if we start at a low state, and end at a high state, since this implies the robot died and had to be recharged.
                        elif (action == 0 and start_state == 0 and new_state == 1):
                            reward = r_search_failed
                        else:
                            reward = r_search

                        q[action] += p3[start_state, action, new_state] * (reward + γ * V[new_state])
            greedy_action = np.argmax(q)
            V[start_state] = q[greedy_action]
            π.loc[start_state, :] = 0 # Policy rejects all options that aren't the greedy action per algorithm.
            π.loc[start_state, greedy_action] = 1
         
        V_diff = np.abs(V - old_V)
        max_diff = np.max(V_diff)
        if max_diff < θ:
            print("Converged in", k, "iterations.")
            break

        k += 1


    return V, π
    # output the optimal value function and a deterministic policy


# the policy: rows correspond to states, columns correspond to actions.
π = pd.DataFrame(np.zeros((len(S),len(A))), index=S, columns=A)
π.loc[0, 0] = 1/3
π.loc[0, 1] = 1/3
π.loc[0, 2] = 1/3
π.loc[1, 0] = 0.5
π.loc[1, 1] = 0.5

V = np.zeros(len(S))  # will hold the value function
V, π = value_iteration(V, π)
print(π, file=output_file_handler)
print(V, file=output_file_handler)

output_file_handler.close()