Words = ['PROGRAM','PROCEDURE','TYPE','VAR','IF',   # reserved words
        'THEN','ELSE','FI','WHILE','DO',
        'ENDWH','BEGIN','END','READ','WRITE',
        'ARRAY','OF','RECORD','RETURN',
        'INTEGER','CHAR']                          # Type
SymbolsName = {         # state 3
    '=': 'EQ',
    '<': 'LT',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'TIMES',
    '/': 'OVER',
    '(': 'LPAREN',
    ')': 'RPAREN',
    '.': 'DOT',
    ':': 'COLON',
    ';': 'SEMI',
    ',': 'COMMA',
    '[': 'LMIDPAREN',
    ']': 'RMIDPAREN',
    ':=': 'ASSIGN',
    '..': 'UNDERANGE'
}
DFATable= [[1, 2, 3, 4, 3, 6, 12, 7, 9, 12],
           [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [12, 12, 12, 12, 5, 12, 12, 12, 12, 12],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [6, 6, 6, 6, 6, 6, 0, 6, 6, 6],  # comment
           [0, 0, 0, 0, 0, 0, 0, 8, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [10, 10, 12, 12, 12, 12, 12, 12, 12, 12],
           [12, 12, 12, 12, 12, 12, 12, 12, 11, 12],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def char2type(c):
    symbols = '+-*/();[]<, '
    types = {
        ':': 3,
        '=': 4,
        '{': 5,
        '}': 6,
        '.': 7,
        '\'': 8
    }
    if c.isalpha(): return 0
    elif c.isdigit(): return 1
    elif c in symbols: return 2
    elif c in types: return types.get(c, None)
    else: return 9

def getToken(currentState, words):
    if currentState == 1:  # ID or reserved words
        if words.upper() in Words: return (words.upper(), '-')
        else: return ('ID', words)
        # 判断是否 合法 7aa === ===
    elif currentState == 2:
        return ('INTC', words)
    elif currentState == 3 or currentState == 5 or currentState == 8:
        return (SymbolsName[words], '-')
    elif currentState == 7:
        return ('EOF', '-')
    elif currentState == 11:
        return ('CHARC', words[1])
    elif currentState == 12:
        return ('ERROR', '-')

def scanner(file):
    Tokens = []
    Buffer = ''
    now = 0  # current state
    lineIndex = 1
    for ch in file:
        input = char2type(ch)
        next = DFATable[now][input]
        if next == 0:
            if now != 6:   # omit commemt
                LexType, Sem = getToken(now, Buffer)
                Tokens.append([lineIndex, LexType, Sem])
                # print([lineIndex, LexType, Sem])
            # current char is useless, initialize the state
            if ch == ' ' or ch == '\n':
                Buffer = ''
                now = 0
            # current char is useful
            else:
                Buffer = ch
                now = DFATable[0][char2type(ch)]
        else:
            Buffer += ch
            now = next
        if ch == '\n': lineIndex += 1
    return Tokens

def readSrcCode(srcFileName):
    fp = open(srcFileName)
    ## read the source code line by line
    file = ''
    while True:
        line = fp.readline()
        if not line: break
        if line != '\n':
            # get rid of extra space
            line = ' '.join(line.split())
            file += line + '\n'
    fp.close()
    return file

def output(tgtFileName, Tokens):
    text = ''
    for Token in Tokens:
        text += str(Token[0]) + ' ' + Token[1] + ' ' + Token[2] + '\n'
    # Write to file
    f = open(tgtFileName, 'w')
    f.write(text)
    f.close()

if __name__ == '__main__':
    srcFileName = './data/sourceCode1.txt'
    # srcFileName = './data/test.txt'
    tgtFileName = './out/tokens.txt'

    file = readSrcCode(srcFileName)
    Tokens = scanner(file)
    output(tgtFileName, Tokens)
