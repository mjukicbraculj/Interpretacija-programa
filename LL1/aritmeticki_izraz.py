from tip import Token, Tokenizer, Parser, Buffer, AST, vrsta
import enum
operators = ['+', '*', '^']


class Aritmetika(enum.Enum):
    GREŠKA, KRAJ, PRAZNO = 1, 2, 3
    BROJ = 4
    PLUS = '+'
    PUTA = '*'
    POTENCIJA = "^"
    OTVORENA = '('
    ZATOVRENA = ')'


#ptp da varijable ne smiju početi sa znamenkom
def lex(expression):
    lexer = Tokenizer(expression)
    while True:
        letter = lexer.pogledaj()
        letter_type = vrsta(letter)
        if letter_type == 'kraj': yield Token(Aritmetika.KRAJ, ''); return
        elif letter_type == 'praznina': Token(Aritmetika.PRAZNO, lexer.praznine())
        elif letter_type == 'znamenka' : yield Token(Aritmetika.BROJ, lexer.broj())
        elif letter in '+*^':
            yield Token(Aritmetika(letter), lexer.čitaj())
        elif letter == '(':
            yield Token(Aritmetika.OTVORENA, lexer.čitaj())
        elif letter == ')':
            yield Token(Aritmetika.ZATOVRENA, lexer.čitaj())
        else:
            yield Token(Aritmetika.GREŠKA, lexer.čitaj())


class AritmParser(Parser):
    def izraz(self):        #na razini zbrajanja
        f1 = self.faktor()
        if(self.granaj(Aritmetika.PLUS, Aritmetika.PUTA, Aritmetika.POTENCIJA,
                       Aritmetika.ZATOVRENA, Aritmetika.KRAJ) == Aritmetika.PLUS):
            self.pročitaj(Aritmetika.PLUS)
            f2 = self.izraz()
            return AST(stablo = 'zbroj', lijevo = f2, desno = f1)
        else:
            return f1

    def faktor(self):       #na razini množenja
        f1 = self.potencija()
        if(self.granaj(Aritmetika.PLUS, Aritmetika.PUTA, Aritmetika.POTENCIJA,
                       Aritmetika.KRAJ, Aritmetika.ZATOVRENA) == Aritmetika.PUTA):
            self.pročitaj(Aritmetika.PUTA)
            f2 = self.faktor()
            return AST(stablo = 'umnozak', lijevo = f2, desno = f1)
        else:
            return f1

    def potencija(self):        #na razini potenciranja
        f1 = self.izraz_zagrade()
        if (self.granaj(Aritmetika.PLUS, Aritmetika.PUTA,Aritmetika.ZATOVRENA,
                        Aritmetika.POTENCIJA, Aritmetika.KRAJ) == Aritmetika.POTENCIJA):
            self.pročitaj(Aritmetika.POTENCIJA)
            f2 = self.potencija()
            return AST(stablo = 'potencija', lijevo = f2, desno = f1)
        else:
            return f1


    def izraz_zagrade(self):        #na razini zagrada
        if self.granaj(Aritmetika.BROJ, Aritmetika.OTVORENA) == Aritmetika.BROJ:
            return self.pročitaj(Aritmetika.BROJ)
        else:
            self.pročitaj(Aritmetika.OTVORENA)
            u_zagradi = self.izraz()
            self.pročitaj(Aritmetika.ZATOVRENA)
            return u_zagradi


def parse(expression):
    *tokeni, kraj = lex(expression)
    assert kraj == Token(Aritmetika.KRAJ, '')
    tokeni.reverse()
    for token in tokeni:
        if token.tip == Aritmetika.OTVORENA: token.tip = Aritmetika.ZATOVRENA
        elif token.tip == Aritmetika.ZATOVRENA: token.tip = Aritmetika.OTVORENA
    tokeni.append(kraj)
    parser = AritmParser(tokeni)
    rezultat = parser.izraz()
    parser.pročitaj(Aritmetika.KRAJ)
    return rezultat


if __name__ == '__main__':
    expression = "((22+2)*3)^76"
    print(*lex(expression), sep='\n')
    print(parse(expression))