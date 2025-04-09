

from environment_design import environment
import numpy as np
import matplotlib.pyplot as plt  

# Following are the optimal hyperparameters found after various tries. 

num_of_steps_per_episode = 500

number_of_episodes = 5000
gamma = 0.99
epsilon = 1.0 
decay = 7e-7
learning_rate =0.01
"""
number_of_episodes = 1000
gamma = 0.99 
epsilon = 1.0 
decay = 2e-6
learning_rate = 0.008
"""
eps_track = []
env = environment()
reward_track = []
actions_list = {"UP": 0, "DOWN":1, "WAIT": 2, "PICKUP/DROPOFF":3}

Q_table = dict()


for epi in range(number_of_episodes): # Run training for given episodes
    state = env.reset()
    episode_reward = 0
    rew = 0
    done = False
    for steps in range(num_of_steps_per_episode+1): # only stay in one episode for 500 steps. 
        
        if state not in Q_table.keys(): # save the state as key if state is not present in Q table
            Q_table[state] = [0,0,0,0]
        if epsilon > np.random.uniform(0,1): # Epsilon defines the randomness in the learning. 
            action = np.random.choice(env.action_space) # take actions randomly 
        else:
            action = env.action_space[np.argmax(Q_table[state][::])] # take action with greedy policy 
            #action =
            
        n_state, reward, done = env.step(action)
        #print(actions_list[action])
        
        if n_state not in Q_table.keys(): # save the next state as key if state is not present in Q table
            Q_table[n_state] = [0,0,0,0]
        
        # At each step train the Q learning agent using TD equation for Q learning. 
        old_Q_value = Q_table[state][actions_list[action]]
        if done==False:
            # Temporal Difference
            target_Q_value = reward + gamma*np.max(Q_table[n_state][::]) - old_Q_value
        else:
            target_Q_value = reward
            
        # Update Q table with Q optimal
        Q_table[state][actions_list[action]] = old_Q_value + (learning_rate *target_Q_value) 
            
        state = n_state
        
        epsilon -= decay
        episode_reward += reward
      
        
    reward_track.append(episode_reward)
    print(f"Episode: {epi} | Epsilon : {epsilon}| Episode Reward: {episode_reward}")
          
np.save("Q_Table.npy", Q_table)
np.save("Reward_Data.npy", reward_track, allow_pickle=True)       
plt.figure(figsize=(15,8), dpi=150)       
plt.plot(reward_track)
plt.title("Accumulative Training Reward Per 500 Steps ", fontsize=20)
plt.ylabel("Mean Reward", fontsize=20)
plt.xlabel("Episodes", fontsize=20)
plt.legend(["Learning Curve"], fontsize=20, loc='upper left')
plt.savefig("learning_Curve_1.png")
#plt.show()

