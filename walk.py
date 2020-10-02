import random
import copy

def _apply(clauses, ref_clauses, assignments):
    for i, clause in enumerate(ref_clauses):
        for j, symbol in enumerate(clause):
            if symbol < 0:
                clauses[i][j] = not assignments[abs(symbol)-1]
            else: 
                clauses[i][j] = assignments[abs(symbol)-1]

def _find_max_symbol(clause, clauses, ref_clauses, assignments):
    max_clauses_matched = 0
    for symbol in clause:
        # Flip the symbol
        assignments[abs(symbol)-1] = not assignments[abs(symbol)-1]
        _apply(clauses, ref_clauses, assignments) 
        # Test how many clauses are satisfied 
        clause_status = [any(clause) for clause in clauses]
        clauses_matched = [status for status in clause_status if status == True]
        if len(clauses_matched) >= max_clauses_matched:
            max_clauses_matched = len(clauses_matched)
            max_symbol = symbol
        # Flip it back
        assignments[abs(symbol)-1] = not assignments[abs(symbol)-1]  
    return max_symbol

def walk(symbols, clauses, p, max_flips):
    ref_clauses = copy.deepcopy(clauses)
    max_clauses_matched = 0
    # Set initial assignment to random
    assignments = [bool(random.getrandbits(1)) for symbol in symbols]
    # Start making assignments
    for i in range(max_flips):
        _apply(clauses, ref_clauses, assignments)
        clause_status = [any(clause) for clause in clauses]
        clauses_matched = [status for status in clause_status if status == True]
        if len(clauses_matched) > max_clauses_matched:
            max_clauses_matched = len(clauses_matched)
        # Check if satisfiability is reached
        if all(clause_status):
            return True, assignments, max_clauses_matched, i
        # Chose a random false clause
        # print(assignments)
        false_clauses = [clause for i, clause in enumerate(ref_clauses) if any(clauses[i]) == False]
        flip_clause = random.choice(false_clauses)
        # print(flip_clause)
        # Occasionally, flip a random symbol in the false clause
        if random.random() < p:
            flip_symbol = random.choice(flip_clause)
            assignments[abs(flip_symbol)-1] = not assignments[abs(flip_symbol)-1] 
        # Otherwise choose the optimal assignment
        else:
            # Test which symbol satisfies most clauses
            test_assign = copy.deepcopy(assignments)
            test_clauses = copy.deepcopy(clauses)
            flip_symbol = _find_max_symbol(flip_clause, test_clauses, ref_clauses, test_assign)
            assignments[abs(flip_symbol)-1] = not assignments[abs(flip_symbol)-1] 
        # print(flip_symbol)
    return  False, None, max_clauses_matched, max_flips

# Provide a filename to log the recursion depth and clauses satisfied values
# If not filename is provided, all logging is printed to stdout
if __name__ == "__main__":
    import sys
    if(len(sys.argv) == 1):
        print("Usage: `walk.py prop max_flips [optional logfile]`")
        quit()

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
        
    # Set random probability
    p = float(sys.argv[1])
    max_flips = int(sys.argv[2])
    # Special thanks to Stack Abuse for teaching me the stdout swap technique
    # Jacob Stopak, https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
    original_stdout = sys.stdout
    if(len(sys.argv) > 3):
        f = open(sys.argv[3], 'w')
        sys.stdout = f
    random.seed(1)
    sat, assignments, max_clauses, flips = walk(symbols, clauses, p, max_flips)
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