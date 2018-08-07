can run individual tests: python grader.py 3a-basic

Q1a & b : did by hand and then redid in code (see scrap_MDP.py). Convergence is quite quick (about 10 iterations).

Q2a: counterexample : DONE
	counterexample shown in which negative rewards exist when taking intended action and positive rewards otherwise give the counterexample : ie the Vopt increases when noise is introduced. 
	FFI (for further investigation) : changing other params of hte MDP (eg symmetry of rewards, endstate_rewards, etc)

Q2b: if acyclical MDP, then Vopt at each node easier. Use memoization and a knapsack-like dynamic programming solution for calculating Vopt: ie use base-case of Vopt(endState) = 0, and recursive-relation Vopt(s) = max { sum over s' of T*(R+disc*Vopt(s')) }
- ie. for each end state , calculate best action to get to that end state. Then recurse backward. Either use recursion with memoization (memoize if the Vopt(s') not seen before, or else bottom-up approach of working backwards in the DAG from endState).

Q2c. easy : T*(R+disc*Vopt(s')) = T*disc*(R/disc+1*Vopt(s')) = T'*(R'+1*Vopt(s'))

Q3a. fine but long. Good use of control abstraction makes the code super-readable, easier-to-code.

Q3b. design card game to maximize frequency of peaking : 
	# want to increase chances of busting so keep high cards, but not so much that optimal to stay
    # need to have lower cards that allow adding without busting

	# cardValues = [1,2,3,4,5,6,7,8,9,10,11,12,13] # attempting mincard << threshold < 2*max card
    # multiplicity = 4 #gave 2%, not 10% peek

    # cardValues = [1,2,3,4,9,10] # #gave 5.5%
    # multiplicity = 5 
 
    # cardValues = [1,2,3,4,9,10,13] # #gave 5.6%
    # multiplicity = 4 

    # cardValues = [2,3,4,8,10,13] # gave 6.0%
    # multiplicity = 4     

    cardValues = [1,5,21] # attempting mincard << threshold < 2*max card
    multiplicity = 6 #gave 8.4%     -->

    <!-- SUCCESS -->
    cardValues = [1,5,21] # attempting mincard << threshold < 2*max card
    multiplicity = 12 # SUCCESS  >= 10%

    print "cardValues = %s, mult = %" %(cardValues, multiplicity)

Q4a. implement QLearningAlgorithm.incorporateFeedback(), which should take an (s,a,r,s′) tuple and update self.weights according to the standard Q-learning update.