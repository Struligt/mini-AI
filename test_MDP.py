from submission import *
import util

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
    solver = util.ValueIteration() #algorithm instantiated
    solver.solve(mdp) #algo applied to the MDP problem
    print "Vopt : %s " %solver.V
    print "optimal_policy : %s " %solver.pi
    print("... done test_util.\n")

def eg_Q2a():
    print("Attempting counterexample Q2a : ")
    print ("... manually toggle noise param in class definition...")
    mdp = CounterexampleMDP()
    mdp.n=2
    # for _s in range(-mdp.n,mdp.n+1):
    #     for a in mdp.actions(_s):
    #         print "from state : %s, action = %s, edges : %s " %(_s, a, mdp.succAndProbReward(_s,a))
    solver = util.ValueIteration() #algorithm instantiated
    solver.solve(mdp) #algo applied to the MDP problem
    print "Vopt : %s " %solver.V
    print "optimal_policy : %s " %solver.pi
    print("... done test_util.\n")

def main():
    print("\nCS221 A4: MDP (optimal policy and value) submission.py testing :\n")
    # test_util()
    # solve_Q1()
    eg_Q2a()



if __name__ == '__main__':
  main()