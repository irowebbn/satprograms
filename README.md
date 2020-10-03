SAT Programs
CS 463G Artificial Intelligence
University of Kentucky Fall 2020

From assignment: "This assignment uses several heuristic search techniques to
find possibly optimal truth assignments for variables in the given Boolean
formulas"

# README
If you want to save a lot of computation, analysis of results obtained from
running all the formulas in `test` have been placed in the `results` directory.
At the top level, there are comma separated files containing the output summary
for each test run, including input file name, the number of symbols and clauses,
whether the algorithm found it to by satisfiable, the number of clauses
satisfied if the formula was not satisfied, and the runtime. A comparison of the
algorithm's performances, with plots, is provided in `summary_data.xlsx`. Images
of the plots for each algorithm are provided in the corresponding subfolder of
`results`. These subfolders also contain a zip of logs for each run over time,
and 2 video files visualizing the solving process of the algorithm, one for an
easy satisfiable formula, and one for an easy unsatisfiable one (the WalkSAT and
Simulated Annealing are cut short because 50,000 flips took too long to
animate). The code for generating these animations is also provided.
Unfortunately, detailed run logs were not collected for WalkSAT, but the summary
data and the visualizations are still available.

`run.py`: Test driver for all 3 algorithms. Set the variables `RUN_DPLL`,
`RUN_WALK`, and `RUN_SAT` to True or False to determine if they will run. The
driver runs the algorithm for each formula in the test set. For randomness-based
algorithms (WalkSAT and Simulated Annealing), each formula is run 10 times.
Start the  driver with `python run.py dir`, where `dir` is a directory
containing `.cnf` files with the candidate formulas. Log files will be stored in
the `logs` directory, sorted by algorithm used. 

`dpll.py`: An implementation of the Davis-Putnam-Logemann-Loveland algorithm.
Based off of pseudocode in Figure 7.17 on page 266 of *Artificial Intelligence:
A Modern Approach* (3rd ed) by Stuart J. Russell and Peter Norvig. No special
optimizations are applied.

`walk.py`: An implementation of the WalkSAT algorithm as described in Figure
7.18 on page 277 of Russell and Norvig. No special optimizations are applied.
The probability value is set at 0.5, simply because it was the number discussed
in class. More investigation is needed to determine what the optimal value for
this is, but there was not enough time to design any systematic test of this
parameter.

`sa.py`: A simulated annealing implementation as described in Figure 4.5 on page
127 of Russell and Norvig. The cooling rate is user-set, but for these tests I
set the temperature to 0.999 times the previous iteration's temperature. This
was set based on some simple informal tests to see which cooling rate allowed
some of the hard but satisfiable formulas to be solved within the maximum flip
bounds. 

Since the WalkSAT and Simulated Annealing algorithms are not complete, they will
terminate after a predetermined number of attempts if a solution is not found.
The current value of 50,000 is set such that WalkSAT is able to find all
satisfiable solutions in the test set. Simulated annealing terminates on a number
of satisfiable solution, indicating that improvements may be needed in the 
cooling schedule.

The python `multiprocessing` library is used to parallelize each formula run.

# Learning outcomes

1. Completeness in DPLL is nice, but it is very slow! It was helpful to be able
   to definitively know when a case was unsatisfiable, because the other
   algorithms would often waste computation time with no progress toward the
   solution until they hit their limit. However, the average solved case took
   909 seconds to solve with DPLL, while only taking 14 seconds with WalkSAT and
   9 seconds with simulated annealing.
2. WalkSAT is incredibly effective. My implementation of WalkSAT was able to
   find a satisfiable solution if it existed in 1575 out of 1670 cases run, or
   ~94% of the time. As noted above, it did this in a fraction of the time that
   DPLL took. I believe that increasing the max flips to 100,000 would allow
   WalkSat to reach 100% of the satisfiable case based on tests with the
   "hardest" formulas as measured by DPLL, but I chose to reduce the max flips
   for the full-scale test as it significantly improved overall runtime by
   reducing the wait for unsatisfiable cases, while only reducing the
   effectiveness by a small amount.
3. The cooling schedule for simulated annealing is tricky. With the parameters
   listed, satisfiable solutions were only found if they existed ~37% of the
   time. This includes finding solutions for some "hard" cases quickly, while
   missing easier ones. In my testing with many of the harder cases, I could
   reach a solution by slowing down the cooling, but most times I could see that
   the solving reached a local extrema fairly early on in the run and remained
   stuck, suggesting that cooling still happened too rapidly. I thought that the
   exponential component of the decrease would keep at least enough randomness
   long time into the run, but it appears that coupled with the exponential
   probability, there was virtually no randomness after a few thousand flips. It
   also seems like the randomness decreased too quickly at the beginning, which
   could not be overcome by randomness later in the run. If I had more time, I
   would consider testing a linear or geometric cooling schedule.
