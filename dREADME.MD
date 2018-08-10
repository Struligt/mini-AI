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

- 

Q4b. Comparison of Value-Iteration and Q-Learning results. 

    For generalization of QL (ie Qˆopt (s,a) := w*phi(s,a) where phi, as in ML, extracts features - eg PCA - of (s,a) pair, returning a vector of features - eg (0 0 0 1 0 1 0 ..) - present ). Here, used the non-generalzing identityFeatureExtractor(state, action) whose featurekey is (state,action). Therfore, in this case, each w is paired with each (s,a) and so w = Qopt(s,a) providing no generalization. 

    Observed : 


	- Q-learn utility does not converge to the MDP value-iteration, since for each trial, semi-random (epsilon-greedy) path taken, not opimal path. In order to compare apples-with-apples, need to calculate max over a ( Qopt(s,a) = w*phi(s,a)) for startState.
	- Each trial ends when you reach endState, so you need lots of trials to explore entire state, action space
	- As numtrials increase, more weights are updated, & estimated Vopt converges on the value-iteration Vopt.
	- For low numtrials, potentially lots of state, action combos unexplored, so therefore many weights potentially unupdated. This disappears as numtrials increases. 
	- As complexity of problem increases (smallMDP -> largeMDP), the state,action space increases (exponentially here), and discrepancy btw VI and QL will reappear, requiring furhter increases in numtrials.
    - Vopt estimate always converges to Vopt as numtrials increase. Estimated optimal policy should converge but may not do so monotonically (since depends on paths taken)

    ... data :
    MDP problem         numtrials       policy difference        Vopt diff          Comments
    -----------         ---------       -----------------        ---------          ---------
    smallMDP                10            0.21 = 8/38 different      -50%
    ""                      30000         0                           -1%                             
    largeMDP                10            800/3000 = 0.26            -99%           
    ""                      30000         850/3000 = 0.29            -80%
    ""                      300000        1070/3000 = 0.36           -50%           *not sure why policy diff inc'd
    largeMDP with featExt   30000          650/3000 = 0.20            -4%          feat-extr to generalize very impt!!




Q4c. Using a better feature extractor. 

    Now coding a feature extractor which enables some generalization - aka reduction in dimension of our weights. The feature extractor returns a list of (feature_key,feature_value) pairs, with , in this case, feature_key where the calculation goes, and feature_value simply being binary indicating presecence (0 by default to indicate doesn't have). 

    ?Why not make featureExtractor value being non-binary : eg initially thought about returning (action, card_index) feature_key giving feature_value = number of cards of card_index in deck.

    Why not have featureExtractor include if you ve peeked or not ? - added this, and it improved score somewhat but not .


    Further investigation - some policy differences arise when deck is None, whereupon VI says optimal is to take (& get reward) whereas RL says Quit ?!

Q4d. What happens when the MDP changes underneath you?!

