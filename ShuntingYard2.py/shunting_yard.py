from tip import Token, Tokenizer, AST, vrsta, Parser
import enum

class Aritmetika(enum.Enum):
    KRAJ, GREŠKA, PRAZNO = 0, 1, 3
    BROJ = 4
    OTVORENA = '([{'
    ZATVORENA = ')]}'
    IME = 'a'
    PLUS = '+'
    MINUS = '-'
    PUTA = '*'
    DIJELJENO = '/'
    POTENICIJA = '^'
    ZAREZ = ','



operands = []
operators = []

prioriteti = {}
prioriteti[Aritmetika.PLUS] = prioriteti[Aritmetika.MINUS] = 1
prioriteti[Aritmetika.PUTA] = prioriteti[Aritmetika.DIJELJENO] = 2
prioriteti[Aritmetika.POTENICIJA] = 3
binarni_op = [Aritmetika.PLUS, Aritmetika.MINUS, Aritmetika.PUTA, Aritmetika.DIJELJENO,
              Aritmetika.POTENICIJA]

broj_argumenata = 0

obrnuta_zagarada = {}
obrnuta_zagarada['('] = ')'
obrnuta_zagarada['{'] = '}'
obrnuta_zagarada['['] = ']'

#imena moraju počinjati sa slovom, a mogu sadržavati i znamenke

def algorithm(expression):
    parser = Parser(lex(expression))
    operators.clear()
    operands.clear()
    global broj_argumenata
    broj_argumenata = 0
    while parser.pogledaj().tip != Aritmetika.KRAJ:
        token = parser.čitaj()
        if token.tip == Aritmetika.BROJ: #ako je broj ide u operande
            operands.append(MakeAST(token))
            if (len(operators) > 1 and
                operators[-2].tip == Aritmetika.IME):   #znaci da je f-ja u operatorima
                broj_argumenata = broj_argumenata +1
        elif token.tip == Aritmetika.IME:
            token1 = parser.pogledaj()
            if token1.tip == Aritmetika.OTVORENA:       #ako je f-ja ide u operatore
                operators.append(token)
            else:                               #inače je varijabla, operand
                operands.append(MakeAST(token))
                if (len(operators) > 1 and
                            operators[-2].tip == Aritmetika.IME):
                    broj_argumenata = broj_argumenata + 1
        elif token.tip == Aritmetika.ZAREZ:
            token1 = parser.pogledaj()
            if(token1.tip == Aritmetika.ZAREZ):
                raise Exception("Greška u pisanju zareza u funkciji.")
            while True:
                if len(operators) == 0:
                    raise Exception("Greška u pisanju zareza u funkciji.")
                elif operators[-1].tip == Aritmetika.OTVORENA:
                    break
                else:
                    operands.append(operators.pop(-1))
        elif (token.tip in binarni_op):
            while len(operators) > 0:
                if (operators[-1].tip is not Aritmetika.OTVORENA
                    and prioriteti[operators[-1].tip] > prioriteti[token.tip]):
                        operands.append(MakeAST(operators.pop(-1)))
                else:
                    break
            if token.tip != Aritmetika.POTENICIJA:
                while len(operators) > 0:
                    if(operators[-1].tip is not Aritmetika.OTVORENA
                       and prioriteti[operators[-1].tip] >= prioriteti[token.tip]):
                            operands.append(MakeAST(operators.pop(-1)))
                    else:
                        break
            operators.append(token)
        elif token.tip == Aritmetika.ZATVORENA:
            while True:
                if len(operators) == 0:
                    raise  Exception('Greška: Zagrade nisu dobro postavljene')
                if operators[-1].tip == Aritmetika.OTVORENA:
                    if obrnuta_zagarada[operators[-1].sadržaj] == token.sadržaj:
                        operators.pop(-1)
                        if len(operators) > 0 and operators[-1].tip == Aritmetika.IME:
                            operands.append(MakeAST(operators.pop(-1), True))
                        break
                    else:
                        raise Exception('Greška: Zagrade nisu dobro postavljene')
                else:
                    operands.append(MakeAST(operators.pop(-1)))
        elif token.tip == Aritmetika.OTVORENA:
            operators.append(token)
        else:
            raise Exception("Greška nepoznati token:", token.sadržaj)

    while len(operators) > 0:
        lastToken = operators[-1]
        if lastToken.tip in [Aritmetika.OTVORENA, Aritmetika.ZATVORENA]:
            raise Exception("Greska: zagrade nisu dobro postavljene!")
        else:
            operands.append(MakeAST(operators.pop(-1)))
    return operands


def MakeAST(token, isFunction = False):
    if token.tip in [Aritmetika.BROJ, Aritmetika.IME] and not isFunction:
        return AST(stablo = 'operand', value = token.sadržaj)
    elif token.tip in binarni_op:
        if len(operands) < 2:
            raise Exception("Nedovoljno operanada za " +  token.sadržaj)
        else:
            prvi = operands.pop(-1)
            drugi = operands.pop(-1)
            return AST(stablo = str(token),
                       lijevo=str(drugi),
                       desno = str(prvi))
    elif token.tip is Aritmetika.IME:       #ovo je f-ja
        if len(operands) < broj_argumenata:
            raise Exception("Nedovoljno operanada za " + token.sadržaj)
        else:
            ast = AST(stablo = str(token))
            ast.argumenti = []
            for i in range(broj_argumenata):
                ast.argumenti.append(str(operands.pop(-1)))
            ast.argumenti.reverse()
            return ast

def lex(expression):
    lexer = Tokenizer(expression)
    minus_operator = False
    while True:
        znak = lexer.pogledaj()
        vrsta_znaka = vrsta(znak)
        if vrsta_znaka == 'kraj': yield Token(Aritmetika.KRAJ, ''); return
        elif vrsta_znaka == 'praznina': Token(Aritmetika.PRAZNO, lexer.praznine())
        elif vrsta_znaka == 'znamenka':
            yield Token(Aritmetika.BROJ, lexer.broj())
            minus_operator = True
        elif vrsta_znaka == 'slovo':
            yield Token(Aritmetika.IME, lexer.ime())
            minus_operator = True
        elif znak in '*+/^':
            yield Token(Aritmetika(znak), lexer.čitaj())
            minus_operator = False
        elif znak == '-':
            if minus_operator:
                yield Token(Aritmetika(znak), lexer.čitaj())
                minus_operator = False
            else:
                prefix = lexer.čitaj()
                znak1 = lexer.pogledaj()
                vrsta_znak1 = vrsta(znak1)
                if vrsta_znak1 == 'znamenka':
                    yield Token(Aritmetika.BROJ, prefix+lexer.broj())
                elif vrsta_znak1 == 'slovo':
                    yield Token(Aritmetika.IME, prefix+lexer.ime())
                else:
                    yield Token(Aritmetika.GREŠKA, lexer.čitaj())
                minus_operator = True
        elif znak in ')]}':
            yield Token(Aritmetika.ZATVORENA, lexer.čitaj())
            minus_operator = True
        elif znak in '([{':
            yield Token(Aritmetika.OTVORENA, lexer.čitaj())
        elif znak == ',':
            yield Token(Aritmetika.ZAREZ, lexer.čitaj())
        else:
            yield Token(Aritmetika.GREŠKA, lexer.čitaj())


if __name__ == '__main__':
    expression = 'f(2)+3'
    expression1 = '3^4^5'
    expression2 = '3+4+5'
    expression3='(333+2*f(4,5,66))'
    expression4 = '(3+4]'
    expression5 = '(3+6)]'
    example5 = "3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3"
    example6 = "a|e"
    #print(*lex(expression), sep='\n')
    print(algorithm(expression))
    print(algorithm(expression1))
    print(algorithm(expression2))
    print(algorithm(expression3))
    #print(algorithm(expression5))
    print(algorithm(example5))
