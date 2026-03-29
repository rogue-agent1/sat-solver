#!/usr/bin/env python3
"""SAT solver using DPLL algorithm."""
import sys

def dpll(clauses, assignment=None):
    assignment = assignment or {}
    clauses = simplify(clauses, assignment)
    if clauses is None: return None
    if not clauses: return assignment
    # Unit propagation
    for c in clauses:
        if len(c) == 1:
            lit = next(iter(c)); var = abs(lit)
            a = dict(assignment); a[var] = lit > 0
            return dpll(clauses, a)
    # Pure literal
    lits = {lit for c in clauses for lit in c}
    for lit in lits:
        if -lit not in lits:
            var = abs(lit); a = dict(assignment); a[var] = lit > 0
            return dpll(clauses, a)
    # Branch
    var = abs(next(iter(next(iter(clauses)))))
    for val in [True, False]:
        a = dict(assignment); a[var] = val
        result = dpll(clauses, a)
        if result is not None: return result
    return None

def simplify(clauses, assignment):
    result = []
    for clause in clauses:
        new_clause = set()
        satisfied = False
        for lit in clause:
            var = abs(lit); val = assignment.get(var)
            if val is None: new_clause.add(lit)
            elif (lit > 0) == val: satisfied = True; break
        if satisfied: continue
        if not new_clause: return None  # empty clause = conflict
        result.append(frozenset(new_clause))
    return result

def parse_dimacs(text):
    clauses = []
    for line in text.strip().split("\n"):
        if line.startswith("c") or line.startswith("p"): continue
        lits = [int(x) for x in line.split() if x != "0"]
        if lits: clauses.append(frozenset(lits))
    return clauses

def main():
    if len(sys.argv) < 2: print("Usage: sat_solver.py <demo|test>"); return
    if sys.argv[1] == "test":
        # Simple SAT: (x1 OR x2) AND (NOT x1 OR x3)
        c = [frozenset([1, 2]), frozenset([-1, 3])]
        r = dpll(c); assert r is not None
        # Verify
        for clause in c:
            assert any((lit > 0) == r.get(abs(lit), True) for lit in clause)
        # UNSAT: (x) AND (NOT x)
        c2 = [frozenset([1]), frozenset([-1])]
        assert dpll(c2) is None
        # Trivially SAT
        assert dpll([]) == {}
        # Unit propagation
        c3 = [frozenset([1]), frozenset([1, 2]), frozenset([-1, 2])]
        r3 = dpll(c3); assert r3 is not None and r3.get(1) == True
        print("All tests passed!")
    else:
        c = [frozenset([1, 2, -3]), frozenset([-1, 3]), frozenset([2, 3])]
        r = dpll(c); print(f"SAT: {r}" if r else "UNSAT")

if __name__ == "__main__": main()
