from tokenGenrator import tokenGenrator
class LL1:
    noneTerminals = list()
    terminals = list()
    startSymbol = ""
    rules = dict()

    def __init__(self, noneTerminals, terminals, startSymbol, rules): #gets grammer data from inputGrammer
        self.noneTerminals = noneTerminals
        self.terminals = terminals
        self.startSymbol = startSymbol
        self.rules = rules


    def calcFirst(self):  # calculate all of firsts in none terminals
        firsts = {}
        for noneTerminal in self.noneTerminals[::-1]:
            firsts[noneTerminal] = self.first(noneTerminal, self.rules[noneTerminal])
        return firsts


    def first(self, left, right):#C -> [~ , BDid]
        firsts = set() 
        for rule in right:
            rule = self.sanitize(rule)
            word = ""
            counter = -1
            for letter in rule:
                counter += 1
                if letter.isupper(): #if letter is none terminal
                    if left == letter: #eshtegag az chap
                        raise TypeError("left derivation in grammer is not supported!")
                    res = self.first(letter, self.rules[letter])
                    if '~' in res:
                        if counter + 1 != len(rule):
                            res.remove('~')
                            firsts.update(res)
                        else:
                            firsts.update(res)
                    else:
                        firsts.update(res)
                        break
                elif letter == '~': #if none terminal goes ~ then add ~ to first this none terminal
                    firsts.add(letter)
                    break
                else: #if rule starts with terminal add to this none termnial first
                    word += letter
                    if word in self.terminals:
                        firsts.add(word)
                        break
        return firsts


    def sanitize(self, string):  # gets a string and removes @funcs and returns new string
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


    def calcFollow(self): # calculate all of follows in none terminals
        follows = {}
        for noneTerminal in self.noneTerminals:
            follows[noneTerminal] = self.follow(noneTerminal)
        return follows
    

    def follow(self, left): #left => none terminal
        follows = set()
        if left == self.startSymbol: #
            follows.add('$')

        for noneTerminal in self.rules:
            flag = False
            for rule in self.rules[noneTerminal]:  #search for left in rules
                rule = self.sanitize(rule)
                counter = 0
                while counter < len(rule):
                    if  rule[counter] == left:  #search matched
                        if left == noneTerminal: #prevent from infinite loop e.g C -> AC
                            flag = True
                            break
                        res = rule[counter+1:]
                        if res:
                            word = ""
                            for letter in res:
                                if letter.isupper():
                                    #imagine C -> BADC then claculte first ADC and add to B's follows
                                    first = self.first(letter, self.rules[letter])
                                    follows.update(first)
                                    if '~' in first:
                                        #imagine C -> BA    if there is ~ in first A then add follow C TO FOLLOW B
                                        follows.update(self.follow(letter))
                                else:
                                    word += letter
                                    if word in self.terminals:
                                        #imagine C -> Bid   follow B is id
                                        follows.add(word)
                                        break
                        else:
                            #imagine C -> B then follow C is follow B
                            follows.update(self.follow(noneTerminal))
                    counter += 1
                if flag == True:
                    flag = False
                    break
        if '~' in follows: #remove all of ~ from follows because we can not have ~ in follow set
            follows.remove('~')
        return follows


    def LL1Table(self): # calculate ll1 parse table with first and follow methods
        table = {}

        counter = 1
        for noneTerminal in self.rules:
            table[noneTerminal] = {}
            for rule in self.rules[noneTerminal]:
                first = self.first(noneTerminal, [rule])
                for item in first:
                    if item != '~':
                        table[noneTerminal][item] = counter
                    else:
                        follow = self.follow(noneTerminal)
                        for item1 in follow:
                            table[noneTerminal][item1] = counter

                counter += 1
        return table

    def indexedRules(self): #create table of rules with number for evey rule
        newIndexedRules = []
        for noneTerminal in self.rules:
            for rule in self.rules[noneTerminal]:
                    newIndexedRules.append([noneTerminal, rule])
        return newIndexedRules

    def getThreeAddressCode(self, inpt): # gets an input and parse it with ll1 parse table
        funcs = set()
        semanticStack = []
        addressCounter = 400
        tempAddressCounter = 600
        threeCodeAddress = []
        tableParser = self.LL1Table()
        indexedRules = self.indexedRules()
        tokens = tokenGenrator(inpt) #gets input and creates tokens with dfa
        print("tokens: ", tokens)
        stack = []
        stack.append('$')
        stack.append(self.startSymbol)

        print("three address code: ", threeCodeAddress)
        print("semantic stack: ", semanticStack)
        print("token stack", tokens)
        print("parse stack", stack)
        print("\n")

        print(tokens)
        print(stack)
        print("\n")


        while stack or tokens:
            if stack[-1] == '$' and tokens[-1].split('-')[0] == '$': #accepted because in both stack we have $
                #print(f'Input "{inpt}" is accepted.')
                return threeCodeAddress
                stack.pop()
                tokens.pop()
                break
            
            elif stack[-1] in funcs:
                if stack[-1] == 'pid':
                    if tokens[-1].split('-')[0] == 'id':
                        semanticStack.append(addressCounter)
                    elif  tokens[-1].split('-')[0] == 'int':
                        semanticStack.append("#" + tokens[-1].split('-')[1])
                    addressCounter += 1
                    stack.pop()
                elif stack[-1] == 'assign':
                    top = semanticStack.pop()
                    threeCodeAddress.append(f'(:=,{semanticStack.pop()}, ,{top})')
                    stack.pop()
                elif stack[-1] == 'mult':
                    top = semanticStack.pop()
                    threeCodeAddress.append(f'(*,{semanticStack.pop()},{top},{tempAddressCounter})')
                    semanticStack.append(tempAddressCounter)
                    tempAddressCounter += 1
                    stack.pop()
                elif stack[-1] == 'add':
                    top = semanticStack.pop()
                    threeCodeAddress.append(f'(+,{semanticStack.pop()},{top},{tempAddressCounter})')
                    semanticStack.append(tempAddressCounter)
                    tempAddressCounter += 1
                    stack.pop()
                else:
                    print(f'Please specify a function fo this func{stack[-1]}.')
                    break
            
            elif stack[-1].isupper(): #if we have none terminal on top of stack
                if  tokens[-1].split('-')[0] in tableParser[stack[-1]]:
                    index = tableParser[stack[-1]][ tokens[-1].split('-')[0]] #find index from parse table
                    left, right = indexedRules[index - 1] #unpack left and right from indexed rules
                    #right = self.sanitize(right) #remove @funcs from right
                    
                    #convert string to temp list and then revresly add it to stack
                    tempList = []
                    word = ''
                    funcFlag = False
                    func = ''
                    for letter in right: # @pid id
                        if funcFlag: #detect @funcs and append to temp list
                            if letter == ' ':
                                tempList.append(func.strip())
                                funcs.add(func.strip())
                                func = ''
                                funcFlag = False
                                continue
                            else:
                                func += letter
                                continue

                        if letter == '@':
                            funcFlag = True
                        elif letter.isupper():
                            tempList.append(letter)
                        else:
                            word += letter
                            if word in self.terminals:
                                tempList.append(word)
                                word = ""                  

                    if func:
                        tempList.append(func.strip())
                        funcs.add(func.strip())
                        func = ''

                    if word:
                        if word in self.terminals:
                            tempList.append(word)
                    stack.pop()
                    stack.extend(tempList[::-1])
                    print("three address code: ", threeCodeAddress)
                    print("semantic stack: ", semanticStack)
                    print("token stack", tokens)
                    print("parse stack", stack)
                    print("\n")
                else:
                    # if we don't have rule in parse table
                    print(f'Input "{inpt}" is not accepted.')
                    break

            
            else: #if we have terminal on top of stack
                if stack[-1] in self.terminals:
                    if stack[-1] ==  tokens[-1].split('-')[0]: #if matched then pop and remove
                        stack.pop()
                        tokens.pop()
                        print("three address code: ", threeCodeAddress)
                        print("semantic stack: ", semanticStack)
                        print("token stack", tokens)
                        print("parse stack", stack)
                        print("\n")
                    else: #if not macthed print error
                        print(f'Input "{inpt}" is not accepted.')
                        break