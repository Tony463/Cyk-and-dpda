def read_pda_and_word(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    
    sections = {}
    current_section = None
    
    for line in lines:
        if line in ["Stări", "Alfabet de intrare", "Alfabetul stivei", "Tranziții", "Stare inițială", "Simbol inițial al stivei", "Stări finale", "Cuvânt"]:
            current_section = line
            sections[current_section] = []
        else:
            sections[current_section].append(line)
    
    states = sections["Stări"][0].split()
    input_alphabet = sections["Alfabet de intrare"][0].split()
    stack_alphabet = sections["Alfabetul stivei"][0].split()
    transitions = {}
    
    for transition in sections["Tranziții"]:
        parts = transition.split("->")
        lhs = parts[0].strip().strip("()").split(", ")
        rhs = parts[1].strip().strip("()").split(", ")
        key = (lhs[0], lhs[1], lhs[2])
        value = (rhs[0], rhs[1])
        transitions[key] = value
    
    initial_state = sections["Stare inițială"][0]
    initial_stack_symbol = sections["Simbol inițial al stivei"][0]
    final_states = sections["Stări finale"][0].split()
    word = sections["Cuvânt"][0]
    
    return (states, input_alphabet, stack_alphabet, transitions, initial_state, initial_stack_symbol, final_states, word)

def dpda_accepts(states, input_alphabet, stack_alphabet, transitions, initial_state, initial_stack_symbol, final_states, word):
    stack = [initial_stack_symbol]
    current_state = initial_state
    
    for symbol in word:
        if (current_state, symbol, stack[-1]) in transitions:
            next_state, stack_action = transitions[(current_state, symbol, stack[-1])]
            stack.pop()
            if stack_action != 'ε':
                stack.extend(reversed(stack_action))
            current_state = next_state
        else:
            return False
    
    while stack and (current_state, 'ε', stack[-1]) in transitions:
        next_state, stack_action = transitions[(current_state, 'ε', stack[-1])]
        stack.pop()
        if stack_action != 'ε':
            stack.extend(reversed(stack_action))
        current_state = next_state
    
    return current_state in final_states

# Citirea automatului și a cuvântului
file_path = 'pda_and_word.txt'
(states, input_alphabet, stack_alphabet, transitions, initial_state, initial_stack_symbol, final_states, word) = read_pda_and_word(file_path)

# Verificarea cuvântului
result = dpda_accepts(states, input_alphabet, stack_alphabet, transitions, initial_state, initial_stack_symbol, final_states, word)
print(f'Cuvântul "{word}" {"aparține" if result else "nu aparține"} limbajului definit de automat.')
