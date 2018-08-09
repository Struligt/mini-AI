from submission import *
import util
import statistics

# import numpy as np

def plotQL(mylist):
    import matplotlib.pyplot as plt
    
    fig = plt.figure()
    fig.add_axes()
    ax =  fig.add_subplot(111)
    counts = [i for i,_ in enumerate(mylist)]
    ax.plot(counts, mylist, color='lightblue', linewidth=3)
    plt.show()

def mdpsolve(mdp):
    solver = util.ValueIteration() #algorithm instantiated
    solver.solve(mdp) #algo applied to the MDP problem
    print "Vopt : %s " %solver.V
    print "optimal_policy : %s " %solver.pi
    # print("... done solving offline MDP.\n")

def test_util():
    print("Testing util module : ")
    print("...creating simple mdp instance ... ")
    mdp = util.NumberLineMDP() #instance of an MDP problem
    solver = util.ValueIteration() #algorithm instantiated
    solver.solve(mdp) #algo applied to the MDP problem
    print "Vopt : %s " %solver.V
    print "optimal_policy : %s " %solver.pi
    print("... done test_util.\n")

def solve_Q1():    
    class Q1(util.MDP):
        def __init__(self, n=2): self.n = n
        def startState(self): return 0
        def actions(self, state): return [-1, 1]
        def succAndProbReward(self, state, action):
            n = self.n
            def IsEnd(s):
                return s in [-n,+n]

            # generate reward lookup :
            reward_d = {-n: 20,n:100} #define reward for moving into end state
            for s in range(-n+1,n):
                reward_d[s] = -5 #reward for any other state
            
            if IsEnd(state): #starting state is an endState -> return empty list
                return []
            if action == -1:
                return [(state-1, 0.6, reward_d[state-1]), (state+1, 0.4, reward_d[state+1])]
            elif action == 1:
                return [(state-1, 0.8, reward_d[state-1]), (state+1, 0.2, reward_d[state+1])]
            else:
                print "Action is neither -1 or +1 ?!"
            # d: returns (newState, prob, reward) corresponding to edges of each action coming out of |state|.
        def discount(self): return 1.0

    print("Solving Q1 : ")
    print("...creating simple mdp instance ... ")
    mdp = Q1() #instance of an MDP problem
    for _s in range(-mdp.n,mdp.n+1):
        for a in mdp.actions(_s):
            print "from state : %s, action = %s, edges : %s " %(_s, a, mdp.succAndProbReward(_s,a))
    mdpsolve(mdp)


def eg_Q2a():
    print("Attempting counterexample Q2a : ")
    print ("... manually toggle noise param in class definition...")
    mdp = CounterexampleMDP()
    mdp.n=2
    # for _s in range(-mdp.n,mdp.n+1):
    #     for a in mdp.actions(_s):
    #         print "from state : %s, action = %s, edges : %s " %(_s, a, mdp.succAndProbReward(_s,a))
    mdpsolve(mdp)

def Q3_a_succprob():
    print("Testing Q3_a_succprob .... ")
    cardValues = [1,2,3]
    multiplicity = 1 
    threshold =  4
    peekCost = 1

    mdp = BlackjackMDP(cardValues, multiplicity, threshold, peekCost)
    s = mdp.startState()
    actions = mdp.actions(s) #['Take', 'Peek', 'Quit']
    testcases = [((3,None,(1,1,0)),'Quit'),
                ((0,None,(1,1,1)),'Peek'), ((0,None,(1,0,1)),'Peek'),((0,0,(1,0,1)),'Peek'),
                ((3,0,(1,1,0)),'Take'),((3,1,(1,1,0)),'Take'), #should bust 
                ((3,None,(1,1,0)),'Take'), #can either not or bust here
                ((3,None,(1,0,0)),'Take')#should return (4,None,None)
                ]
    # testi = 0
    # case = testcases[testi]
    # print "From state %s, %s --> %s " %(case[0], case[1], mdp.succAndProbReward(case[0], case[1]))
    for case in testcases:
        print "From state %s, %s --> %s " %(case[0], case[1], mdp.succAndProbReward(case[0], case[1]))
    
def Q3_a_solve():
    print("Trying to solve Q3_a_ .... ")
    cardValues = [1,2,3]
    multiplicity = 1 
    threshold =  4
    peekCost = 1

    mdp = BlackjackMDP(cardValues, multiplicity, threshold, peekCost)
    mdpsolve(mdp)

def Q4a_test():
    # create a dummy RL_algo:
    qla = QLearningAlgorithm(actions = lambda s : (-1,+1), 
        discount = 1, 
        featureExtractor = lambda s,a : [((s,a),1)], #dummy here; shud be a function that takes a state and action and returns a list of (feature name, feature value) pairs, in order to allow generalization
        explorationProb=0.2)

    qla.getAction(0)
    qla.incorporateFeedback(0, -1, -5, -2) #incorporateFeedback(state, action, reward, newState):
    qla.incorporateFeedback(0, -1, -5, None)

def Q4b():
    print "Comparing value iteration ag simulated Q-learning :"

    mdp = largeMDP
    numqtrials = 10
    print "...comparison for %s x %s MDP; Q-learning numtrials : %s" %(mdp.cardValues, mdp.multiplicity, numqtrials)
    
    # value iteration
    solver = util.ValueIteration() #algorithm instantiated
    solver.solve(mdp) #algo applied to the MDP problem
    
    # q-learning simulate :
    phi = identityFeatureExtractor
    rl = QLearningAlgorithm(actions = mdp.actions , discount=mdp.discount(), featureExtractor = phi, explorationProb=0.2)
    # simulate_QL_over_MDP(mdp, rl)
    totPVs = util.simulate(mdp, rl, numTrials=numqtrials, verbose = False) #returns list of totRewards for each trial
    # print " ........ totPVs : %s " %totPVs
    print " ........ # non-zero weights = %s" %sum([1 for k,v in rl.weights.items() if v])
    
    Vopt_est = max(rl.weights[(mdp.startState(),a)] for a in rl.actions(mdp.startState() ) )
    
    print "...Comparison of Vopt : "
    print " ... value iteration = expected optimal PV :: optimal utility of startState, stdev: ( %s, 0 )" %(solver.V[mdp.startState()])
    print " ... q-learning: avg PV :: utility, stdev over all trials: ( %s, %s ) (see note * below)" %(statistics.mean(totPVs), statistics.stdev(totPVs))
    print " ... q-learning: estimated optimal PV :: optimal utility of startState : ( %s, 0 )" %Vopt_est
    # plotQL(totPVs) 
    
    print "...Comparison of policies (rerun with explorationProb = 0) : "
    # rerun QL now with 0 exploration prob (since learned)
    rl.explorationProb = 0
    totPVs = util.simulate(mdp, rl, numTrials=numqtrials, verbose = False) #reruns simulation
    Vopt_est = max(rl.weights[(mdp.startState(),a)] for a in rl.actions(mdp.startState() ) )
    print " ... q-learning: estimated optimal PV :: optimal utility of startState : ( %s, 0 )" %Vopt_est
    print " ... # non-zero weights = %s" %sum([1 for k,v in rl.weights.items() if v])

    #sample weights :
    # s = mdp.startState()
    # print "weights for startState : %s" %{k:v for k,v in rl.weights.items() if k[0] == s}
    # print "--> vip = %s" %max((rl.weights[(s,a)],a) for a in rl.actions(s) )[1]
    
    diffs = 0 #counts number of differences in policy btw VI and QL
    for s,p in solver.pi.items() : # using value-iteration policy as starting point
        vip = max((rl.weights[(s,a)],a) for a in rl.actions(s) )[1]
        if vip != p :
            diffs += 1
    print "number of different policies btw VI and QL , out of total : %s / %s = %4.2f" %(diffs, len(solver.pi), diffs/(1.0*len(solver.pi)))
    # print(" \n *note: Q-learn utility does not converge to the MDP value-iteration, since for each trial, semi-random (epsilon-greedy) path taken, not opimal path. \
    # In order to compare apples-with-apples, need to calculate max over a (w*phi(s,a)) for startState, which is shown on next line. \n")


    

def main():
    print("\nCS221 A4: MDP (optimal policy and value) submission.py testing :\n")
    # test_util()
    # solve_Q1()
    # eg_Q2a()
    # Q3_a_succprob()
    # Q3_a_solve()
    # Q4a_test()
    Q4b()


if __name__ == '__main__':
  main()