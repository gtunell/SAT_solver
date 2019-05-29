# SAT_solver
2SAT and 3SAT solvers.

### 2SAT  
**Input**  
The first line will encode a boolean formula in conjunctive normal form
(CNF). The encoded formula consists of a sequence of one or more encoded
clauses each separated by a single semicolon (;). Each encoded clause consists
of a sequence of one or more encoded literals each separated by a single
comma (,). Each encoded literal consists of one or more lowercase letters
and numbers representing a variable name, optionally preceded by a dash
(-) representing the negation of the variable.  
To illustrate, the input
-a1,a2;a2,-b;b
encodes the boolean formula
(¬a1 ∨ a2) ∧ (a2 ∨ ¬b) ∧ (b).


