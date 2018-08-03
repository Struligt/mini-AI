import util, math, random
from collections import defaultdict
from util import ValueIteration

############################################################
# Problem 2a

# If you decide 2a is true, prove it in blackjack.pdf and put "return None" for
# the code blocks below.  If you decide that 2a is false, construct a counterexample.

# d: if the inter-endstate moves give negative rewards, but moving to end_state gives a positive reward, then increasing 
# random jumps should allow "bleeding in" of the positive rewards, increasing the Vopt if only action is to stay in current state or 
#  quit the game. 
# similarly, another MDP game that would increase the Vopt when introducing noise , would be if a reward is given when a state (s+1) is moved to which is contrary to the action (-1) taken

class CounterexampleMDP(util.MDP):
    # Return a value of any type capturing the start state of the MDP.
    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return 0
        # raise Exception("Not implemented yet")
        # END_YOUR_CODE

    # Return a list of strings representing actions possible from |state|.
    def actions(self, state):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return [-1,1]
        # raise Exception("Not implemented yet")
        # END_YOUR_CODE

    # Given a |state| and |action|, return a list of (newState, prob, reward) tuples
    # corresponding to the states reachable from |state| when taking |action|.
    # Remember that if |state| is an end state, you should return an empty list [].
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        # raise Exception("Not implemented yet")
            def IsEnd(s):
                return s in [-n,+n]
            def mix_probs(oldprobl, noise = 0.5): #orig_probs gives mapping a : [non-zero prob of moving from state an increment]
                num_nzp = sum(p > 0 for p in oldprobl) #number of nonzero probabilities
                return [ (((1-noise)*p + noise/num_nzp) if p> 0 else 0) for p in oldprobl]
            def gen_reward(s_orig, s_new, a):
                if IsEnd(s_new):
                    return reward_d[s_new]
                elif a == (s_new - s_orig):  #change in state as intended by action
                    return -5
                else:
                    return 5
            
            # define graph (state and transition) space
            n = 2
            states = range(-n,n+1)
            reward_d = {-n: 0, n: 0} #define reward for moving into end state
            poss_transitions = {-1:[-1,1] , 1:[-1,1]} #action: transitions from current state given that action
            orig_pd = {-1:[0.99,0.01], 1:[0.01,0.99]}  #{a: P(s-1),P(s+1)} corresponding to the *actions* list
            # add noise:
            noise = 0.5 #TOGGLE THIS
            new_probs = mix_probs(orig_pd[action], noise)
            #check :
            if len(new_probs) != len(poss_transitions[action]) :
                print ("new_probs list doesnt match up with actions list!")
            
            # return results: 
            if IsEnd(state): #starting state is an endState -> return empty list
                return []
            # returns (newState, prob, reward) corresponding to edges of each action coming out of |state|.
            edges = []
            for i,trans in enumerate(poss_transitions[action]):
                edges.append(((state+trans),new_probs[i],gen_reward(state,state+trans,action)))
            return edges
        # END_YOUR_CODE

    # Set the discount factor (float or integer) for your counterexample MDP.
    def discount(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return 1.0
        # raise Exception("Not implemented yet")
        # END_YOUR_CODE


class CounterexampleMDP2(util.MDP):
    # another counterexample, though not sure this would be acceptable, as really there are no actions: regardless of action choice,
    # you get same transition states and associated probs
    def startState(self):
        return 1

    def actions(self, state):
        if state == 1:
            return [-1,1]
        return []

    def succAndProbReward(self, state, action):
        if state == 1:
            return [(0,.90,10),(2,.10,100)]
        return []

    def discount(self):
        return 1

############################################################
# Problem 3a

class BlackjackMDP(util.MDP):
    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: list of integers (face values for each card included in the deck)
        multiplicity: single integer representing the number of cards with each face value
        threshold: maximum number of points (i.e. sum of card values in hand) before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look closely at this function to see an example of state representation for our Blackjack game.
    # Each state is a tuple with 3 elements:
    #   -- The first element of the tuple is the sum of the cards in the player's hand.
    #   -- If the player's last action was to peek, the second element is the index
    #      (not the face value) of the next card that will be drawn; otherwise, the
    #      second element is None.
    #   -- The third element is a tuple giving counts for each of the cards remaining
    #      in the deck, or None if the deck is empty or the game is over (e.g. when
    #      the user quits or goes bust).
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be placed into the succAndProbReward function below.
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']

    # Given a |state| and |action|, return a list of (newState, prob, reward) tuples
    # corresponding to the states reachable from |state| when taking |action|.
    # A few reminders:
    # * Indicate a terminal state (after quitting, busting, or running out of cards)
    #   by setting the deck to None.
    # * If |state| is an end state, you should return an empty list [].
    # * When the probability is 0 for a transition to a particular new state,
    #   don't include that state in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 53 lines of code, but don't worry if you deviate from this)
        
        # state : (totalCardValueInHand, nextCardIndexIfPeeked, deckCardCounts)
        # eg 3-card 1,2,3 with multiplicity one: startState : (0,None,(1,1,1)) -> successor actions [take,peek, quit]
        # after peeking: s' : (0,1,(1,1,1)), cost = -peekCost -> successor actions [take,quit]
        # after taking : (2,None,(1,0,1)) deterministically 
        # after busting :  (2+3,None, None) (?? not (0,None,None)) or (2+3,None, None) cost = -(2+3)
        # after quitting : (2, None, None), cost = 0
        # if take last card,then return [(new totalCardValueInHand, None, *NONE* to indicate game done), prob=1, reward] :: quit 

        def IsEnd(s): #if state is an endState -> return empty list
                return s[2] is None

        def gen_nextc(s): #generate (index of next card to be dealt, associated probability)
            cc=s[2] #cardcount :: deck from which cards to be dealt : eg (1,0,1)
            totalcs = sum(cc)
            return [(i,numc/(1.0*totalcs))for i,numc in enumerate(cc) if numc]

        def cc_adjust(cc,ci): #adusts cardcount :: state[2] for card index ci taken : eg (1,1,1),1 -> (1,0,1)
            cc = list(cc)
            cc[ci] -= 1
            return tuple(cc)

        def calc_result(s,p): #gives result depending on if empty deck or busted or neither
            # if take last card,then return [(new totalCardValueInHand, None, *NONE* to indicate game done), prob, reward] :: quit 
            # if busted, then set s[2] :: deckcount = None
            if s[0] > self.threshold : #busted
                return ((s[0], None, None),p,0)
            elif all(numc == 0 for numc in s[2]): # if empty deck & not busted, then set deck -> None, reward -> valueHand
                return ((s[0],s[1],None),p,s[0])
            else:
                return (s,p,0)
            
        results =[]
        cardcount = state[2]
        # go thru the different cases :
        if IsEnd(state):
            return []
        if action == 'Take':
            if state[1] is not None: #ie previous action was peeked, in which case card known
                nextState = (state[0]+self.cardValues[state[1]],
                                None,
                                cc_adjust(cardcount,state[1]))
                return [calc_result(nextState,1)]
            else: #next card unknown
                for nextci, prob in gen_nextc(state):
                        nextState = (state[0]+self.cardValues[nextci], 
                                        None, 
                                        cc_adjust(cardcount,nextci))
                        results.append(calc_result(nextState,prob))
                return results
        
        elif action == 'Quit' :
            return [((state[0], state[1], None),1,state[0])]

        elif action == 'Peek':
            if state[1] is not None: #you peeded before ...
                return [] # if the player peeks twice in a row, then succAndProbReward() should return []    
            else:
                for nextci, prob in gen_nextc(state):
                    nextState = (state[0], nextci, state[2])
                    results.append((nextState,prob,-self.peekCost))
                return results
        # raise Exception("Not implemented yet")
        # END_YOUR_CODE

    def discount(self):
        return 1

############################################################
# Problem 3b

def peekingMDP():
    """
    Return an instance of BlackjackMDP where peeking is the
    optimal action at least 10% of the time.
    """
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE

############################################################
# Problem 4a: Q learning

# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAlgorithm(util.RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

# Return a single-element list containing a binary (indicator) feature
# for the existence of the (state, action) pair.  Provides no generalization.
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

############################################################
# Problem 4b: convergence of Q-learning
# Small test case
smallMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# Large test case
largeMDP = BlackjackMDP(cardValues=[1, 3, 5, 8, 10], multiplicity=3, threshold=40, peekCost=1)

def simulate_QL_over_MDP(mdp, featureExtractor):
    # NOTE: adding more code to this function is totally optional, but it will probably be useful
    # to you as you work to answer question 4b (a written question on this assignment).  We suggest
    # that you add a few lines of code here to run value iteration, simulate Q-learning on the MDP,
    # and then print some stats comparing the policies learned by these two approaches.
    # BEGIN_YOUR_CODE
    pass
    # END_YOUR_CODE


############################################################
# Problem 4c: features for Q-learning.

# You should return a list of (feature key, feature value) pairs.
# (See identityFeatureExtractor() above for a simple example.)
# Include the following features in the list you return:
# -- Indicator for the action and the current total (1 feature).
# -- Indicator for the action and the presence/absence of each face value in the deck.
#       Example: if the deck is (3, 4, 0 , 2), then your indicator on the presence of each card is (1,1,0,1)
#       Note: only add this feature if the deck is not None.
# -- Indicators for the action and the number of cards remaining with each face value (len(counts) features).
#       Note: only add these features if the deck is not None.
def blackjackFeatureExtractor(state, action):
    total, nextCard, counts = state

    # BEGIN_YOUR_CODE (our solution is 8 lines of code, but don't worry if you deviate from this)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE

############################################################
# Problem 4d: What happens when the MDP changes underneath you?!

# Original mdp
originalMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# New threshold
newThresholdMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=15, peekCost=1)

def compare_changed_MDP(original_mdp, modified_mdp, featureExtractor):
    # NOTE: as in 4b above, adding more code to this function is completely optional, but we've added
    # this partial function here to help you figure out the answer to 4d (a written question).
    # Consider adding some code here to simulate two different policies over the modified MDP
    # and compare the rewards generated by each.
    # BEGIN_YOUR_CODE
    pass
    # END_YOUR_CODE

