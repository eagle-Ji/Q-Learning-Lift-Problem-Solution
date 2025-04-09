# Q-Learning Lift Problem Solution

## Problem Overview

This repository contains a Q-learning implementation to solve the lift (elevator) system problem. The goal is to train an agent to efficiently operate an elevator by making decisions on when to move, wait, and pick up or drop off passengers in a multi-floor building. 

## Project Files

- **`environment_design.py`**: Contains the environment logic, including the state space, action space, and reward structure.
- **`agent_design.py`**: Contains the Q-learning agent's implementation, including the training loop.
- **`Q_Table.npy`**: The Q-table containing the learned values for state-action pairs.
- **`Reward_Data.npy`**: The cumulative reward data during training.
- **`learning_Curve.png`**: Plot of the cumulative reward over episodes.
- **`drop_pick_policy.PNG`**: Visualization of the optimal drop-off and pick-up policy.
- **`Q_2.PNG`**: Visualization of the Q-values for state-action pairs.
- **`reward.PNG`**: A plot showing the reward distribution during the training.

## How the Q-Learning Algorithm Works

### 1. **State Representation**
The state of the system is represented as a combination of the current floor, next floor, and the floors where passengers need to be dropped off. 

### 2. **Action Space**
The agent can perform the following actions:
- `"UP"`: Move the lift one floor up.
- `"DOWN"`: Move the lift one floor down.
- `"WAIT"`: Keep the lift at the current floor.
- `"PICKUP/DROPOFF"`: Pick up passengers and drop them off at their destination.

### 3. **Reward Structure**
- **Positive reward**: +10 for each passenger dropped off at their destination.
- **Negative reward**: -1 for unnecessary actions like waiting or moving without a passenger drop-off.

### 4. **Q-Learning Update**
The Q-values are updated using the Temporal Difference (TD) learning formula:
\[
Q(s_t, a_t) = Q(s_t, a_t) + \alpha \left[ R_t + \gamma \cdot \max_a Q(s_{t+1}, a) - Q(s_t, a_t) \right]
\]
Where:
- \( Q(s_t, a_t) \) is the Q-value of the state-action pair.
- \( \alpha \) is the learning rate.
- \( \gamma \) is the discount factor.
- \( R_t \) is the immediate reward.

### 5. **Epsilon-Greedy Policy**
The agent uses an epsilon-greedy policy to balance exploration and exploitation. Initially, it explores more randomly (with a high epsilon), and over time, as epsilon decays, it exploits the learned Q-values more.

---

## Results

### **Learning Curve**
Below is the plot of the cumulative reward during the training process, showing how the agent's performance improves over time.

![Learning Curve](learning_Curve.png)

### **Optimal Policy**
This plot shows the optimal pick-up and drop-off policy learned by the agent.

![Pick-up/Drop-off Policy](drop_pick_policy.PNG)

### **Q-Values**
This image shows the Q-values associated with different state-action pairs.

![Q-Values](Q_2.PNG)

### **Reward Distribution**
This image illustrates the reward distribution during training.

![Reward Distribution](reward.PNG)

---

## How to Run the Code

1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install numpy matplotlib
