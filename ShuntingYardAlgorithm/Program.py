from ShuntingYard import ShuntingYard

if __name__ == '__main__':
    example1 = "a+b--c+(-s+-g)"     #this example tests unary operators
    example2 = "a+b(c+d)"           #this example teste function token
    shuntingYard = ShuntingYard(example2)
    shuntingYard.ReadExpression()
    print("kraj")
