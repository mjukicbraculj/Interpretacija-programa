from tip import Parser, Token, Tokenizer, AST, vrsta
import enum

# UPDATE table_name
# SET column1=value1,column2=value2,...
# WHERE some_column=some_value;

# INSERT INTO table_name
# VALUES (value1,value2,value3,...);

# INSERT INTO table_name (column1,column2,column3,...)
# VALUES (value1,value2,value3,...);

class SQL(enum.Enum):
    INSERT = 'INSERT'
    INTO = 'INTO'
    VALUES = 'VALUES'
    OPEN_B = '('
    CLOSE_B = ')'
    COMMA = ','
    UPDATE = 'UPDATE'
    SET = 'SET'
    WHERE = 'WHERE'
    NAME = 'NAME'
    END = ''
    ERROR = '\x00'
    EMPTY = '\t\n'

KEYWORDS = 'INSERT INTO VALUES UPDATE SET WHERE'.split()
Operators = ['+', '-', '=', '*', '/']

class SQLParser(Parser):
    def insert(self):
        return ''

    def update(self):
        naredba = AST(stablo='naredba', vrsta=SQL.UPDATE)
        self.pročitaj(SQL.UPDATE)
        naredba.tablica = self.pročitaj(SQL.NAME)
        self.pročitaj(SQL.SET)
        print(naredba, 'je sadasnje stablo')
        naredba.stupci = []
        naredba.vrijednosti = []
        naredba.stupci_uvjet = []
        naredba.vrijednosti_uvjet = []
        while self.granaj(SQL.NAME, 'operator', SQL.WHERE) is not SQL.WHERE:
            naredba.stupci.append(self.pročitaj(SQL.NAME))
            self.pročitaj('operator')
            naredba.vrijednosti.append(self.pročitaj(SQL.NAME))
        self.pročitaj(SQL.WHERE)
        while self.granaj(SQL.NAME, 'operator', SQL.END) is not SQL.END:
            naredba.stupci_uvjet.append(self.pročitaj(SQL.NAME))
            self.pročitaj('operator')
            naredba.vrijednosti_uvjet.append(self.pročitaj(SQL.NAME))
        return naredba


    def line(self):
        naredba = self.granaj(SQL.UPDATE, SQL.INSERT)
        if naredba == SQL.UPDATE:
            return self.update()
        elif naredba == SQL.INSERT:
            return self.insert()

def parse(expression):
    parser = SQLParser(lex(expression))
    stablo = parser.line()
    parser.pročitaj(SQL.END)
    return stablo


def lex(expression):
    lexer = Tokenizer(expression)
    while True:
        letter = lexer.pogledaj()
        letter_type = vrsta(letter)
        if letter_type == 'kraj': yield Token(SQL.END, ''); return
        elif letter_type == 'praznina': Token(SQL.EMPTY, lexer.praznine())
        elif letter_type == 'slovo' or letter_type == 'znamenka':
            ime = lexer.ime()
            ime = ime.upper()
            if ime in KEYWORDS:
                yield Token(SQL[ime], ime)
            else:
                yield Token(SQL.NAME, ime)
        elif letter_type == 'ostalo' and letter in Operators:
            yield Token('operator', lexer.čitaj())
        else:
            yield Token(SQL.ERROR, lexer.čitaj())



if __name__ == '__main__':
    expression = '''update animal
                    set age=10
                    where name=Spot'''
    expression1 ='update animal set age=10 where name=Spot'
    print(*lex(expression1), sep='\n')
    print(parse(expression1))
