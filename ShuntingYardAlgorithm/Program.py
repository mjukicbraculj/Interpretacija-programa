from ShuntingYard import ShuntingYard

if __name__ == '__main__':
    example1 = "a+b--c+(-s+-g)"     #this example tests unary operators
    example2 = "a+b(c+d)"           #this example teste function
    example3 = "s(m(c,d)/ef)"       #left out *
    example4 = "s(m(c,d))/(ef)"
    example5 = "3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3"  #3 4 2 * 1 5 - 2 3 ^ ^ / +
    example6 = "A * (B + C)"        #A B C + *
    example7 = "A * B ^ C + D"      #A B C ^ * D +
    example8 = "A * (B + C * D) + E"    #A B C D * + * E +
    example9 = "a(3,,2*3)"            #Separators are not correct!
    example12 = "a+b(a, b)))"           #Brackets are not correct!
    example10 = "(a+b+c)^-d"
    example11 = "a+b"
    shuntingYard = ShuntingYard(example5)
    shuntingYard.ReadExpression()



