from Token import Token

#class that implements shunting yard algorithm

class ShuntingYard:

    def __init__(self, expression):
        self.expression = expression.replace(" ", "")       #ignoriramo praznine
        self.operands = []
        self.operators = []
        self.counter = 0

    def ReadExpression(self):
        while self.counter < len(self.expression):
            if(Token.CheckIsCloseBracket(self.expression[self.counter])):       #ako je zatvorena zagrada onda izbacujemo
                while True:                                                     #operatore dok ne dodjemo do otvorene zagrade
                    if len(self.operators) == 0:
                        raise Exception("Error: Brackets are not correct!")        #ako nema otvorene zagrade --> greška
                    lastToken = self.operators[-1]
                    if Token.CheckIsOpenBracket(lastToken.label):
                        if Token.IsSameBracketType(lastToken.label, self.expression[self.counter]):
                            self.operators.pop(-1)
                            if len(self.operators) > 0 and self.operators[-1].isFunction:
                                self.operands.append(self.operators.pop(-1))        #ako su zagrade zbog f-je onda izbacimo i nju
                            break
                        else:
                            raise Exception("Error: Brackets are not correct!")     #ako zagrade nisu istog tipa --> greška
                    else:
                        self.operands.append(self.operators.pop(-1))

            elif Token.CheckIsSeparator(self.expression[self.counter]):         #dok ne dodjemo do otvorene zagrade izbacujemo operatore
                if Token.CheckIsSeparator(self.expression[self.counter-1]):
                    raise Exception("Error: Separators are not correct!")
                while True:
                    if len(self.operators) == 0:
                        raise Exception("Error: Separators are not correct!")   #ako nema otvorene zagrade --> greška
                    elif Token.CheckIsOpenBracket(self.operators[-1].label):
                        break
                    else:
                        self.operands.append(self.operators.pop(-1))
            else:
                tokenList = self.MakeToken()                    #jedan ili dva tokena(ako je izgubljen *)
                for token in tokenList:
                    if token.isFunction:                        #token f-ja --> dodamo ga u operatore
                        self.operators.append(token)
                    elif token.isOperand:                       #token operand --> dodamo ga u operande
                        self.operands.append(token)
                    elif token.isBinaryOperator:                #ako je binarni micemo operatore s stoga ako imaju prioritet veci od sadasnjeg
                        while len(self.operators) > 0:
                            if ((self.operators[-1].priority > token.priority
                                    and not Token.CheckIsOpenBracket(token.label))
                                    or self.operators[-1].isUnaryOperator):
                                self.operands.append(self.operators.pop(-1))
                            else:
                                break
                        if token.IsLeftAssociative():
                            while len(self.operators) > 0:
                                if (self.operators[-1].priority == token.priority and not
                                        Token.CheckIsOpenBracket(token.label)):
                                    self.operands.append(self.operators.pop(-1))
                                else:
                                    break
                        self.operators.append(token)
                    elif token.isUnaryOperator:
                        # while len(self.operators)>0:
                        #     if self.operators[-1].isUnaryOperator:
                        #         self.operands.append(self.operators.pop(-1))
                        self.operators.append(token)
            self.counter += 1
            print(self.operands)
            print(self.operators)
        while len(self.operators) > 0:      #sve dok stog nije prazan micemo operatore
            lastToken = self.operators[-1]
            if(Token.CheckIsOpenBracket(lastToken.label)
               or Token.CheckIsCloseBracket(lastToken.label)):
                raise Exception("Error: Brackets are not correct!")
            else:
                self.operands.append(self.operators.pop(-1))
        print(self.operands)
        print(self.operators)
    def MakeToken(self):
        tokenList = []
        if ((self.counter == 0 or Token.CheckIsOpenBracket(self.expression[self.counter-1])
                or Token.CheckIsBinaryOperator(self.expression[self.counter-1]))
                and Token.CheckIsUnaryOperator(self.expression[self.counter])):
            tokenList.append(Token(self.expression[self.counter], False, False, True, False))
        elif (Token.CheckIsBinaryOperator(self.expression[self.counter])
                or Token.CheckIsOpenBracket(self.expression[self.counter])):
            tokenList.append(Token(self.expression[self.counter], False, True, False,  False))
        elif (Token.CheckIsOperand(self.expression[self.counter]) and self.counter < len(self.expression)-1 and
                Token.CheckIsOpenBracket(self.expression[self.counter+1])):
            tokenList.append(Token(self.expression[self.counter], True, False, False, False))
        else:
            tokenList.append(Token(self.expression[self.counter], False, False, False, True))
            if self.counter < len(self.expression)-1 and Token.CheckIsOperand(self.expression[self.counter+1]):
                tokenList.append(Token("*", False, True, False, False))
        return tokenList
