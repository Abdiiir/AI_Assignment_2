
# This function finds the most inside brackets
# It does so by taking the last "(" to appear in the
# sentence and then finding it's corresponding ")"
def findMiddleBrackets(sentence):

    idxStart = sentence.rfind("(")

    idxEnd = 0
    for i in range(idxStart, len(sentence)):
        if sentence[i] == ")":
            idxEnd = i
            break

    left = sentence[:idxStart]
    middle = sentence[idxStart+1:idxEnd]
    right = sentence[idxEnd+1:]
    return left, middle, right


# This function eliminates the Biconditional operators
# It uses the findMiddleBrackets function to find the inmost brackets
# and then checks if there are any biconditional operators in said
# bracket, and removes them if so, and then replaces the brackets "(" and ")"
# with the temporary square brackets "[" and "]".
# It repeats until there are no more brackets and biconditional operators left
# and finally replaces the temporary square brackets with the normal brackets
# to get the new sentence with the biconditionals eliminated
def eliminateBiconditional(sentence):
    while "(" in sentence:
        left, middle, right = findMiddleBrackets(sentence)

        # Checks if there are any Bicoditionals in inside bracket
        ind = middle.find("<->")
        if ind == -1:
            sentence = left + "[" + middle + "]" + right
            continue

        # Splits into left and right side of biconditional
        # And then creates new sentence with the biconditional eliminated
        middleLeft = middle[:ind]
        middleRight = middle[ind+3:]
        sentence = left +"["+ middleLeft +"->"+ middleRight +"]"+"&"+"["+ middleRight +"->"+ middleLeft +"]"+ right

    sentence = sentence.replace("[","(").replace("]",")")
    return sentence


# This funtion eliminates the implication oprerators.
# It work n the same way as the eliminateBiconditional as it finds the
# inmost bracket and then eliminates the implication operator and repeats
# until none are left.
def eliminateImplication(sentence):
    while "(" in sentence:
        left, middle, right = findMiddleBrackets(sentence)

        # Checks if there are any Implications in inside bracket
        ind = middle.find("->")
        if ind == -1:
            sentence = left + "[" + middle + "]" + right
            continue

        # Split into left and right side of implication
        # And then creates new sentence with the implication eliminated
        middleLeft = middle[:ind]
        middleRight = middle[ind+2:]
        sentence = left + "[~" + middleLeft +"|"+ middleRight +"]" + right

    sentence = sentence.replace("[","(").replace("]",")")
    return sentence


# This function applies De Morgan's Laws.
# It also starts by the inmost bracket, and then checks if there is
# a not "~" infront of that bracket. If there is it perfroms De Morgan's
# laws, otherwise it updates the brackets to the temporary square ones and
# moves on, until all brackets have been checked.
def deMorgan(sentence):
    while "(" in sentence:
        left, middle, right = findMiddleBrackets(sentence)

        if len(left) == 0:
            sentence = left + "[" + middle + "]" + right

        # If there is a not ("~") infront
        elif left[-1] == "~":
            counter = 0
            for i in range(len(middle)):
                if middle[i] == "[":
                    counter += 1
                if middle[i] == "]":
                    counter -= 1
                if middle[i] == "|" and counter == 0:
                    sentence = left[:-1] + "[~" + middle[:i] + "&~" + middle[i+1:] + "]" + right
                if middle[i] == "&" and counter == 0:
                    sentence = left[:-1] + "[~" + middle[:i] + "|~" + middle[i+1:] + "]" + right

        else:
            sentence = left + "[" + middle + "]" + right

    # Replaces temporary brackets with original ones and removes and double negates
    sentence = sentence.replace("[","(").replace("]",")").replace("~~","")
    return sentence




def distributeAndOverOr(sentence):
    while "(" in sentence:
        left, middle, right = findMiddleBrackets(sentence)
        if len(left) == 0 and len(right) == 0:
            sentence = left + "[" + middle + "]" + right

        counter = 0
        for i in range(len(middle)):
            if middle[i] == "[":
                counter += 1
            if middle[i] == "]":
                counter -= 1
            if middle[i] == "&" and counter == 0:

                # Split into left and right side of and ("&")
                middleLeft = middle[:i]
                middleRight = middle[i+1:]

                if len(right) > 1 and right[0] == "|":

                    if right[1] == "[" or right[1] == "(":
                        extra = 0
                    else:
                        extra = -1
                    counter = 0
                    for i in range(1, len(right)):
                        if right[i] == "[" or right[i] == "(":
                            counter += 1
                        if right[i] == "]" or right[i] == ")":
                            counter -= 1
                        if counter == extra-1:
                            break
                        if counter == extra:
                            sentence = left + "[" + middleLeft + "|" + right[2+extra:i] + "]&[" + middleRight + "|" + right[2+extra:i] + "]" + right[i+1+extra:]
                            break
                    break



                if len(left) > 1 and left[-1] == "|":
                    if left[-2] == ")" or left[-2] == "]":
                        extra = 0
                    else:
                        extra = -1
                    counter = 0
                    for i in range(2, len(left)+1):
                        if left[-i] == ")" or left[-i] == "]":
                            counter += 1
                        if left[-i] == "(" or left[-i] == "[":
                            counter -= 1
                        if counter == extra:
                            sentence = left[:-i-extra] + "[" + middleLeft + "|" + left[1-i:-2-extra] + "]&[" + middleRight + "|" + left[1-i:-2-extra] + "]" + right
                            break
                    break

                else:
                    sentence = left + "[" + middle + "]" + right
                    break
            if i == len(middle)-1:
                sentence = left + "[" + middle + "]" + right


    # Replaces temporary brackets with original ones and removes any double negates
    sentence = sentence.replace("[","(").replace("]",")")
    return sentence


# This function applies the previous functions to convert
# the sentence to CNF
def convertToCNF(sentence):
    print(sentence)
    sentence = eliminateBiconditional(sentence)
    print(sentence)
    sentence = eliminateImplication(sentence)
    print(sentence)
    sentence = deMorgan(sentence)
    print(sentence)
    sentence = distributeAndOverOr(sentence)
    print(sentence)
    return sentence



sentence = "a&(b->c)&((a|a<->b)|((a->b))<->(c->d))"
sentence2 = "(a<->b)&(c->(a&b))"
sentence = convertToCNF(sentence2)
