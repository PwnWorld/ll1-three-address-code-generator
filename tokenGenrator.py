#lexicalAnalyzer has two class => first one is 'dfa' second one is 'input validation' that inherits from dfa
from lexicalAnalyzer import InputValidation


def tokenGenrator(text): # create tokens and add $ and return stack
    tokens = []
    analyzer = InputValidation()

    words = text.split(' ')

    for word in words:
        while len(word) > 0:
            res, data = analyzer.try_input(word)
            if res:
                token = data['final state']
                if token == 'id' or token == 'int':
                    tokens.append(token + '-' + word)
                else:
                    tokens.append(token)
                break
            else:
                if data['last final state']:
                    token = data['last final state']
                    if token == 'id':
                        tokens.append(token + '-' + word)
                    elif token == 'int':
                        tokens.append(token + '-' + "".join(filter(str.isdigit, word)))
                    else:
                        tokens.append(token)
                    word = word[data['index last final char']+1:]
                else:
                    raise NameError(f'LEXICAL ERROR {word}')
    tokens.append('$')
    tokens = tokens[::-1]
    return tokens