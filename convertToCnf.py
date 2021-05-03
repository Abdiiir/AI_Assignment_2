from sympy.logic.boolalg import to_cnf

def removeBiconditional(sentence):
    
    # Checks if there are any Bicoditionals
    ind = sentence.find("<->")
    if ind == -1:
        return to_cnf(sentence, True, True)
    
    # Splits into left and right side of biconditional
    leftAll = sentence[:ind]
    rightAll = sentence[ind+3:]
    
    # Finds where the biconditional bracket ends
    counter = 1
    for x in range(len(leftAll)-1,-1,-1):
        char = leftAll[x]
        if char == ")":
            counter += 1
        elif char == "(":
            counter -= 1
            
        if counter == 0:
            split = x
            break
    
    # Splits into part contained in biconditional and the other
    leftExtra = leftAll[:split]
    leftBi = leftAll[split:]+")"
    
    # Same for right side
    counter = 1
    for x in range(len(rightAll)):
        char = rightAll[x]
        if char == "(":
            counter += 1
        elif char == ")":
            counter -= 1
            
        if counter == 0:
            split = x
            break
    # Same
    rightBi = "(" + rightAll[:split+1]
    rightExtra = rightAll[split:-1]
    
    # Make new sentence without biconditionals
    newBi = leftExtra +"("+ leftBi +">>"+ rightBi +")"+"&"+"("+ rightBi +">>"+ leftBi +")"+ rightExtra
    print(newBi)
    return removeBiconditional(newBi)
    

sentence = "(a&(b>>c)&(a|(a&b)<->b)|((a>>b)<->(c>>d)))"

cnf = removeBiconditional(sentence)
print(cnf)



