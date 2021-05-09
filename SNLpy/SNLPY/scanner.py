#!/usr/bin/env python
'''
# 文件 scanner.py
# 说明 实现词法扫描，基于python实现
# 作者 lkk
'''
import sys, os, pickle
from enum import Enum
from globals import LexType, Token, Log
from util import Lexical

# 定义全局变量
global theCodeArray, inlinePos, linePos, tokenList, currentPos, prePos, TAG, LOG, lexicalCache

# 有限自动机状态集合
class StateType(Enum):
    START = 1
    INASSIGN = 2
    INRANGE = 3
    INCOMMENT = 4
    INNUM = 5
    INID = 6
    INCHAR = 7
    DONE = 8

# 保留字集合
reservedWords = {
    "program": LexType.PROGRAM, "type": LexType.TYPE, "var": LexType.VAR, "procedure": LexType.PROCEDURE,
    "begin": LexType.BEGIN, "end": LexType.END, "array": LexType.ARRAY, "of": LexType.OF, "record": LexType.RECORD,
    "if": LexType.IF, "then": LexType.THEN, "else": LexType.ELSE, "fi": LexType.FI, "while": LexType.WHILE,
    "do": LexType.DO, "endwh": LexType.ENDWH, "read": LexType.READ, "write": LexType.WRITE, "return": LexType.RETURN,
    "integer": LexType.INTEGER, "char": LexType.CHAR}

# 获取当前行的下一个字符
def getNextChar(line):
    global inlinePos

    if inlinePos < len(line):
        c = line[inlinePos]
        inlinePos += 1
        return c
    else:
        raise IndexError


# 字符退回函数
def ungetNextChar():
    global inlinePos

    if inlinePos > 0:
        inlinePos -= 1
    else:
        raise IndexError


#查找保留字
def reservedLookup(word):
    if word in reservedWords:
        return reservedWords[word].name
    else:
        return LexType.ID.name


#取得单词函数
def getTokenlist(id, line):
    global tokenList, currentPos

    currentToken = Token()

    while inlinePos < len(line):
        tokenString = ""
        state = StateType.START
        has_error = False

        while state != StateType.DONE:
            save = True

            try:
                c = getNextChar(line)

                if state == StateType.START:
                    if c.isdigit():
                        state = StateType.INNUM

                    elif c.isalpha():
                        state = StateType.INID

                    elif c == ':':
                        state = StateType.INASSIGN

                    elif c == '.':
                        state = StateType.INRANGE

                    elif c == '\'':
                        save = False
                        state = StateType.INCHAR

                    elif c == ' ' or c == '\t' or c == '\n':
                        save = False

                    elif c == '{':
                        save = False
                        state = StateType.INCOMMENT

                    else:
                        state = StateType.DONE

                        if inlinePos == len(line):
                            save = False

                        elif c == '=':
                            currentToken.setLex(LexType.EQ)

                        elif c == '<':
                            currentToken.setLex(LexType.LT)

                        elif c == '+':
                            currentToken.setLex(LexType.PLUS)

                        elif c == '-':
                            currentToken.setLex(LexType.MINUS)

                        elif c == '*':
                            currentToken.setLex(LexType.TIMES)

                        elif c == '/':
                            currentToken.setLex(LexType.OVER)

                        elif c == '(':
                            currentToken.setLex(LexType.LPAREN)

                        elif c == ')':
                            currentToken.setLex(LexType.RPAREN)

                        elif c == ';':
                            currentToken.setLex(LexType.SEMI)

                        elif c == ',':
                            currentToken.setLex(LexType.COMMA)

                        elif c == '[':
                            currentToken.setLex(LexType.LMIDPAREN)

                        elif c == ']':
                            currentToken.setLex(LexType.RMIDPAREN)

                        else:
                            currentToken.setLex(LexType.ERROR)
                            has_error = True

                elif state == StateType.INCOMMENT:
                    save = False

                    if inlinePos == len(line) - 1:
                        state = StateType.DONE

                    elif c == '}':
                        state = StateType.START

                elif state == StateType.INASSIGN:

                    state = StateType.DONE

                    if c == '=':
                        currentToken.setLex(LexType.ASSIGN)
                    else:
                        ungetNextChar()
                        save = False
                        currentToken.setLex(LexType.ERROR)
                        has_error = True

                elif state == StateType.INRANGE:
                    state = StateType.DONE

                    if c == '.':
                        currentToken.setLex(LexType.UNDERANGE)
                    else:
                        ungetNextChar()
                        save = False
                        currentToken.setLex(LexType.DOT)
                elif state == StateType.INNUM:
                    if not c.isdigit():
                        ungetNextChar()
                        save = False
                        state = StateType.DONE
                        currentToken.setLex(LexType.INTC)
                elif state == StateType.INCHAR:
                    if c.isalnum():
                        c1 = getNextChar()
                        if c1 == '\'':
                            save = True
                            state = StateType.DONE
                            currentToken.setLex = LexType.CHARC
                        else:
                            ungetNextChar()
                            ungetNextChar()
                            state = StateType.DONE
                            currentToken.setLex = LexType.ERROR
                            has_error = True
                    else:
                        ungetNextChar()
                        state = StateType.DONE
                        currentToken.setLex(LexType.ERROR)
                        has_error = True
                elif state == StateType.INID:
                    if not c.isalnum():
                        ungetNextChar()
                        save = False
                        state = StateType.DONE
                        currentToken.setLex(LexType.ID)
                        #elif state == StateType.DONE :
                        #if save == True :

                else:
                    state = StateType.DONE
                    currentToken.setLex(LexType.ERROR)
                    has_error = True

                if save:
                    tokenString = tokenString + c


            except IndexError:
                break

        if has_error:
            LOG.e(TAG, "There are error in line " + str(linePos) + ". Near \"" + tokenString + "\"")

        currentToken.setLine(id)
        if currentToken.lex == LexType.ID:
            currentToken.setLex(reservedLookup(tokenString))
            if currentToken.lex == LexType.ID:
                currentToken.setSem(tokenString)
        else:
            currentToken.setSem(tokenString)

        if tokenString != '':
            tokenList.append(currentToken)
            currentToken = Token()



#look up reserve
def reservedLookup(key):
    if key in reservedWords.keys():
        return reservedWords[key]
    else:
        return LexType.ID


if __name__ == '__main__':
    global theCodeArray, inlinePos, linePos, tokenList, currentPos, prePos, TAG, lexicalCache
    #初始化
    inlinePos = 0
    linePos = 0
    currentPos = 0
    prePos = 0
    tokenList = []
    TAG = "Lexical analysis"
    lexicalCache = "lexicalCache.data"
    LOG = Log()

    #LOG.d(TAG, "start creating token.")
    if len(sys.argv) == 2:
        fileName = sys.argv[1]
        if not os.path.isfile(fileName):
            print("Please check filename")
            exit(-1)
    else:
        print("Please use as scanner filename")
        exit(-2)
    #LOG.d(TAG, "finish creating data.")
    file = open(fileName)
    theCodeArray = file.readlines()
    file.close()

    #生成Token
    for line in theCodeArray:
        inlinePos = 0
        linePos += 1

        #处理特殊情况，行内美柚\n
        if not '\n' in line:
            line += '\n'
        getTokenlist(linePos, line)

    #插入ENDFILE
    currentToken = Token(linePos + 1, LexType.ENDFILE)
    tokenList.append(currentToken)

    if not os.path.isdir("cache"):
        os.mkdir("cache")
    os.chdir("cache")

    #LOG.d(TAG, "start saving data.")
    fp = open(lexicalCache, 'wb')
    pickle.dump(tokenList, fp)
    fp.close()
    os.chdir("..")
    #LOG.d(TAG, "finish saving data.")

    Lexical.showTokenList(tokenList)
