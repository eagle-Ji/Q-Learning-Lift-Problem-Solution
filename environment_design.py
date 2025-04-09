import numpy as np 

MAX_CAPACITY = 3 
MAX_FLOORS = 4 
OPEN = 'open'
CLOSE = 'close'


        

      
class environment():
    def __init__(self):
        self.current_floor      = 0 
        self.next_floor         = 0
        self.lift_psngr_count   = 0 
        self.psngr_drop_floor   = np.array([None,None,None])
        self.door_state         = CLOSE
        self.psngr_count_floor  = [0,0,0,0]
        self.psngr_dropped_count = 0
        self.steps_in_env = 0
        
        self.action_space = ["UP", "DOWN", "WAIT", "PICKUP/DROPOFF"]
        
    def get_psngr(self):
        psngr_arriving = np.random.choice(a=[True,False],p=[0.2, 0.8]) # passenger arival with 20% probability
        if psngr_arriving:
            pass_at_floor = np.random.choice(a=[0,1,2,3],p=[0.2, 0.1, 0.2, 0.5]) # passenger arival at any floor with defined probabilities. 
            
            self.psngr_count_floor[pass_at_floor] += 1
        
    def reset(self): # Reset the sysetm after each episode is over that is 500 steps. 
        self.steps_in_env       = 0
        self.current_floor      = np.random.randint(0,4) 
        self.next_floor         = 0
        self.lift_psngr_count   = 0 
        self.door_state         = CLOSE
        self.psngr_count_floor  = [0,0,0,0]
        self.psngr_drop_floor   = np.array([None,None,None])
        self.get_psngr()
        state = str(self.current_floor) +str(self.next_floor)  +str(self.psngr_drop_floor[0])+str(self.psngr_drop_floor[1])+str(self.psngr_drop_floor[2])
        return state
        


    def step(self, action):
        remaining_capacity = 0
        reward = 0
        done = False
        self.psngr_dropped_count = 0
        #print("Current Action ==> ", action)
        if action == "UP":
            # -ve reward for waiting and passengers in the lift waiting for drop. 
            
            #reward -= 1*(self.lift_psngr_count + sum(self.psngr_count_floor))
            self.door_state = CLOSE
            if self.current_floor < 3:
                # Move up if the lift is not at the last floor 
                self.next_floor = self.current_floor + 1
            elif self.current_floor == 3: 
                # Don't move up if lift is at top floor
                self.next_floor = self.current_floor
                
        if action == "DOWN":
            # -ve reward for waiting and passengers in the lift waiting for drop. 
            
            #reward -= 1*(self.lift_psngr_count + sum(self.psngr_count_floor))
            self.door_state = CLOSE
            if self.current_floor > 0:
                # Move down if the lift is not at the bottom floor 
                self.next_floor = self.current_floor - 1
            elif self.current_floor == 0: 
                # Don't move down if lift is at bottom floor
                self.next_floor = 0 #self.current_floor
        if action == "WAIT":
            # -ve reward for waiting and passengers in the lift waiting for drop. 
            
            
            # Don't change the floor for wait action
            self.next_floor = self.current_floor
            self.door_state = CLOSE
        if action == "PICKUP/DROPOFF":
            #print(f"current_floor {self.current_floor}| psngr_count_floor : {self.psngr_count_floor[self.current_floor]} ")
            # open the door so that passenger for the paticular floor can leave or enter
            self.door_state = OPEN
            
            if self.door_state == OPEN:
                for ind, floor in enumerate(self.psngr_drop_floor): # Drop the passengers
                    if floor == self.current_floor: # if the floor matches with the current floor
                        self.lift_psngr_count -= 1
                        self.psngr_drop_floor[ind] = None
                        self.psngr_dropped_count += 1
                        
                   
                psngr_alredy_on_lift = self.lift_psngr_count       
                # Passenger Pick Up
                if (self.lift_psngr_count < MAX_CAPACITY): # Pick up only if the lift has capacity
                    
                    remaining_capacity = MAX_CAPACITY - self.lift_psngr_count # find the capacity of lift
                    if (remaining_capacity > self.psngr_count_floor[self.current_floor]): # if the capacity is more than the passengers present at the current floor
                        self.lift_psngr_count += self.psngr_count_floor[self.current_floor] # load all passengers at that floor
                        self.psngr_count_floor[self.current_floor] = 0 # remove loaded passengers from the floor
                        
                    else:  # if the capacity is less than the passengers present at a given floor
                        self.lift_psngr_count += remaining_capacity # load the passengers according to the remaining capacity
                        self.psngr_count_floor[self.current_floor] -= remaining_capacity # remove loaded passengers from the floor
                #print(f"current_floor {self.current_floor}| psngr_alredy_on_lift {psngr_alredy_on_lift} | After Pick up {self.lift_psngr_count}| psngr_dropped_count : {self.psngr_dropped_count}")
                if (psngr_alredy_on_lift < self.lift_psngr_count):
                    pngr_picked_count = self.lift_psngr_count - psngr_alredy_on_lift
                    #if psngr_alredy_on_lift == 0:
                    for cnt in range(pngr_picked_count): # Find Dropoff floor accordinhg to given probabilities. 
                        load_psnger = np.where(self.psngr_drop_floor == None)[0][0]
                        self.psngr_drop_floor[load_psnger] = np.random.choice(a=[0,1,2,3], p=[0.25,0.25,0.25,0.25])
                #print(f"current_floor {self.current_floor}| psngr_count_floor : {self.psngr_count_floor[self.current_floor]}" )
                # Allocate the reward +10 for each passenger droped        
                #reward += 10*self.psngr_dropped_count      
                    
                    #print(f"current_floor {self.current_floor}| psngr_count_floor : {self.psngr_count_floor[self.current_floor]}" )
                print(f"Current Floor {self.current_floor}| Passengers on Lift {psngr_alredy_on_lift} | After Pick up {self.lift_psngr_count}| Passengers Droped : {self.psngr_dropped_count}| Passengers at [f0,f1,f2,f3] : {self.psngr_count_floor}| Passengers Destination: {self.psngr_drop_floor}")
        
        #print(f"self.psngr_count_floor : {self.psngr_count_floor}| psngr_drop_floor : {self.psngr_drop_floor} ")
        if self.psngr_dropped_count > 0:    
            reward = (10*self.psngr_dropped_count) 
        if action != "PICKUP/DROPOFF":
            reward = (-1)*(self.lift_psngr_count + sum(self.psngr_count_floor))
        if self.steps_in_env < 200:
            self.get_psngr()
        self.steps_in_env += 1
        
        if self.steps_in_env >= 500: # Only 500 steps are allowed in one episode. 
            done = True
         
        state = str(self.current_floor) +str(self.next_floor)  +str(self.psngr_drop_floor[0])+str(self.psngr_drop_floor[1])+str(self.psngr_drop_floor[2])
        self.current_floor = self.next_floor
        #print("Reward --> ", reward)
        #print(state)
        
        return state, reward, done
        
        
        
        
        
        
"""
If you want to run training comment the following section. 
"""     

# Uncomment for environment testing  
Q_table = np.load("Q_Table.npy", allow_pickle=True)[()]
env = environment()
steps = 500
state = env.reset()
done = False
for i in range(steps):
    action = env.action_space[np.argmax(Q_table[state][::])]
    #action = np.random.choice(env.action_space)
    n_state, reward, done = env.step(action )
    print(f"Action   {action} |  Reward   {reward}")
    state = n_state
    #print(act)
    #print(env.current_floor)

 
