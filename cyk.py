#Function to read the grammar and the word from a file
def load_grammar_and_word(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    grammar = {}
    word = ''
    for line in lines:
        line = line.strip()
        if '->' in line: 
            left, right = line.split('->')
            left = left.strip()
            right = right.strip()
            if left not in grammar:
                grammar[left] = []
            grammar[left].append(right.split())
        else:
            word = line.strip()  
    
    return grammar, word

#Function implementing the CYK algorithm to verify if the word belongs to the language
def cyk_check(grammar, word):
    n = len(word)
    if n == 0:
        return False
    
    #matrix to store set of non-terminals
    table = [[set() for _ in range(n)] for _ in range(n)]
    
    #Fill the matrix for substrings of length 1
    for i in range(n):
        for lhs, productions in grammar.items():
            for production in productions:
                if len(production) == 1 and production[0] == word[i]:
                    table[i][i].add(lhs)  #Contains the non-terminals that produce the letter at postion i

    #Fill the matrix for substrings of length greater than 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for lhs, productions in grammar.items():
                    for production in productions:
                        if len(production) == 2:
                            B, C = production
                            if B in table[i][k] and C in table[k + 1][j]:  #Check if the non-terminal B can produce the substring from i to k and C                                                     
                                table[i][j].add(lhs)                        # can produce the substring from k+1 to j
    
    start_symbol = 'S'  
    return start_symbol in table[0][n - 1]


file_path = 'grammar_and_word.txt'
grammar, word = load_grammar_and_word(file_path)


result = cyk_check(grammar, word)
print(f'The word "{word}" {"is" if result else "is not"} part of the language defined by the grammar.')
