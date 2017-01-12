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
                print("zatvorena zagrada")
            else:
                token = self.MakeToken()
            self.counter += 1

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


