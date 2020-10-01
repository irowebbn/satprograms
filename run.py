import sys
import glob
import multiprocessing
import dpll
import time

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

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: run.py dir")
        print("`dir/` should be a directory containing properly formatted .cnf formula files")

    formulas_to_solve = glob.glob(sys.argv[1]+"/*.cnf")
    with multiprocessing.Pool() as pool:
        pool.map(run_dpll, formulas_to_solve)
    