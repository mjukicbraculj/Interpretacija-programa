class Token:

    UnaryOperatorsList = {"+", "-"}
    BinaryOperatorsList = {"+", "-", "*", "/", "^"}
    OpenBracketsDict = {"(": 1, "[": 2, "{": 3}
    CloseBracketsDict = {")": 1, "]": 2, "}": 3}
    SeparatorList = {","}

    def __init__(self, label, isFunction, isBinaryOperator, isUnaryOperator, isOperand):
        self.BinaryOperatorsPriorityDict = {"(": 0, "[" : 0, "{" : 0, "+" : 1, "-" : 1, "*" : 2, "/" : 2, "^" : 3}
        self.label = label
        self.isFunction = isFunction
        self.isBinaryOperator = isBinaryOperator
        self.isUnaryOperator = isUnaryOperator
        self.isOperand = isOperand
        self.priority = self.GetOperatorPriority()

    def __repr__(self):
        return self.label + " "

    @staticmethod
    def CheckIsBinaryOperator(label):
        return Token.BinaryOperatorsList.__contains__(label)

    @staticmethod
    def CheckIsUnaryOperator(label):
        return Token.UnaryOperatorsList.__contains__(label)

    @staticmethod
    def CheckIsOperand(label):
        return not (Token.CheckIsUnaryOperator(label) or Token.CheckIsBinaryOperator(label) or
                    Token.CheckIsOpenBracket(label) or Token.CheckIsCloseBracket(label) or
                    Token.CheckIsSeparator(label))

    @staticmethod
    def CheckIsOpenBracket(label):
        return Token.OpenBracketsDict.keys().__contains__(label)

    @staticmethod
    def CheckIsCloseBracket(label):
        return Token.CloseBracketsDict.keys().__contains__(label)

    @staticmethod
    def CheckIsSeparator(label):
        return Token.SeparatorList.__contains__(label)


    def GetOperatorPriority(self):
        if self.isBinaryOperator:
            return self.BinaryOperatorsPriorityDict[self.label]
        else:
            return 0


    def IsLeftAssociative(self):
        priority = self.GetOperatorPriority()
        if(priority > 0 and priority < 3):
            return True
        else:
            return False

    @staticmethod
    def IsSameBracketType(open, close):
        if Token.OpenBracketsDict[open] == Token.CloseBracketsDict[close]:
            return True
        else:
            return False
