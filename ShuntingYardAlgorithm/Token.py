class Token:

    UnaryOperatorsList = {"+", "-"}
    BinaryOperatorsList = {"+", "-", "*", "/", "^"}
    OpenBracketsList = {"(", "[", "{"}
    CloseBracketsList = {")", "]", "}"}

    def __init__(self, label, isFunction, isBinaryOperator, isUnaryOperator, isOperand):
        self.BinaryOperatorsPriorityDict = {"(": 0, ")" : 0, "+" : 1, "-" : 1, "*" : 2, "/" : 2, "^" : 3}
        self.label = label
        self.isFunction = isFunction
        self.isBinaryOperator = isBinaryOperator
        self.isUnaryOperator = isUnaryOperator
        self.isOperand = isOperand
        self.priority = self.GetOperatorPriority()


    @staticmethod
    def CheckIsBinaryOperator(label):
        return Token.BinaryOperatorsList.__contains__(label)

    @staticmethod
    def CheckIsUnaryOperator(label):
        return Token.UnaryOperatorsList.__contains__(label)

    @staticmethod
    def CheckIsOperand(label):
        return not (Token.CheckIsUnaryOperator(label) and Token.CheckIsBinaryOperator(label))

    @staticmethod
    def CheckIsOpenBracket(label):
        return Token.OpenBracketsList.__contains__(label)

    @staticmethod
    def CheckIsCloseBracket(label):
        return Token.CloseBracketsList.__contains__(label)



    def GetOperatorPriority(self):
        if self.isBinaryOperator:
            return self.BinaryOperatorsPriorityDict[self.label]
        else:
            return 0

