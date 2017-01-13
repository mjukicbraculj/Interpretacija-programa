from Token import Token

#class that implements shunting yard algorithm

class ShuntingYard:

    def __init__(self, expression):
        self.expression = expression
        self.operands = []
        self.operators = []
        self.counter = 0

    def ReadExpression(self):
        while self.counter < len(self.expression):
            if(Token.CheckIsCloseBracket(self.expression[self.counter])):
                while True:
                    if len(self.operators) == 0:
                        raise Exception("Error: Brackets are not correct!")
                    lastToken = self.operators[-1]
                    if Token.CheckIsOpenBracket(lastToken.label):
                        if Token.IsSameBracketType(lastToken.label, self.expression[self.counter]):
                            self.operators.pop(-1)
                            if self.operators[-1].isFunction:
                                self.operands.append(self.operators.pop(-1))
                            break
                        else:
                            raise Exception("Error: Brackets are not correct!")
                    else:
                        self.operands.append(self.operators.pop(-1))

            elif Token.CheckIsSeparator(self.expression[self.counter]):
                while True:
                    if len(self.operators) == 0:
                        raise Exception("Error: Separators are not correct!")
                    elif Token.CheckIsOpenBracket(self.operators[-1].label):
                        break
                    else:
                        self.operands.append(self.operators.pop(-1))
            else:
                token = self.MakeToken()
                if token.isFunction:
                    self.operators.append(token)
                elif token.isOperand:
                    self.operands.append(token)
                elif token.isBinaryOperator:
                    while len(self.operators) > 0:
                        if self.operators[-1].priority > token.priority:
                            self.operands.append(self.operators.pop(-1))
                        else:
                            break
                    if token.IsLeftAssociative():
                        while len(self.operators) > 0:
                            if self.operators[-1].priority == token.priority:
                                self.operands.append(self.operators.pop(-1))
                            else:
                                break
                    self.operators.append(token)
            self.counter += 1
            self.__repr__()
        while len(self.operators) > 0:
            lastToken = self.operators[-1]
            if(Token.CheckIsOpenBracket(lastToken.label)
               or Token.CheckIsCloseBracket(lastToken.label)):
                raise Exception("Error: Brackets are not correct!")
            else:
                self.operands.append(self.operators.pop(-1))
        self.__repr__()
    def MakeToken(self):
        if ((self.counter == 0 or Token.CheckIsOpenBracket(self.expression[self.counter-1])
                or Token.CheckIsBinaryOperator(self.expression[self.counter-1]))
                and Token.CheckIsUnaryOperator(self.expression[self.counter])):
            return Token(self.expression[self.counter], False, False, True, False)
        elif (Token.CheckIsBinaryOperator(self.expression[self.counter])
                or Token.CheckIsOpenBracket(self.expression[self.counter])):
            return Token(self.expression[self.counter], False, True, False,  False)
        elif (Token.CheckIsOperand(self.expression[self.counter]) and
                Token.CheckIsOpenBracket(self.expression[self.counter+1])):
            return Token(self.expression[self.counter], True, False, False, False)
        else:
            return Token(self.expression[self.counter], False, False, False, True)

    def __repr__(self):
        print(self.operands)
        print(self.operators)
