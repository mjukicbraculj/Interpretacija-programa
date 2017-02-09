from tip import Tokenizer, Buffer, Token, Parser

#grammar:
#Stmt -> if Sxpr then Stmt else Stmt|
#       while Sxp do Stmt |
#       begin Stmt end
#Stmts -> Stmt;Stmts | eps
#Exp -> id

Term = 0
Rule = 1


#Termminals
T_IF = 0
T_THEN = 1
T_ELSE = 2
T_WHILE = 3
T_DO = 4
T_BEGIN = 5
T_END = 6
T_ID = 7
T_SEMICOLON = 8
T_ERROR = 9
T_KRAJ = 10
T_EPS = 11

#Non-terminals
N_STMT = 0
N_STMTS = 1
N_EXPR = 2

#parse table
parse_table = [
    [0, -1, -1, 1, -1, 2, -1, -1, -1, -1, -1, -1],
    [3, -1, -1, 3, -1, 3, 4, -1, -1, -1, 4, -1],
    [-1, -1, -1, -1, -1, -1, -1, 5, -1, -1, -1, -1]]

rules = [[(Term, T_IF), (Rule, N_EXPR), (Term, T_THEN), (Rule, N_STMT), (Term, T_ELSE), (Rule, N_STMT)],
         [(Term, T_WHILE), (Rule, N_EXPR), (Term, T_DO), (Rule, N_STMT)],
         [(Term, T_BEGIN), (Rule, N_STMTS), (Term, T_END)],
         [(Rule, N_STMT), (Term, T_SEMICOLON), (Rule, N_STMTS)],
         [(Term, T_EPS)],
         [(Term, T_ID)]]

stack = [(Term, T_KRAJ), (Rule, N_STMTS)]

def ll1_lex(expression):
    lexer = Tokenizer(expression)
    while True:
        znak = lexer.pogledaj()
        if znak == ';':
            lexer.čitaj()
            lexer.praznine()
            yield Token(T_SEMICOLON, ';')
        else:
            word = lexer.ime()
            lexer.praznine()        #ovo da pojede sve praznine
            if word == 'if' : yield Token(T_IF, 'if')
            elif word == 'then': yield Token(T_THEN, 'then')
            elif word == 'else': yield Token(T_ELSE, 'else')
            elif word == 'while': yield Token(T_WHILE, 'while')
            elif word == 'do': yield Token(T_DO, 'do')
            elif word == 'begin': yield Token(T_BEGIN, 'begin')
            elif word == 'end': yield Token(T_END, 'end')
            elif word == 'id': yield Token(T_ID, 'id')
            elif word == '': yield Token(T_KRAJ, None); return
            else:
                yield Token(T_ERROR, word)


def ll1_parse(expression):
    parser = Parser(ll1_lex(expression))
    while len(stack) > 0:
        (s_type, s_value) = stack.pop()
        if s_type == Term and s_value != T_EPS and s_value != T_KRAJ:
            obradio = parser.pročitaj(s_value)
            print(obradio.sadržaj, "je obradjenji token")
        elif s_type == Rule:
            # gledamo u tablici kojim pravilom cemo zamijeniti pravilo, to određujemo prema dolazećem tokenu
            rule = parse_table[s_value][parser.granaj(*range(11))]
            if(rule == -1):
                raise Exception("pravilo je -1, nije dobro")
            for i in reversed(rules[rule]):
                stack.append(i)


if __name__ == '__main__':
    #print(*ll1_lex("if id then begin end else begin end"), sep="\n")
    #ll1_parse("if id then begin end else begin end")
    #print(*ll1_lex("if id then begin end else begin end; while id do begin end"), sep='\n')
    ll1_parse("if id then begin end else begin end; while id do begin end; begin end;")