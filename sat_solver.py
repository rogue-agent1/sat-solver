#!/usr/bin/env python3
"""sat_solver: DPLL SAT solver for Boolean satisfiability."""
import sys

def dpll(clauses, assignment=None):
    if assignment is None: assignment = {}
    clauses = simplify(clauses, assignment)
    if clauses is None: return None
    if not clauses: return assignment
    # Unit propagation
    for c in clauses:
        if len(c) == 1:
            lit = c[0]
            var = abs(lit)
            val = lit > 0
            new_assign = {**assignment, var: val}
            return dpll(clauses, new_assign)
    # Pure literal elimination
    all_lits = {lit for c in clauses for lit in c}
    for lit in all_lits:
        if -lit not in all_lits:
            var = abs(lit)
            new_assign = {**assignment, var: val} if var not in assignment else assignment
            val = lit > 0
            new_assign = {**assignment, var: val}
            return dpll(clauses, new_assign)
    # Choose variable
    var = abs(clauses[0][0])
    for val in [True, False]:
        result = dpll(clauses, {**assignment, var: val})
        if result is not None: return result
    return None

def simplify(clauses, assignment):
    new_clauses = []
    for c in clauses:
        new_c = []
        satisfied = False
        for lit in c:
            var = abs(lit)
            if var in assignment:
                if (lit > 0) == assignment[var]:
                    satisfied = True; break
            else:
                new_c.append(lit)
        if satisfied: continue
        if not new_c: return None  # Empty clause = conflict
        new_clauses.append(new_c)
    return new_clauses

def test():
    # Simple SAT: (x1 OR x2) AND (NOT x1 OR x2) AND (x1 OR NOT x2)
    clauses = [[1, 2], [-1, 2], [1, -2]]
    result = dpll(clauses)
    assert result is not None
    assert result[1] == True and result[2] == True
    # UNSAT: (x1) AND (NOT x1)
    clauses2 = [[1], [-1]]
    assert dpll(clauses2) is None
    # Trivial
    assert dpll([]) == {}
    # 3-SAT
    clauses3 = [[1, 2, 3], [-1, -2, 3], [1, -2, -3], [-1, 2, -3]]
    r3 = dpll(clauses3)
    assert r3 is not None
    for c in clauses3:
        assert any((lit > 0) == r3.get(abs(lit), True) for lit in c)
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: sat_solver.py test")
