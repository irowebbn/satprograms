# Uses CNF input as described here: 
# http://www.satcompetition.org/2011/format-benchmarks2011.html

import copy
import math

def get_assignment(symbol, assignments):
    value = assignments[abs(symbol)-1]
    if (symbol > 0 and value == True) or (symbol < 0 and value == False):
        return True
    elif(symbol > 0 and value == False) or (symbol < 0 and value == True):
        return False
    else: 
        return None

def set_assignment(value, symbol, assignments):
    if symbol < 0:
        assignments[abs(symbol)-1] = not value
        return
    else:
        assignments[symbol-1] = value
        return

def reduce(assignments, clauses):
    reduced_clauses = copy.deepcopy(clauses)
    for i, clause in enumerate(clauses):
        if clause != [True]:
            for symbol in clause:
                # Check if symbols in clause have been assigned values
                value = get_assignment(symbol, assignments)
                if value != None:
                    # If the symbol is True, we can set the whole clause to true
                    if value == True:
                        reduced_clauses[i] = [True]
                        break
                    # If the symbol is False, then we can drop it from the clause
                    if value == False:
                        reduced_clauses[i].remove(symbol)
    return reduced_clauses

def find_pure_symbols(symbols, assignments, clauses):
    pure_symbols = []
    
    for symbol in symbols:
        # We don't have to check for symbols that have an assignment
        if get_assignment(symbol, assignments) != None:
            continue
        seen_positive = False
        seen_negative = False
        for clause in clauses:
            if clause != [True]:
                for instance in clause:
                    # When we see a symbol, record whether it was negated or not
                    if symbol == instance:
                        seen_positive = True
                        break
                    if symbol == -instance:
                        seen_negative = True
                        break
                # If we say both normal and negated versions of the symbol,
                # it is not a pure literal
                if seen_positive and seen_negative:
                    break
        if seen_positive ^ seen_negative:
            pure_symbols.append(symbol)
            set_assignment(True, int(math.pow(-1, seen_negative)*symbol), assignments)
    return pure_symbols  


def find_unit_clauses(symbols, assignments, clauses):
    unit_clause_symbols = []
    for clause in clauses:
        if clause != [True] and len(clause) == 1:
            set_assignment(True, clause[0], assignments)
            unit_clause_symbols.append(clause[0])
    return unit_clause_symbols

def dpll(symbols, assignments, clauses, recursion_depth):
    updated_assignments = copy.deepcopy(assignments)
    # Check if all clauses are already true
    if all([clause == [True] for clause in  clauses]):
        return True
    if any([clause == [] for clause in clauses]):
        return False
    pure_symbols = find_pure_symbols(symbols, updated_assignments, clauses)
    if len(pure_symbols) > 0:
        reduced_clauses = reduce(updated_assignments, clauses)
        return dpll(symbols, updated_assignments, reduced_clauses, recursion_depth+1)
    unit_clauses = find_unit_clauses(symbols, updated_assignments, clauses)
    if len(unit_clauses) > 0:
        reduced_clauses = reduce(updated_assignments, clauses)
        return dpll(symbols, updated_assignments, reduced_clauses, recursion_depth+1)
    guess_symbol = next(symbol for symbol in symbols if get_assignment(symbol, updated_assignments) == None)
    guess_true = updated_assignments[0:guess_symbol-1] + [True] + updated_assignments[guess_symbol:]
    guess_false = updated_assignments[0:guess_symbol-1] + [False] + updated_assignments[guess_symbol:] 
    return dpll(symbols, guess_true, reduce(guess_true, clauses), recursion_depth+1) \
        or dpll(symbols, guess_false, reduce(guess_false, clauses), recursion_depth+1)


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

if(dpll(symbols, assignments, clauses, 0)):
    print("SATISFIABLE")
else:
    print("UNSATISFIABLE")