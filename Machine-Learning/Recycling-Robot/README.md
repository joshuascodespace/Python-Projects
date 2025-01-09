Finds the most optimal policy for a robot who's goal is to recycle. At any given point, the robot can wait in place for someone to give it recycling, move around to look for recycling, or recharge itself so it doesn't run out of battery. If the robot searches for recycling, it might lower its battery. This isn't true for any other decisions. At any point, the robot is either at a low energy state, a high energy state, or out of batteries in which a human must recharge the robot. This last possibility is strongly discouraged by the policy.

### `Recycling-Robot.py`
Finds an optimal policy for the robot in the above situation.

### `Recycling-Robot-Output.txt`
Shows the optimal policy for the robot in the above situation in which 0 as a column represents the decision to search, 1 represents the decision to wait, and 2 represents the decision to recharge. As a crow, 0 represents the state of being low energy, and 1 represents a state of high energy