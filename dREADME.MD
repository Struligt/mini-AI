can run individual tests: python grader.py 3a-basic

Q1a & b : did by hand and then redid in code (see scrap_MDP.py). Convergence is quite quick (about 10 iterations).

Q2a: counterexample : DONE
	counterexample shown in which negative rewards exist when taking intended action and positive rewards otherwise give the counterexample : ie the Vopt increases when noise is introduced. 
	FFI (for further investigation) : changing other params of hte MDP (eg symmetry of rewards, endstate_rewards, etc)

Q2b: if acyclical MDP, then Vopt at each node easier. Use memoization and a knapsack-like dynamic programming solution for calculating Vopt: ie use base-case of Vopt(endState) = 0, and recursive-relation Vopt(s) = max { sum over s' of T*(R+disc*Vopt(s')) }
- ie. for each end state , calculate best action to get to that end state. Then recurse backward. Either use recursion with memoization (memoize if the Vopt(s') not seen before, or else bottom-up approach of working backwards in the DAG from endState).

Q2c. easy : T*(R+disc*Vopt(s')) = T*disc*(R/disc+1*Vopt(s')) = T'*(R'+1*Vopt(s'))

Q3. fine but long. Good use of control abstraction makes the code super-readable, easier-to-code.


	