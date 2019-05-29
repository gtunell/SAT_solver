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

**Output**

The output will be either two or three lines to standard output, depending on
the input. The first line outputs either output yes or no, where yes
means that the given formula is satisfiable, and no means otherwise.
If the formula is satisfiable, also output another line representing
a satisying assignment of variables for the formula. This line will contain
a sequence of comma-separated substrings of the form var name=value, where
for some variable v, var name denotes the variable name of v and value
denotes the boolean value it receives from the assignment (either T or F).
There will be one such substring per variable that appears in the formula.
So for the formula  
(¬a1 ∨ a2) ∧ (a2 ∨ ¬b) ∧ (b)  
given above, one possible assignment would be (a1, a2, b) = (F, T, T). A  
possible output corresponding to this assignment would be formatted as  
b=T,a1=F,a2=T.  
Regardless of whether the formula is satisfiable or not, on a new line, output a single dollar sign ($)




