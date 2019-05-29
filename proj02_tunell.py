#!/usr/bin/env python3
# Author: Gregory Tunell
# UID: 115065703

def get_implication_graph(formula):
    graph = {}
    for i in range(0, len(formula)):
        A = formula[i][0] 
        B = A if len(formula[i]) == 1 else formula[i][1]            
        not_A = A[1:] if A[0] == '-' else '-' + A
        not_B = B[1:] if B[0] == '-' else '-' + B
        not_A_adjacent = []
        not_B_adjacent = []

        if not_A in graph:
            not_A_adjacent = graph[not_A]
        if not_B in graph:
            not_B_adjacent = graph[not_B]

        if B not in not_A_adjacent: not_A_adjacent.append(B) 
        if A not in not_B_adjacent: not_B_adjacent.append(A)

        graph[not_A] = not_A_adjacent
        graph[not_B] = not_B_adjacent
        graph[A] = [] if A not in graph else graph[A]
        graph[B] = [] if B not in graph else graph[B]
    
    return graph

def recursive_dfs(graph, v, visited, stack): 
    visited.append(v)
    for u in graph[v]: 
        if u not in visited: 
            recursive_dfs(graph, u, visited, stack) 
    stack = stack.append(v) 

def transpose_graph(graph):
    transpose = {}
    for v in graph:
        transpose[v] = []

    for v in graph:
        for u in graph[v]:
            expand = transpose[u]
            expand.append(v)
            transpose[u] = expand

    return transpose    

def topological_order_by_scc(graph):

    visited = []    
    stack = []

    for v in graph:
        if v not in visited:
            recursive_dfs(graph, v, visited, stack)

    graph_transposed = transpose_graph(graph)
    
    visited = []
    topological_order = []
    while stack:
        v = stack.pop()
        if v not in visited:
            next_scc = []
            recursive_dfs(graph_transposed, v, visited, next_scc)
            topological_order.append(next_scc)

    return topological_order

def assign(key, scc, assignments):   
    not_key = key[1:] if key[0] == '-' else '-' + key
    neg_comp = -1
    pos_comp = -1
    for i in range(0, len(scc)):
        for j in scc[i]:
            if key == j:
                pos_comp = i
            if not_key == j:
                neg_comp = i

    if neg_comp == pos_comp:
        return 'no'
    elif neg_comp < pos_comp: 
        assignments[key] = True
    elif neg_comp > pos_comp:
        assignments[key] = False

    return 'yes'

def solve_2SAT(formula):
    formula_builder = []
    for clause in formula:
        clause_builder = []
        if len(clause) == 1:
            clause_builder.append(clause[0])
            clause_builder.append(clause[0])
        else:
            clause_builder.extend(clause)
        formula_builder.append(clause_builder)

    graph = get_implication_graph(formula_builder)
    scc = topological_order_by_scc(graph)
    assignments = {}
    result = 'yes'
    for key in graph:
        result = assign(key, scc, assignments)
        if result == 'no':
            break

    return result, assignments

    #results = test_assignment(formula, assignments)
    #print('Test result says assignments make formula ===> {}'.format(results))

def print_assignments(result, assignments):
    if result == 'yes' or result == 'maybe':
        print(result)
        output = []
        for assignment in assignments:
            if assignments[assignment] != '' and assignment[0] != '-':
                t_or_f = 'T' if assignments[assignment] else 'F'
                output.append('{}={}'.format(assignment, t_or_f))
        print(','.join(output))
    else:
        print('no')

def can_run_2SAT(formula):
    for i in range(0, len(formula)):
        length = len(formula[i])
        if length > 2 or length == 0:
            return False

    return True

def recursive_STAND(formula, dict_partial, annihilated):

    length = len(formula)
    if length == 0:
        return 'yes'

    seen_literals = []
    formula_builder = []
    clauses_removed = 0
    for i in range(0, length):
        clause_builder = []
        literal_one = ''
        literal_two = ''
        literal_three = ''

        clause = formula[i]
        length = len(clause)
        if length == 0:
            return 'no'

        if length == 1:
            literal_one = clause[0]
            literal_one_complement = literal_one[1:] if literal_one[0] == '-' else '-' + literal_one

            if literal_one not in seen_literals: seen_literals.append(literal_one) 

            if dict_partial[literal_one] == '' and dict_partial[literal_one] == '':
                dict_partial[literal_one] = True
                dict_partial[literal_one_complement] = False
                
            if dict_partial[literal_one] == True:
                clause_builder = ''
                
        if length == 2:
            literal_one = clause[0]
            literal_two = clause[1]

            if literal_one not in seen_literals: seen_literals.append(literal_one) 
            if literal_two not in seen_literals: seen_literals.append(literal_two) 

            if dict_partial[literal_one] == True:
                formula_minus_clause = formula_builder[0:i - clauses_removed] + formula[i + 1:]
                flattened = []
                for i in range(0, len(formula_minus_clause)):
                    flattened.extend(formula_minus_clause[i])
                literal_two_complement = literal_two[1:] if literal_two[0] == '-' else '-' + literal_two
                if literal_two not in flattened and literal_two_complement not in flattened: annihilated.append(literal_two)
                clause_builder = ''
            elif dict_partial[literal_two] == True:
                formula_minus_clause = formula_builder[0:i - clauses_removed] + formula[i + 1:]
                flattened = []
                for i in range(0, len(formula_minus_clause)):
                    flattened.extend(formula_minus_clause[i])
                literal_one_complement = literal_one[1:] if literal_one[0] == '-' else '-' + literal_one
                if literal_one not in flattened and literal_one_complement not in flattened: annihilated.append(literal_one)
                clause_builder = ''
            elif dict_partial[literal_one] == False and dict_partial[literal_two] == '':
                clause_builder.append(literal_two)
            elif dict_partial[literal_one] == '' and dict_partial[literal_two] == False:
                clause_builder.append(literal_one)
            elif dict_partial[literal_one] == '' and dict_partial[literal_two] == '':
                clause_builder.append(literal_one)
                clause_builder.append(literal_two)

        if length == 3:
            literal_one = clause[0]
            literal_two = clause[1]
            literal_three = clause[2]

            if literal_one not in seen_literals: seen_literals.append(literal_one) 
            if literal_two not in seen_literals: seen_literals.append(literal_two) 
            if literal_three not in seen_literals: seen_literals.append(literal_three) 

            if dict_partial[literal_one] == True:
                # formula_minus_clause = formula[0:i] + formula[i+1:]
                formula_minus_clause = formula_builder[0:i - clauses_removed] + formula[i + 1:]
                flattened = []
                for i in range(0, len(formula_minus_clause)):
                    flattened.extend(formula_minus_clause[i])
                literal_two_complement = literal_two[1:] if literal_two[0] == '-' else '-' + literal_two
                literal_three_complement = literal_three[1:] if literal_three[0] == '-' else '-' + literal_three
                if literal_two not in flattened and literal_two_complement not in flattened: annihilated.append(literal_two)
                if literal_three not in flattened and literal_three_complement not in flattened: annihilated.append(literal_three)
                clause_builder = ''
            elif dict_partial[literal_two] == True:
                # formula_minus_clause = formula[0:i] + formula[i+1:]
                formula_minus_clause = formula_builder[0:i - clauses_removed] + formula[i + 1:]
                flattened = []
                for i in range(0, len(formula_minus_clause)):
                    flattened.extend(formula_minus_clause[i])
                literal_one_complement = literal_one[1:] if literal_one[0] == '-' else '-' + literal_one
                literal_three_complement = literal_three[1:] if literal_three[0] == '-' else '-' + literal_three
                if literal_one not in flattened and literal_one_complement not in flattened: annihilated.append(literal_one)
                if literal_three not in flattened and literal_three_complement not in flattened: annihilated.append(literal_three)
                clause_builder = ''
            elif dict_partial[literal_three] == True:
                # formula_minus_clause = formula[0:i] + formula[i+1:]
                formula_minus_clause = formula_builder[0:i - clauses_removed] + formula[i + 1:]
                flattened = []
                for i in range(0, len(formula_minus_clause)):
                    flattened.extend(formula_minus_clause[i])
                literal_one_complement = literal_one[1:] if literal_one[0] == '-' else '-' + literal_one
                literal_two_complement = literal_two[1:] if literal_two[0] == '-' else '-' + literal_two
                if literal_one not in flattened and literal_one_complement not in flattened: annihilated.append(literal_one)
                if literal_two not in flattened and literal_two_complement not in flattened: annihilated.append(literal_two)
                clause_builder = ''
            elif dict_partial[literal_one] == False and dict_partial[literal_two] == False and dict_partial[literal_three] == '':
                clause_builder.append(literal_three)
            elif dict_partial[literal_one] == False and dict_partial[literal_two] == '' and dict_partial[literal_three] == False:
                clause_builder.append(literal_two)    
            elif dict_partial[literal_one] == '' and dict_partial[literal_two] == False and dict_partial[literal_three] == False:
                clause_builder.append(literal_one)
            elif dict_partial[literal_one] == False and dict_partial[literal_two] == '' and dict_partial[literal_three] == '':
                clause_builder.append(literal_two)
                clause_builder.append(literal_three)
            elif dict_partial[literal_one] == '' and dict_partial[literal_two] == False and dict_partial[literal_three] == '':
                clause_builder.append(literal_one)
                clause_builder.append(literal_three)
            elif dict_partial[literal_one] == '' and dict_partial[literal_two] == '' and dict_partial[literal_three] == False:
                clause_builder.append(literal_one)
                clause_builder.append(literal_two)
            elif dict_partial[literal_one] == '' and dict_partial[literal_two] == '' and dict_partial[literal_three] == '':
                clause_builder.append(literal_one)
                clause_builder.append(literal_two)
                clause_builder.append(literal_three)

        if clause_builder != '':
            formula_builder.append(clause_builder)
            clauses_removed = clauses_removed + 1
            '''
            if clause_builder == '':
                formula_builder.extend(formula[i + 1:])
                return recursive_STAND(formula_builder, dict_partial, annihilated)
            else:
                formula_builder.append(clause_builder)
            '''

    recurse_again = False
    for literal in seen_literals:
        complement = literal[1:] if literal[0] == '-' else '-' + literal

        if complement not in seen_literals:
            recurse_again = True
            if dict_partial[literal] == '' and dict_partial[complement] == '':
                dict_partial[literal] = True
                dict_partial[complement] = False

    if not recurse_again and formula == formula_builder:
        if can_run_2SAT(formula):
            result, assignments = solve_2SAT(formula)
            if result == 'yes':
                for literal in assignments:
                    if dict_partial[literal] != '' and assignments[literal] != dict_partial[literal]:
                        return 'no'
                dict_partial.update(assignments)
                return 'yes'
            else:
                return 'no'    

        return 'maybe'
    else:
        return recursive_STAND(formula_builder, dict_partial, annihilated)


def STAND(formula, partial_assignment):

    dict_partial = {}
    for assignment in partial_assignment:
        literal = assignment[0]
        complement = literal[1:] if literal[0] == '-' else '-' + literal
        dict_partial[literal] = True if assignment[1] == 'T' else False
        dict_partial[complement] = True if assignment[1] == 'F' else False

    formula_builder = []
    annihilated = []
    clauses_removed = 0
    for index in range(0, len(formula)):
        clause = formula[index]
        length = len(clause)

        for i in range(0, length):
            literal = clause[i]
            if literal not in dict_partial:
                dict_partial[literal] = ''

        clause_builder = []
        if length == 1:
            literal_first = clause[0]
            clause_builder.append(literal_first)

        if length == 2:
            literal_first = clause[0]
            literal_second = clause[1]

            if literal_first == literal_second:
                clause_builder.append(literal_first)
            elif ('-' + literal_first) != literal_second and literal_first != ('-' + literal_second):
                clause_builder.append(literal_first)
                clause_builder.append(literal_second)

        if length == 3:
            literal_first = clause[0]
            literal_second = clause[1]
            literal_third = clause[2]

            if ('-' + literal_first) == literal_second or literal_first == ('-' + literal_second):
                if literal_third != literal_first and literal_third != literal_second:
                    #formula_minus_clause = formula[0:index] + formula[index+1:]
                    formula_minus_clause = formula_builder[0:i - clauses_removed] + formula[i + 1:]
                    flattened = []
                    for i in range(0, len(formula_minus_clause)):
                        flattened.extend(formula_minus_clause[i])
                    literal_third_complement = literal_third[1:] if literal_third[0] == '-' else '-' + literal_third
                    if literal_third not in flattened and literal_third_complement not in flattened: annihilated.append(literal_third)
            elif ('-' + literal_first) == literal_third or literal_first == ('-' + literal_third):
                if literal_second != literal_first and literal_second != literal_third:
                    #formula_minus_clause = formula[0:index] + formula[index+1:]
                    formula_minus_clause = formula_builder[0:i - clauses_removed] + formula[i + 1:]
                    flattened = []
                    for i in range(0, len(formula_minus_clause)):
                        flattened.extend(formula_minus_clause[i])
                    literal_second_complement = literal_second[1:] if literal_second[0] == '-' else '-' + literal_second
                    if literal_second not in flattened and literal_second_complement not in flattened: annihilated.append(literal_second)
            elif ('-' + literal_second) == literal_third or literal_second == ('-' + literal_third):
                if literal_first != literal_second and literal_first != literal_third:
                    #formula_minus_clause = formula[0:index] + formula[index+1:]
                    formula_minus_clause = formula_builder[0:i - clauses_removed] + formula[i + 1:]
                    flattened = []
                    for i in range(0, len(formula_minus_clause)):
                        flattened.extend(formula_minus_clause[i])
                    literal_first_complement = literal_first[1:] if literal_first[0] == '-' else '-' + literal_first
                    if literal_first not in flattened and literal_first_complement not in flattened: annihilated.append(literal_first)
            elif literal_first == literal_second and literal_first == literal_third:
                clause_builder.append(literal_first)
            elif literal_first == literal_second:
                clause_builder.append(literal_first)
                clause_builder.append(literal_third)
            elif literal_first == literal_third or literal_second == literal_third:
                clause_builder.append(literal_first)
                clause_builder.append(literal_second)
            else:
                clause_builder.append(literal_first)
                clause_builder.append(literal_second)
                clause_builder.append(literal_third)

        if len(clause_builder) > 0:
            formula_builder.append(clause_builder) 


    complements_to_add = []
    for literal in dict_partial:
        if dict_partial[literal] == '':
            complement = literal[1:] if literal[0] == '-' else '-' + literal

            if complement not in dict_partial:
                complements_to_add.append(complement)
                dict_partial[literal] = True

    for complement in complements_to_add:
        dict_partial[complement] = False

    result = recursive_STAND(formula_builder, dict_partial, annihilated)

    for literal in annihilated:
        if dict_partial[literal] == '':
            complement = literal[1:] if literal[0] == '-' else '-' + literal
            dict_partial[literal] = True
            dict_partial[complement] = False

    #results = test_assignment(formula, dict_partial)
    #print('Test result says assignments make formula ===> {}'.format(results))
    return result, dict_partial, annihilated

def call7ALG(clause_index, formula, dict_partial, annihilated):

    next_clause = formula[clause_index]
    '''
    if len(next_clause) == 1:
        literal = next_clause[0]
        string_literal = [[literal, 'T']]
        new_formula = []
        for i in range(0, len(formula)):
            new_clause = []
            for j in range(0, len(formula[i])):
                new_clause.append(formula[i][j])
            new_formula.append(new_clause)
        result, new_dict_partial, _ = STAND(new_formula, string_literal)
        if result == 'maybe' and formula != new_formula and cmp(dict_partial, new_dict_partial) != 0:
            dict_partial.update(new_dict_partial)
            return call7ALG(0, new_formula, new_dict_partial)
    '''

    if len(next_clause) == 2:
        literal1 = next_clause[0]
        literal2 = next_clause[1]

        new_formula = []
        for i in range(0, len(formula)):
            new_clause = []
            for j in range(0, len(formula[i])):
                new_clause.append(formula[i][j])
            new_formula.append(new_clause)
        string_literal = [[literal1, 'T'], [literal2, 'T']]
        result, new_dict_partial, _ = STAND(new_formula, string_literal)
        if result == 'maybe' and formula != new_formula and cmp(dict_partial, new_dict_partial) != 0:
            dict_partial.update(new_dict_partial)
            return call7ALG(0, new_formula, new_dict_partial)
        if result == 'yes':
            return result, new_dict_partial
        
        new_formula = []
        for i in range(0, len(formula)):
            new_clause = []
            for j in range(0, len(formula[i])):
                new_clause.append(formula[i][j])
            new_formula.append(new_clause)
        string_literal = [[literal1, 'T'], [literal2, 'F']]
        result, new_dict_partial, _ = STAND(new_formula, string_literal)
        if result == 'maybe' and formula != new_formula and cmp(dict_partial, new_dict_partial) != 0:
            dict_partial.update(new_dict_partial)
            return call7ALG(0, new_formula, new_dict_partial)
        if result == 'yes':
            return result, new_dict_partial

        new_formula = []
        for i in range(0, len(formula)):
            new_clause = []
            for j in range(0, len(formula[i])):
                new_clause.append(formula[i][j])
            new_formula.append(new_clause)
        string_literal = [[literal1, 'F'], [literal2, 'T']]
        result, new_dict_partial, _ = STAND(new_formula, string_literal)
        if result == 'maybe' and formula != new_formula and cmp(dict_partial, new_dict_partial) != 0:
            dict_partial.update(new_dict_partial)
            return call7ALG(0, new_formula, new_dict_partial)
        if result == 'yes':
            return result, new_dict_partial

    if len(next_clause) == 3:
        
        literal1 = next_clause[0]
        literal2 = next_clause[1]
        literal3 = next_clause[1]

        new_formula = []
        for i in range(0, len(formula)):
            new_clause = []
            for j in range(0, len(formula[i])):
                new_clause.append(formula[i][j])
            new_formula.append(new_clause)
        string_literal = [[literal1, 'T'], [literal2, 'T'], [literal3, 'T']]
        result, new_dict_partial, _ = STAND(new_formula, string_literal)
        if result == 'maybe' and formula != new_formula and cmp(dict_partial, new_dict_partial) != 0:
            dict_partial.update(new_dict_partial)
            return call7ALG(0, new_formula, new_dict_partial)
        if result == 'yes':
            return result, new_dict_partial

        new_formula = []
        for i in range(0, len(formula)):
            new_clause = []
            for j in range(0, len(formula[i])):
                new_clause.append(formula[i][j])
            new_formula.append(new_clause)
        string_literal = [[literal1, 'T'], [literal2, 'F'], [literal3, 'T']]
        result, new_dict_partial, _ = STAND(new_formula, string_literal)
        if result == 'maybe' and formula != new_formula and cmp(dict_partial, new_dict_partial) != 0:
            dict_partial.update(new_dict_partial)
            return call7ALG(0, new_formula, new_dict_partial)
        if result == 'yes':
            return result, new_dict_partial

        new_formula = []
        for i in range(0, len(formula)):
            new_clause = []
            for j in range(0, len(formula[i])):
                new_clause.append(formula[i][j])
            new_formula.append(new_clause)
        string_literal = [[literal1, 'F'], [literal2, 'T'], [literal3, 'T']]
        result, new_dict_partial, _ = STAND(new_formula, string_literal)
        if result == 'maybe' and formula != new_formula and cmp(dict_partial, new_dict_partial) != 0:
            dict_partial.update(new_dict_partial)
            return call7ALG(0, new_formula, new_dict_partial)
        if result == 'yes':
            return result, new_dict_partial
        
        new_formula = []
        for i in range(0, len(formula)):
            new_clause = []
            for j in range(0, len(formula[i])):
                new_clause.append(formula[i][j])
            new_formula.append(new_clause)
        string_literal = [[literal1, 'T'], [literal2, 'F'], [literal3, 'F']]
        result, new_dict_partial, _ = STAND(new_formula, string_literal)
        if result == 'maybe' and formula != new_formula and cmp(dict_partial, new_dict_partial) != 0:
            dict_partial.update(new_dict_partial)
            return call7ALG(0, new_formula, new_dict_partial)
        if result == 'yes':
            return result, new_dict_partial

        new_formula = []
        for i in range(0, len(formula)):
            new_clause = []
            for j in range(0, len(formula[i])):
                new_clause.append(formula[i][j])
            new_formula.append(new_clause)
        string_literal = [[literal1, 'F'], [literal2, 'F'], [literal3, 'T']]
        result, new_dict_partial, _ = STAND(new_formula, string_literal)
        if result == 'maybe' and formula != new_formula and cmp(dict_partial, new_dict_partial) != 0:
            dict_partial.update(new_dict_partial)
            return call7ALG(0, new_formula, new_dict_partial)
        if result == 'yes':
            return result, new_dict_partial

        new_formula = []
        for i in range(0, len(formula)):
            new_clause = []
            for j in range(0, len(formula[i])):
                new_clause.append(formula[i][j])
            new_formula.append(new_clause)
        string_literal = [[literal1, 'F'], [literal2, 'T'], [literal3, 'F']]
        result, new_dict_partial, _ = STAND(new_formula, string_literal)
        if result == 'maybe' and formula != new_formula and cmp(dict_partial, new_dict_partial) != 0:
            dict_partial.update(new_dict_partial)
            return call7ALG(0, new_formula, new_dict_partial)
        if result == 'yes':
            return result, new_dict_partial

    if clause_index + 1 >= len(formula):
        return 'no',[]
    else:
        return call7ALG(clause_index + 1, formula, dict_partial, annihilated)
    

def test_assignment(formula, assignment):
    result = True
    for clause in formula:
        clause_result = False
        for i in range(0, len(clause)):
            if clause[i] in assignment: 
                clause_result = clause_result or assignment[clause[i]] 

        result = result and clause_result
    return result

def main():
    input_lines = [input(), input(), input(), input()]

    # Part1
    formula = input_lines[0].split(';')
    for i in range(0, len(formula)): formula[i] = formula[i].split(',')
    result, assignments = solve_2SAT(formula)
    print_assignments(result, assignments)
    print('$')
    
    # Part2
    formula = input_lines[1].split(';')
    for i in range(0, len(formula)): formula[i] = formula[i].split(',')
    partial_assignment = input_lines[2].split(',')
    for i in range(0, len(partial_assignment)): partial_assignment[i] = partial_assignment[i].split('=')
    result, dict_partial, _ = STAND(formula, partial_assignment)
    print_assignments(result, dict_partial)
    print('$')

    # Part3
    formula = input_lines[3].split(';')
    for i in range(0, len(formula)): formula[i] = formula[i].split(',')
    result, dict_partial = call7ALG(0, formula, dict_partial, [])
    print_assignments(result, dict_partial)

    
    #results = test_assignment(formula, dict_partial)
    #print('Test result says assignments make formula ===> {}'.format(results))

if __name__ == "__main__":
    main()