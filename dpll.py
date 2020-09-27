# Uses CNF input as described here: 
# http://www.satcompetition.org/2011/format-benchmarks2011.html

def find_pure_symbols(symbols, clauses):
    for symbol in range(len(symbols)):
        for clause in clauses:
            for instance in clause:
                    

def find_unit_clauses(symbols, clauses):


def
def dpll(clauses, symbols):
    # Check if all clauses are already true
    if (all([any(i) for i in clauses])):
        return True

user_input = input()

while(user_input[0] == 'c'):
    user_input = input()

_, _, nbvar, nbclauses = user_input.split()
nbvar = int(nbvar)
nbclauses = int(nbclauses)

symbols = [None] * nbvar
clauses = [None] * nbclauses

for i in range(nbclauses):
    user_input = input() 
    clauses[i] = [int(i) for i in user_input.split()]

dpll(clauses, symbols)

    

