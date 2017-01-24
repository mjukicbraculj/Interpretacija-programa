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
    example13 = 'a+b()'
    example14 = '2 + 3 -'
    shuntingYard = ShuntingYard(example5)
    shuntingYard.ReadExpression()


#example5 [operator+(arg1=operand(value=3), arg2=operator/(arg1=operator*(arg1=operand(value=4), arg2=operand(value=2)), arg2=operator^(arg1=operator-(arg1=operand(value=1), arg2=operand(value=5)), arg2=operator^(arg1=operand(value=2), arg2=operand(value=3)))))]
#example1 [operator+(arg1=operator-(arg1=operator+(arg1=operand(value=a), arg2=operand(value=b)), arg2=operator-(arg1=operand(value=c))), arg2=operator+(arg1=operator-(arg1=operand(value=s)), arg2=operator-(arg1=operand(value=g))))]
#example2 [operator+(arg1=operand(value=a), arg2=funkcija:b(arg1=operator+(arg1=operand(value=c), arg2=operand(value=d))))]
#example3 [funkcija:s(arg1=operator*(arg1=operator/(arg1=funkcija:m(arg1=operand(value=c), arg2=operand(value=d)), arg2=operand(value=e)), arg2=operand(value=f)))]
#example4 [operator/(arg1=funkcija:s(arg1=funkcija:m(arg1=operand(value=c), arg2=operand(value=d))), arg2=operator*(arg1=operand(value=e), arg2=operand(value=f)))]
#example5 [operator*(arg1=operand(value=A), arg2=operator+(arg1=operand(value=B), arg2=operand(value=C)))]
#example13 [operator+(arg1=operand(value=a), arg2=funkcija:b())]
#example14 Exception: Error: number od operands is not correct!
#example9 Exception: Error: Separators are not correct!
#example12 Exception: Error: Brackets are not correct!