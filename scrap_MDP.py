#solves manually problem 1 of cs221 MDP assignment

import numpy as np #using linear algebra multiplication
from copy import copy



#define state space & transition probabilities
states = tuple(range(-2,3))
endstates = (-2,2)
endstatereward = {-2:20, 2:100 }
actions = (-1,1)
usualreward = -5
Tsa=np.array([[0.6,0.4], [0.8,0.2]]) #( [T(s,a=-1,s'=s-1),T(s,a=-1,s'=s+1)],[(T(s,a=+1,...))])

#create rewards table
rewards=copy(endstatereward)
for s in states:
    if s not in endstates:
        rewards[s]=usualreward

#initialize
disc = 1.0
Voptend = 0
Vopt_prev = {s:0 for s in states} #previous iterations V_opt(s)
Vopt0 = 0 #initial guess
aopt = {s:None for s in states}
Vopt = {s:Vopt0 for s in states}

#value iteration
iters = range(10) 
for iter in iters:
    for j,s in enumerate(states):
        if s in endstates:
            Vopt[s] = 0
        else:
            #calculate optimal action and associated value for each state:
            new_states = [s-1,s+1] #corresponding to actions [-1,+1]
            util_a = np.array([(rewards[_s]+disc*Vopt_prev[_s]) for _s in new_states])
            exputil_a = Tsa.dot(util_a)
            Vopt[s] = max(exputil_a)
            aopt[s] = actions[np.argmax(exputil_a)]
    #update for next iteration:
    Vopt_prev = {_s:Vopt[_s] for _s in states}
    aopt_prev = {_s:aopt[_s] for _s in states}
    # print results : 
    print "... iter %d : (s, Vopt, aopt) for each state : %s" %(iter, [(_s, Vopt[_s], aopt[_s]) for _s in states])
    
print "\nResult : (s, Vopt, aopt) for each state : %s \n" %([(_s, Vopt[_s], aopt[_s]) for _s in states])
print "OBS how aopt for s=-1 flips from a=+1 to a=-1 as the maximum reward of +100 bleeds into the expected utility of s=-1 as iterations increase. "
if all([aopt[_s] == aopt[states[1]] for _s in states if _s not in endstates]) :
    print "Optimal policy regardless of state is a = %s." %aopt[states[1]]
