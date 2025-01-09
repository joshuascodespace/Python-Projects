import numpy as np
import random
import pandas as pd

output_file_name = "Q-Learning-Output.txt"
output_file_handler = open(output_file_name, 'w')

start = 36
goal = 37
nstates = 37
nactions = 4

def nextstate(s, a): # return next state when taking action a from state s
    if (s == goal) or (s == 35 and a == 1):
        return goal
    elif (s == start and a == 2) or ((s in range(25,35)) and a == 1):
        return start   # stepped into the cliff so back to start
    elif (s in [0, 12, 24, 36]) and a == 3:  # step off grid to left
        return s
    elif (s in range(12)) and a == 0:    # step off grid above
        return s
    elif (s in [11, 23, 35]) and a == 2:   # step off grid to right
        return s
    elif (s in range(11)) and a == 2: # step to right
        return s + 1
    elif (s in range(1,12)) and a == 3:
        return s - 1
    elif (s in range(12,23)) and a == 2: # step to right
        return s + 1
    elif (s in range(13, 24)) and a == 3:
        return s - 1
    elif (s in range(24,35)) and a == 2:
        return s + 1
    elif (s in range(25,36)) and a == 3:
        return s - 1
    elif (s in range(24)) and a == 1:
        return s + 12
    elif (s in range(12,36)) and a == 0:
        return s - 12
    elif s == start and a == 1:
        return s
    elif s == start and a == 0:
        return 24
    elif s == 24 and a == 1:
        return start
    else:
        print("!!! unexpected state $(s) and action $(a) !!!")
        print(s, a)
        assert False

def reward(s, a):
    if s == goal:
        r = 0
    elif (s == start and a == 2) or ((s in range(25,35)) and a == 1):
        r = -100
    else:
        r = -1
    return r

def qlearn(Q):
    alpha = 0.5
    gamma = 1.0
    epsilon = 0.10
    episodes = []

    for i in range(10000):
        path = []
        policy = []
        state = start
        k=0
        
        while(state != goal):
            action = np.argmax(Q[state, :])
            if random.random() < epsilon:
                action = random.choice([0,1,2,3])
            new_state = nextstate(state, action)

            r = reward(state, action)

            
            Q[state, action] += alpha * (r + gamma * (np.max(Q[new_state, :]) - Q[state, action]))

            path.append(state)
            policy.append(action)
            state = new_state
            k += 1

        episodes.append(k)
    
Q = np.zeros((nstates + 1, nactions)) # Extra state included to include the goal state.
qlearn(Q)

for i in range(nstates):
    if i in [11, 23, 35]:
        print(np.argmax(Q[i, :]), file=output_file_handler)
    else:
        print(np.argmax(Q[i, :]), end='\t', file=output_file_handler)

output_file_handler.close()
            