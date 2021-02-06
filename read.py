def sanitize(string):
        newString = ""
        flag = False
        for letter in string:
            if letter == '@':
                flag = True
            elif letter == ' ':
                flag = False
            
            if flag:
                continue
            else:
                if letter != ' ':
                    newString += letter

        return newString.strip()


def readGrammer(fileName):
    noneTerminals = list()
    terminals = list()
    startSymbol = ""
    rules = dict()

    with open(fileName) as inputFile:
        index = 1
        lines = inputFile.readlines()

        for line in lines:

            if index == 1:
                for noneTerminal in line.strip().split(','):
                    if(len(noneTerminal) > 1):
                        raise NameError('none terminal can not be more than 1 chars.')
                    if noneTerminal in noneTerminals:
                        raise NameError(f'none terminal {noneTerminal}is repeated!')
                    noneTerminals.append(noneTerminal.upper())
                index += 1

            elif index == 2:
                for terminal in line.strip().split(','):
                    terminals.append(terminal.lower())
                index += 1

            elif index == 3:
                char = line.strip()
                if len(char) > 1:
                    raise NameError(f'Start symbol can not be greater than one char!')
                if char not in noneTerminals:
                    raise NameError(f'Start symbol is not in noneTerminals!')
                startSymbol = char
                index += 1

            else:
                left, right = line.strip().split('->')
                left = left.strip()
                right = right.strip()

                if left.islower():
                    raise NameError(f'{left} can not be lowercase!')

                if left not in noneTerminals:
                    raise NameError(f'{left} is not in none terminals!')
                
                newRight = sanitize(right).strip()
                word = ""
                for letter in newRight:
                    if letter == ' ' or letter == '~':
                        continue

                    if letter.isupper():
                        if word:
                            if word not in terminals:
                                raise NameError(f'{word} is not in terminals!')
                        word = ""
                        if letter not in noneTerminals:
                            raise NameError(f'{letter} is not in none terminals!')
                    else:
                        word += letter
                if word:
                    if word not in terminals:
                        raise NameError(f'{word} is not in terminals!')        
                
                #left -> right    {}
                if left in rules:
                    rules[left].append(right)
                else:
                    rules[left] = [right]

    return (noneTerminals, terminals, startSymbol, rules)




def readInput(fileName):
    with open(fileName) as inputFile:
        return inputFile.readline().strip()