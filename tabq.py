import numpy as np
import tensorflow as tf
import gym

epsilon = 0.1
gamma = 0.9

env = gym.make('CartPole-v0')
table = {}

def get(s,a):
    if not (s,a) in table:
        table[(s,a)] = 0
    return table[(s,a)]

def ro(val):
    level = 5.0
    return float(int(val*level)/level)
def discretize(s):
    return tuple([ro(o) for o in s])


actions = [0,1]

rr = 0
for i in range(0,200000):
    obs = env.reset()
    s = discretize(obs)
    total = 0
    alpha = 0.5*(0.1 + (1.0/((i/100.0)+1.0)))
    while True:

        a = 0
        if np.random.uniform() < epsilon:
            a = env.action_space.sample()
        else:
            a = np.argmax( [ get(s,ap) for ap in actions ] ) 
        if epsilon > 0 and rr > 50: epsilon *= 0.9999999

        obs,reward,done,info =  env.step(a)
        total += reward
        sp = discretize(obs)
    
        best_q  = max( [ get(sp,ap) for ap in actions ] ) 
        target = reward + gamma*best_q
        if done:
            target = reward
    
        # update table
        get(s,a) # touch
        table[(s,a)] = (1.0-alpha) * table[(s,a)] + alpha*target
    
        s = sp
        if done: break
    rr = 0.99*rr + 0.01*total
    if i % 100 == 0: print("iteration %d avg rew %d epsilon %f" % (i,rr,epsilon))

raw_input("Press any key to play")
obs = env.reset()
s = discretize(obs)
while True:
    env.render()
    a = np.argmax( [ get(s,ap) for ap in actions ] ) 
    obs,reward,done,info = env.step(a)
    sp = discretize(obs)
    s = sp
    if done: break
