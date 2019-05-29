# SAT_solver
2SAT and 3SAT solvers.

## 2SAT  
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

      (¬a1 ∨ a2) ∧ (a2 ∨ ¬b) ∧ (b)
      
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

      b=T,a1=F,a2=T
      
Regardless of whether the formula is satisfiable or not, on a new line, output a single dollar sign ($)  

## STAND Algorithm for 3SAT
**Input**

The first line of input consists of an encoded boolean formula that will be
used by STAND. This encoded formula will be encoded the same way as the
encoded formula given in part one. This time, however, the
boolean formula may have up to three (instead of two) literals per clause.
The second line of input consists of an encoded partial assignment that
will be used by STAND. This line will be encoded using the same encoding 
scheme specified in the output section of part one. Keep in mind that
this represents a partial assignment, so it will not necessarily determine the
meaning of every variable that appears in the given formula. It is possible
that no variables will be assigned a value, in which case only an empty line
will be provided.

**Output**

The output will be either two or three lines to standard output, depending on
the input. The first line will output either output yes, no, or maybe, where yes
means that the given formula is satisfiable under the partial assignment, no
means that it is not, and maybe means that not enough information could be
determined from STAND to determine satisfiability.
If the ouput is yes or maybe previously, then output a new line
representing an extended partial assignment that is produced by STAND
on the given input. If the previous output was specifically yes, then this
extended partial assignment will be a total assignment. Lastly, on a new line, 
output a single dollar sign to separate the output.

## Recursive 7-ALG
**Input**

This part has one line of input consisting of an encoded boolean formula that will
be used by R7ALG. This encoded formula will be encoded the same way as
the encoded formula given in part one of the project. Similarly to the second
part of the project, the boolean formula may have up to three literals per
clause.
Notice that no partial assignment is given as part of the input for this part. 
This part is similar to STAND but with no partial assignment given.

**Output**

Output will be either one or two lines to standard output, depending on
the input. Similar to part one, for the first line, either output yes
or no, where yes means that the given formula is satisfiable, and no means
otherwise. If the formula is satisfiable, output another line
representing a satisfying assignment of variables for the formula. This line
should be formatted using the same rules used in the previous two parts.
No dollar sign is printed after this part






