# Uses CNF input as described here: 
# http://www.satcompetition.org/2011/format-benchmarks2011.html

import copy
import math

# Given a symbol, get its assigned value
def _get_assignment(symbol, assignments):
    value = assignments[abs(symbol)-1]
    if (symbol > 0 and value == True) or (symbol < 0 and value == False):
        return True
    elif(symbol > 0 and value == False) or (symbol < 0 and value == True):
        return False
    else: 
        return None

# Update the assignment list for a symbol
def _set_assignment(value, symbol, assignments):
    if symbol < 0:
        assignments[abs(symbol)-1] = not value
        return
    else:
        assignments[symbol-1] = value
        return

# Reduce the clauses using the updated assignment list
def _reduce(assignments, clauses):
    reduced_clauses = copy.deepcopy(clauses)
    for i, clause in enumerate(clauses):
        # We have to check the type because we could have a unit clause [1]
        # that evaluates to [True]
        if type(clause[0]) != type(True):
            for symbol in clause:
                # Check if symbols in clause have been assigned values
                value = _get_assignment(symbol, assignments)
                if value != None:
                    # If the symbol is True, we can set the whole clause to true
                    if value == True:
                        reduced_clauses[i] = [True]
                        break
                    # If the symbol is False, then we can drop it from the clause
                    if value == False:
                        reduced_clauses[i].remove(symbol)
    return reduced_clauses

# Set to true any symbols that are never negated
# Set to false any symbols that are always negated
def _find_pure_symbols(symbols, assignments, clauses):
    pure_symbols = []
    for symbol in symbols:
        # We don't have to check for symbols that have an assignment
        if _get_assignment(symbol, assignments) != None:
            continue
        seen_positive = False
        seen_negative = False
        for clause in clauses:
            # We have to check the type because we could have a unit clause [1]
            # that evaluates to [True]
            if type(clause[0]) != type(True):
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
            _set_assignment(True, int(math.pow(-1, seen_negative)*symbol), assignments)
    return pure_symbols  


def _find_unit_clauses(symbols, assignments, clauses):
    unit_clause_symbols = []
    for clause in clauses:
        # We have to check the type because we could have a unit clause [1]
        # that evaluates to [True]
        if (type(clause[0]) != type(True)) and len(clause) == 1:
            _set_assignment(True, clause[0], assignments)
            unit_clause_symbols.append(clause[0])
    return unit_clause_symbols


def dpll(symbols, assignments, clauses, recursion_depth):
    clauses_matched = len([clause for clause in clauses if len(clause) != 0 and type(clause[0]) == type(True)])
    print(str(recursion_depth) + ", " + str(clauses_matched))
    updated_assignments = copy.deepcopy(assignments)
    # Check if all clauses are already true
    if all([clause == [True] for clause in  clauses]):
        return True
    # Check if we hit an an unsatisfiable branch
    if any([clause == [] for clause in clauses]):
        return False
    # Propagate pure literals and unit clauses
    pure_symbols = _find_pure_symbols(symbols, updated_assignments, clauses)
    if len(pure_symbols) > 0:
        reduced_clauses = _reduce(updated_assignments, clauses)
        return dpll(symbols, updated_assignments, reduced_clauses, recursion_depth+1)
    unit_clauses = _find_unit_clauses(symbols, updated_assignments, clauses)
    if len(unit_clauses) > 0:
        reduced_clauses = _reduce(updated_assignments, clauses)
        return dpll(symbols, updated_assignments, reduced_clauses, recursion_depth+1)
    # Branch to try both the positive and negative assignment of the next unassigned symbol
    guess_symbol = next(symbol for symbol in symbols if _get_assignment(symbol, updated_assignments) == None)
    guess_true = updated_assignments[0:guess_symbol-1] + [True] + updated_assignments[guess_symbol:]
    guess_false = updated_assignments[0:guess_symbol-1] + [False] + updated_assignments[guess_symbol:] 
    return dpll(symbols, guess_true, _reduce(guess_true, clauses), recursion_depth+1) \
        or dpll(symbols, guess_false, _reduce(guess_false, clauses), recursion_depth+1)

# Provide a filename to log the recursion depth and clauses satisfied values
# If not filename is provided, all logging is printed to stdout
if __name__ == "__main__":
    import sys
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
    if(len(sys.argv) > 1):
        f = open(sys.argv[1], 'w')
        sys.stdout = f
    if(dpll(symbols, assignments, clauses, 0)):
        sys.stdout = original_stdout
        print("SATISFIABLE")
    else:
        sys.stdout = original_stdout
        print("UNSATISFIABLE")