# README

`run.py`: Test driver for all 3 algorithms. Set the variables RUN_DPLL,
RUN_WALK, and RUN_SAT to True or False to determine if they will run. The driver
runs the algorithm for each formula in the test set. For randomness-based
algorithms (WalkSAT and Simulated Annealing), each formula is run 10 times.

`dpll.py`: An implementation of the Davis-Putnam-Logemann-Loveland algorithm.
Based off of pseudocode in Figure 7.17 on page 266 of *Artificial Intelligence:
A Modern Approach* (3rd ed) by Stuart J. Russell and Peter Norvig.

`walk.py`: An implementation of the WalkSAT algorithm as described in Figure
7.18 on page 277 of Russell and Norvig

`sa.py`: A simulated annealing implementation as described in Figure 4.5 on page
127 of Russell and Norvig

Since the WalkSAT and Simulated Annealing algorithms are not complete, they will
terminate after a predetermined number of attempts if a solution is not found.
The current value of 50,000 is set such that WalkSAT is able to find all
satisfiable solutions in the test set. Simulated annealing terminates on a number
of satisfiable solution, indicating that improvements may be needed in the 
cooling schedule.