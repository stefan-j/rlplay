import numpy as np
import tensorflow as tf
import gym

epsilon = 0.1
gamma = 0.9

env = gym.make('CartPole-v0')


state_inp = tf.placeholder('float', [None, 4])
layer1 = tf.layers.dense(inputs=state_inp, units=100, activation=tf.nn.relu)
layer2 = tf.layers.dense(inputs=layer1, units=50, activation=tf.nn.relu)
layer3 = tf.layers.dense(inputs=layer2, units=20, activation=tf.nn.relu)
layer4 = tf.layers.dense(inputs=layer3, units=10, activation=tf.nn.relu)
out = tf.layers.dense(inputs=layer4, units=2, activation=None)
targ_inp = tf.placeholder('float', [None,1])
act = tf.placeholder('float', [None,2])
loss = tf.nn.l2_loss(targ_inp - tf.multiply(out,act) )
optim = tf.train.AdamOptimizer(0.001).minimize(loss)

actions = [0,1]

sess = tf.Session()
sess.run(tf.global_variables_initializer())

rr = 0
for i in range(0,200000):
    obs = env.reset()
    total = 0
    alpha = 0.5*(0.1 + (1.0/((i/100.0)+1.0)))
    while True:

        a = 0
        if np.random.uniform() < epsilon:
            a = env.action_space.sample()
        else:
            a = sess.run(out, feed_dict={state_inp: [obs]} )[0]
            a = np.argmax( a )
        if epsilon > 0 and rr > 50: epsilon *= 0.9999999

        obs_new,reward,done,info =  env.step(a)
        total += reward
   
        o = sess.run(out, feed_dict={state_inp: [obs_new]})
        best_q  = np.max( o[0] )
        target = reward + gamma*best_q # for next state !
        if done:
            target = reward
   
        act_vec = np.zeros(2)
        act_vec[a] = 1
        # print('a',a)
        sess.run(optim, feed_dict={targ_inp: [[target]], state_inp: [obs], act: [act_vec]})
        # sess.run(optim, feed_dict={targ_inp: [[targ_inp]], state_inp: [obs], act: [act_vec]})
    
        obs = obs_new
        if done: break
    rr = 0.99*rr + 0.01*total
    if i % 10 == 0: print("iteration %d avg rew %d epsilon %f" % (i,rr,epsilon))

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
