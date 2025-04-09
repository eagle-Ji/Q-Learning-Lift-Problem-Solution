# Q-Learning Lift Problem Solution

## Problem Overview

This repository contains a Q-learning implementation to solve the lift (elevator) system problem. The goal is to train an agent to efficiently operate an elevator by making decisions on when to move, wait, and pick up or drop off passengers in a multi-floor building. The system involves passengers arriving randomly at different floors, and the lift must learn to pick them up and drop them off at their desired destinations while minimizing unnecessary movements and waiting.

## Project Files

- **`environment_design.py`**: Contains the environment logic, including the state space, action space, and reward structure.
- **`agent_design.py`**: Contains the Q-learning agent's implementation, including the training loop.
- **`Q_Table.npy`**: The Q-table containing the learned values for state-action pairs.
- **`Reward_Data.npy`**: The cumulative reward data during training.
- **`learning_Curve.png`**: Plot of the cumulative reward over episodes.
- **`drop_pick_policy.PNG`**: Visualization of the optimal drop-off and pick-up policy.
- **`Q_2.PNG`**: Visualization of the Q-values for state-action pairs.
- **`reward.PNG`**: A plot showing the reward distribution during the training.

---

## Detailed Explanation

### 1. **Environment Class (Lift Problem)**

The environment is designed to simulate the lift's operation. It includes the following components:

#### **State Representation:**

The state is represented as a string combining several key variables:
- `self.current_floor`: The lift’s current floor.
- `self.next_floor`: The next floor the lift is going to.
- `self.psngr_drop_floor`: The destination floors for passengers that are in the lift.
  
For example, the state could look like this:  
`state = str(self.current_floor) + str(self.next_floor) + str(self.psngr_drop_floor[0]) + str(self.psngr_drop_floor[1]) + str(self.psngr_drop_floor[2])`

#### **Action Space:**

The agent can take the following actions:
1. `"UP"`: Move the lift one floor up.
2. `"DOWN"`: Move the lift one floor down.
3. `"WAIT"`: Keep the lift at the current floor.
4. `"PICKUP/DROPOFF"`: Pick up passengers at the current floor and drop off passengers whose destination is the current floor.

#### **Reward Structure:**

The reward is structured as follows:
- **For each dropped-off passenger**: A reward of +10 is given.
- **For each non-productive action (like waiting or moving without a passenger drop)**: A penalty of -1 is applied.

#### **Mathematics (Reward Calculation):**

- **For dropped-off passengers**: 
  \[
  \text{Reward} = 10 \times \text{Number of passengers dropped off}
  \]
  This reward is given whenever passengers are dropped off at their desired floor.

- **For non-productive actions** (waiting or moving without dropping off passengers):
  \[
  \text{Penalty} = -1 \times (\text{Lift passenger count} + \text{Total passengers at all floors})
  \]
  This penalty discourages waiting or moving the lift unnecessarily.

---

### 2. **Training Loop (Q-learning Agent)**

The Q-learning agent follows these steps to learn the optimal policy:

#### **Initialization:**

- The Q-table is initialized with zeros for all state-action pairs.
- The agent starts with an epsilon (\(\epsilon\)) of 1.0, meaning it will initially take random actions to explore the environment. Over time, epsilon decays, and the agent increasingly exploits the best-known actions.
  
#### **For Each Episode:**

1. **State Reset**: 
   The environment is reset to a random state.

2. **Action Selection (Epsilon-Greedy Policy):**
   The agent selects an action based on the epsilon-greedy policy:
   - With probability \(\epsilon\), it takes a random action (exploration).
   - With probability \(1 - \epsilon\), it takes the action that maximizes the Q-value (exploitation).
   
   Mathematically:
   \[
   \text{With probability} \, \epsilon: \, \text{Choose a random action}
   \]
   \[
   \text{With probability} \, (1 - \epsilon): \, \text{Choose the action with the highest Q-value}
   \]

3. **Action Execution**:
   The chosen action is applied to the environment. The agent receives a reward and the next state is determined.

4. **Q-value Update (Temporal Difference):**
   The Q-value for the current state-action pair is updated using the Temporal Difference (TD) learning formula:
   \[
   Q(s_t, a_t) = Q(s_t, a_t) + \alpha \left[ R_t + \gamma \cdot \max_a Q(s_{t+1}, a) - Q(s_t, a_t) \right]
   \]
   where:
   - \( Q(s_t, a_t) \) is the Q-value of the state-action pair.
   - \( R_t \) is the immediate reward received.
   - \( \gamma \) is the discount factor (how much future rewards are considered).
   - \( \alpha \) is the learning rate.
   - \( \max_a Q(s_{t+1}, a) \) is the maximum Q-value for the next state.

5. **Epsilon Decay**:
   After each action, epsilon is decayed to decrease exploration over time, allowing the agent to exploit what it has learned. The decay is controlled by a decay rate:
   \[
   \epsilon_{t+1} = \epsilon_t - \text{decay rate}
   \]

6. **Reward Tracking**: 
   The cumulative reward for each episode is tracked and saved in `Reward_Data.npy`.

#### **Mathematics (Q-value Update)**:

The Q-value update is key to Q-learning:
\[
Q(s_t, a_t) = Q(s_t, a_t) + \alpha \left[ R_t + \gamma \cdot \max_a Q(s_{t+1}, a) - Q(s_t, a_t) \right]
\]
Where:
- \( Q(s_t, a_t) \) is the value for taking action \(a_t\) in state \(s_t\).
- \( R_t \) is the immediate reward after performing action \(a_t\).
- \( \gamma \) (gamma) is the discount factor that controls how much future rewards are considered.
- \( \alpha \) (alpha) is the learning rate, controlling how quickly new information overrides old information.

---

## Results

### **Learning Curve**

Below is the plot of the cumulative reward during the training process, showing how the agent's performance improves over time. The curve tracks how the agent's rewards accumulate as it learns to efficiently pick up and drop off passengers.

![Learning Curve](learning_Curve.png)

### **Optimal Policy**

This plot shows the optimal pick-up and drop-off policy learned by the agent. The policy indicates the best actions for the agent to take based on the current state.

![Pick-up/Drop-off Policy](drop_pick_policy.PNG)

### **Q-Values**

This image shows the Q-values associated with different state-action pairs. The values represent the expected cumulative reward for each state-action pair, which the agent uses to make decisions.

![Q-Values](Q_2.PNG)

### **Reward Distribution**

This image illustrates the reward distribution during training, showing how the agent's actions resulted in different reward values over the episodes.

![Reward Distribution](reward.PNG)

---

## How to Run the Code

1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install numpy matplotlib
