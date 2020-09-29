import sys
import glob
import dpll

def get_input():
    user_input = input()

    while(user_input[0] == 'c'):
        user_input = input()

    _, _, nbvar, nbclauses = user_input.split()
    nbvar = int(nbvar)
    nbclauses = int(nbclauses)

    symbols = [i for i in range(1, nbvar+1)]
    assignments = [None] * nbvar
    clauses = [None] * nbclauses

    for i in range(nbclauses):
        user_input = input() 
        clauses[i] = [int(i) for i in user_input.split()[:-1]]

    return symbols, assignments, clauses

if len(argv) != 2:
    print("Usage: run.py dir/")
    print("`dir/` should be a directory containing properly formatted .cnf formula files")
formulas_to_solve = glob.glob(sys.argv[1]+"*.cnf")