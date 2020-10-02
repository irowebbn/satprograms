import sys
import glob
import random
import multiprocessing
import time

import dpll
import walk
import sa

# Parse symbols and clauses from CNF INPUT
def get_input(filename):
    with open(filename , 'r') as file:
        user_input = file.readline()

        while(user_input[0] == 'c'):
            user_input = file.readline()

        _, _, nbvar, nbclauses = user_input.split()
        nbvar = int(nbvar)
        nbclauses = int(nbclauses)

        symbols = [i for i in range(1, nbvar+1)]
        assignments = [None] * nbvar
        clauses = [None] * nbclauses

        for i in range(nbclauses):
            user_input = file.readline() 
            clauses[i] = [int(i) for i in user_input.split()[:-1]]

    return symbols, assignments, clauses

# Test driver for DPLL
def run_dpll(formula):
    symbols, assignments, clauses = get_input(formula)
     # Special thanks to Stack Abuse for teaching me the stdout swap technique
    # Jacob Stopak, https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
    original_stdout = sys.stdout
    with open("./logs/"+str(formula)[:-4]+".log" , 'w') as log:
        sys.stdout = log
        max_recursion_depth = 0
        max_clauses_sat = 0
        max_list = [max_clauses_sat, max_recursion_depth]
        start_time = time.time()
        
        if(dpll.dpll(symbols, assignments, clauses, 0, max_list)):
            duration = time.time() - start_time
            sys.stdout = original_stdout
            print(str(formula) + ", " + str(len(symbols)) + ", " + 
                str(len(clauses)) + ", SATISFIABLE, " + str(max_list[0]) + 
                ", " + str(max_list[1]) + ", " + str(duration))
        else:
            duration = time.time() - start_time
            sys.stdout = original_stdout
            print(str(formula) + ", " + str(len(symbols)) + ", " + 
                str(len(clauses)) + ", UNSATISFIABLE, " + str(max_list[0]) + 
                ", " + str(max_list[1]) + ", " + str(duration))

# Test driver for WalkSAT
def run_walk(formula):
    symbols, assignments, clauses = get_input(formula)

    # Special thanks to Stack Abuse for teaching me the stdout swap technique
    # Jacob Stopak, https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
    original_stdout = sys.stdout
    if(len(sys.argv) > 3):
        f = open(sys.argv[3], 'w')
        sys.stdout = f
    start_time = time.time()
    sat, assignments, max_clauses, flips = walk.walk(symbols, clauses, p, max_flips)
    duration = time.time() - start_time
    if(sat):
        sys.stdout = original_stdout
        print(str(formula) + ", " + str(len(symbols)) + ", " + str(len(clauses)) +
             ", SATISFIABLE, " + str(max_clauses) + 
             ", " + str(flips) + ", " + str(duration))
    else:
        sys.stdout = original_stdout
        print(str(formula) + ", " + str(len(symbols)) + ", " + str(len(clauses)) + 
            ", CANNOT SATISFY IN MAX FLIPS, " + str(max_clauses) + 
            ", " + str(flips) + ", " + str(duration) )

# Test driver for Simulated Annealing
def run_sa(formula):
    symbols, assignments, clauses = get_input(formula)

    # Special thanks to Stack Abuse for teaching me the stdout swap technique
    # Jacob Stopak, https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
    original_stdout = sys.stdout
    if(len(sys.argv) > 3):
        f = open(sys.argv[3], 'w')
        sys.stdout = f
    start_time = time.time()
    sat, assignments, max_clauses, flips = sa.sa(symbols, clauses, max_flips, cool_rate)
    duration = time.time() - start_time
    if(sat):
        sys.stdout = original_stdout
        print(str(formula) + ", " + str(len(symbols)) + ", " + str(len(clauses)) +
             ", SATISFIABLE, " + str(max_clauses) + 
             ", " + str(flips) + ", " + str(duration))
    else:
        sys.stdout = original_stdout
        print(str(formula) + ", " + str(len(symbols)) + ", " + str(len(clauses)) + 
            ", CANNOT SATISFY IN MAX FLIPS, " + str(max_clauses) + 
            ", " + str(flips) + ", " + str(duration) )

# Main test driver
if __name__ == '__main__':
    RUN_DPLL = False
    RUN_WALK = False
    RUN_SA = True

    if len(sys.argv) != 2:
        print("Usage: run.py dir")
        print("`dir/` should be a directory containing properly formatted .cnf formula files")
        quit()

    # Set random probability for WalkSAT
    p = 0.5
    max_flips = 50000
    # Set cooling rate for Simulated Annealing
    cool_rate = 0.999

    formulas_to_solve = glob.glob(sys.argv[1]+"/*.cnf")
    with multiprocessing.Pool() as pool:
        if RUN_DPLL:
            pool.map(run_dpll, formulas_to_solve)
        if RUN_WALK:
            for _ in range(10):
                pool.map(run_walk, formulas_to_solve)
        if RUN_SA:
            for _ in range(10):
                pool.map(run_sa, formulas_to_solve)
    