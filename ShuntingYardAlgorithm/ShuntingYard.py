from Token import Token
from AST import AST
from collections import OrderedDict

#class that implements shunting yard algorithm

class ShuntingYard:

    def __init__(self, expression):
        self.expression = expression.replace(" ", "")       #ignoriramo praznine
        self.operands = []                                  #keeps AST objects
        self.operators = []
        self.counter = 0

    def ReadExpression(self):
        while self.counter < len(self.expression):
            if(Token.CheckIsCloseBracket(self.expression[self.counter])):       #ako je zatvorena zagrada onda izbacujemo
                self.ProcessCloseBracket()
            elif Token.CheckIsSeparator(self.expression[self.counter]):         #dok ne dodjemo do otvorene zagrade izbacujemo operatore
                self.ProcessSeparator()
            else:
                tokenList = self.MakeToken()                    #jedan ili dva tokena(ako je izgubljen *)
                for token in tokenList:
                    if token.isFunction:                        #token f-ja --> dodamo ga u operatore
                        self.operators.append(token)
                    elif token.isOperand:                       #token operand --> dodamo ga u operande
                        self.operands.append(self.MakeAST(token))
                    elif token.isBinaryOperator:                #ako je binarni micemo operatore s stoga ako imaju prioritet veci od sadasnjeg
                        while len(self.operators) > 0:
                            if ((self.operators[-1].priority > token.priority
                                    and not Token.CheckIsOpenBracket(token.label))
                                    or self.operators[-1].isUnaryOperator):
                                self.operands.append(self.MakeAST(self.operators.pop(-1)))
                            else:
                                break
                        if token.IsLeftAssociative():
                            while len(self.operators) > 0:
                                if (self.operators[-1].priority == token.priority and not
                                        Token.CheckIsOpenBracket(token.label)):
                                    self.operands.append(self.MakeAST(self.operators.pop(-1)))
                                else:
                                    break
                        self.operators.append(token)
                    elif token.isUnaryOperator:
                        # while len(self.operators)>0:
                        #     if self.operators[-1].isUnaryOperator:
                        #         self.operands.append(self.operators.pop(-1))
                        self.operators.append(token)
            self.counter += 1
            for i in range (len(self.operands)):
                print(self.operands[i])
            print(self.operators)
        while len(self.operators) > 0:      #sve dok stog nije prazan micemo operatore
            lastToken = self.operators[-1]
            if(Token.CheckIsOpenBracket(lastToken.label)
               or Token.CheckIsCloseBracket(lastToken.label)):
                raise Exception("Error: Brackets are not correct!")
            else:
                self.operands.append(self.MakeAST(lastToken))
                self.operators.pop(-1)
        print(self.operands)
        print(self.operators)

    def MakeAST(self, token):
        if token.isOperand:
            return AST(tree='operand', value = token.label)
        else:
            #print("STVARAM " + token.label + " " + str(token.argsNum) + "duljina operands je " + str(len(self.operands)))
            if len(self.operands) >= token.argsNum:
                args = OrderedDict()
                if(token.isFunction):
                    args['tree'] = 'funkcija:'+ token.label
                else:
                    args['tree']='operator'+token.label
                while token.argsNum > 0:
                    args['arg'+str(token.argsNum)]=self.operands.pop(-1)
                    token.argsNum-=1
                args = OrderedDict(reversed(list(args.items())))
                #print(list(args.items()))
                return AST(**args)
            else:
                raise Exception("Error: number od operands is not correct!")



    def ProcessSeparator(self):
        if Token.CheckIsSeparator(self.expression[self.counter - 1]):
            raise Exception("Error: Separators are not correct!")
        while True:
            if len(self.operators) == 0:
                raise Exception("Error: Separators are not correct!")  # ako nema otvorene zagrade --> greška
            elif Token.CheckIsOpenBracket(self.operators[-1].label):
                self.operators[-2].argsNum += 1
                break
            else:
                self.operands.append(self.operators.pop(-1))

    def ProcessCloseBracket(self):
        while True:  # operatore dok ne dodjemo do otvorene zagrade
            if len(self.operators) == 0:
                raise Exception("Error: Brackets are not correct!")  # ako nema otvorene zagrade --> greška
            lastToken = self.operators[-1]
            if Token.CheckIsOpenBracket(lastToken.label):
                if Token.IsSameBracketType(lastToken.label, self.expression[self.counter]):
                    self.operators.pop(-1)
                    if len(self.operators) > 0 and self.operators[-1].isFunction:
                        self.operands.append(self.MakeAST(self.operators.pop(-1)))  # ako su zagrade zbog f-je onda izbacimo i nju
                    break
                else:
                    raise Exception("Error: Brackets are not correct!")  # ako zagrade nisu istog tipa --> greška
            else:
                self.operands.append(self.MakeAST(self.operators.pop(-1)))

    def MakeToken(self):
        tokenList = []
        if ((self.counter == 0 or Token.CheckIsOpenBracket(self.expression[self.counter-1])
                or Token.CheckIsBinaryOperator(self.expression[self.counter-1]))
                and Token.CheckIsUnaryOperator(self.expression[self.counter])):
            tokenList.append(Token(self.expression[self.counter], False, False, True, False, 1))
        elif (Token.CheckIsBinaryOperator(self.expression[self.counter])
                or Token.CheckIsOpenBracket(self.expression[self.counter])):
            tokenList.append(Token(self.expression[self.counter], False, True, False,  False, 2))
        elif (Token.CheckIsOperand(self.expression[self.counter]) and self.counter < len(self.expression)-1 and
                Token.CheckIsOpenBracket(self.expression[self.counter+1])):
            try:
                if Token.CheckIsCloseBracket(self.expression[self.counter+2]):
                    argNum = 0
                else:
                    argNum = 1
            except:
                raise Exception('Error: function brackets!')
            tokenList.append(Token(self.expression[self.counter], True, False, False, False, argNum))
        else:
            tokenList.append(Token(self.expression[self.counter], False, False, False, True, 0))
            if self.counter < len(self.expression)-1 and Token.CheckIsOperand(self.expression[self.counter+1]): #kada ispustimo *
                tokenList.append(Token("*", False, True, False, False, 2))
        return tokenList
