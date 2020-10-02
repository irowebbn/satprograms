import random 
import math
import copy

def _apply(clauses, ref_clauses, assignments):
    for i, clause in enumerate(ref_clauses):
        for j, symbol in enumerate(clause):
            if symbol < 0:
                clauses[i][j] = not assignments[abs(symbol)-1]
            else: 
                clauses[i][j] = assignments[abs(symbol)-1]

def update_temp(temp, cool_rate):
    return temp * cool_rate
    
def sa(symbols, clauses, max_flips, cool_rate):
    ref_clauses = copy.deepcopy(clauses)
    max_clauses_matched = 0
    # Set initial assignment to random
    assignments = [bool(random.getrandbits(1)) for symbol in symbols]
    _apply(clauses, ref_clauses, assignments)
    temp = 1
    for t in range(max_flips):
        clause_status = [any(clause) for clause in clauses]
        clauses_matched = len([status for status in clause_status if status == True])
        print(str(t) + ", " + str(clauses_matched))
        if clauses_matched > max_clauses_matched:
            max_clauses_matched = clauses_matched
        if all(clause_status):
            return True, assignments, max_clauses_matched, t
        temp = update_temp(temp, cool_rate)
        # Make a random change
        random_symbol = random.choice(symbols)
        assignments[abs(random_symbol)-1] = not assignments[abs(random_symbol)-1]
        _apply(clauses, ref_clauses, assignments)
        # See if it is closer to solution or not
        clause_status = [any(clause) for clause in clauses]
        clauses_delta = len([status for status in clause_status if status == True]) - clauses_matched
        # if it is, take it
        if clauses_delta > 0:
            continue
        # if not, take it occasionally
        else:
            if random.random() < math.exp(clauses_delta/temp):
                continue
            else:
                assignments[abs(random_symbol)-1] = not assignments[abs(random_symbol)-1]
                _apply(clauses, ref_clauses, assignments)
    return False, None, max_clauses_matched, max_flips

if __name__ == "__main__":
    import sys
    if(len(sys.argv) == 1):
        print("Usage: `sa.py max_flips cool_rate [optional logfile]`")
        quit()
    max_flips = int(sys.argv[1])
    cool_rate = float(sys.argv[2])

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

    # Special thanks to Stack Abuse for teaching me the stdout swap technique
    # Jacob Stopak, https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
    original_stdout = sys.stdout
    if(len(sys.argv) > 3):
        f = open(sys.argv[3], 'w')
        sys.stdout = f
    random.seed(1)
    sat, assignments, max_clauses, flips = sa(symbols, clauses, max_flips, cool_rate)
    if(sat):
        sys.stdout = original_stdout
        print(str(len(symbols)) + ", " + str(len(clauses)) +
             ", SATISFIABLE, " + str(max_clauses) + 
             ", " + str(flips))
    else:
        sys.stdout = original_stdout
        print(str(len(symbols)) + ", " + str(len(clauses)) + 
            ", CANNOT SATISFY IN MAX FLIPS, " + str(max_clauses) + 
            ", " + str(flips))