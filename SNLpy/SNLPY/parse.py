#!/usr/bin/env python
'''
# 文件 parse.py
# 说明 递归向下语法分析，基于python实现
# 作者 lkk
'''
import pickle, os, sys
from globals import *
from util import Grammatical

# 定义全局变量
global lexicalCache, LOG, TAG, DEBUG, tokenList, \
    token, tokenPos, currentLine, temp_name, root

# 获取下一个token
def readNextToken():
    global tokenPos, tokenList

    if tokenPos < len(tokenList):
        t = tokenList[tokenPos]
        tokenPos += 1
    else:
        t = Token()
    return t


# 匹配函数，如果无法匹配返回错误-2
def match(expected):
    global token, currentLine

    if token.lex == expected:
        token = readNextToken()
        currentLine = token.line
    else:
        LOG.e(TAG, "not match error. Expect the" + expected.name + " in line " + str(token.line) + ".")
        token = readNextToken()
        exit(-2)


# 语法分析程序
def parse():
    global token

    t = None

    token = readNextToken()
    t = program()

    if token.lex != LexType.ENDFILE:
        LOG.e(TAG, "Code ends before file")

    return t


# 匹配program
def program():
    global token

    t = programHead()
    q = declarePart()
    s = programBody()

    root = newRootNode()
    if root != None:
        root.linePos = 0
        if t != None:
            root.child[0] = t
        else:
            LOG.e(TAG, "a program head is expected!")
        if q != None:
            root.child[1] = q
        if s != None:
            root.child[2] = s
        else:
            LOG.e(TAG, "a program body is expected!")
    match(LexType.DOT)

    return root


# 匹配程序头
def programHead():
    global token

    t = newPheadNode()
    match(LexType.PROGRAM)
    if t != None and token.lex == LexType.ID:
        t.linePos = 0
        t.name[0] = token.sem
    match(LexType.ID)

    return t


# 匹配声明部分
def declarePart():
    global token

    typeP = newDecANode(NodeKind.TypeK)
    pp = typeP

    if typeP != None:
        typeP.linePos = 0
        tp1 = typeDec()

        if tp1 != None:
            typeP.child[0] = tp1
        else:
            typeP = None

    varP = newDecANode(NodeKind.VarK)

    if varP != None:
        varP.linePos = 0
        tp2 = varDec()
        if tp2 != None:
            varP.child[0] = tp2
        else:
            varP = None

    s = procDec()

    if varP == None:
        varP = s
    if typeP == None:
        pp = typeP = varP
    if typeP != varP:
        typeP.brother = varP
        typeP = varP
    if varP != s:
        varP.brother = s
        varP = s

    return pp


def typeDec():
    global token

    t = None

    if token.lex == LexType.TYPE:
        t = typeDeclaration()
    elif token.lex == LexType.VAR or token.lex == LexType.PROCEDURE or \
                    token.lex == LexType.BEGIN:
        pass
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is here!")

    return t


def typeDeclaration():
    global token

    match(LexType.TYPE)
    t = typeDecList()
    if t == None:
        LOG.e(TAG, "a type declaration is expected!")
    return t


def typeDecList():
    global token

    t = newDecNode()
    if t != None:
        t.linePos = currentLine
        typeId(t)
        match(LexType.EQ)
        typeName(t)
        match(LexType.SEMI)
        p = typeDecMore()
        if p != None:
            t.brother = p

    return t


def typeDecMore():
    global token

    t = None

    if token.lex == LexType.VAR or token.lex == LexType.PROCEDURE or \
                    token.lex == LexType.BEGIN:
        pass
    elif token.lex == LexType.ID:
        t = typeDecList()
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is in typeDecMore()!")
    return t


def typeId(t):
    global token

    tnum = t.idnum
    if token.lex == LexType.ID and t != None:
        t.name[tnum] = token.sem
        tnum += 1

    t.idnum = tnum
    match(LexType.ID)


def typeName(t):
    global token

    if t != None:
        if token.lex == LexType.INTEGER or token.lex == LexType.CHAR:
            baseType(t)
        elif token.lex == LexType.ARRAY or token.lex == LexType.RECORD:
            structureType(t)
        elif token.lex == LexType.ID:
            t.kind["dec"] = DecKind.IdK
            t.attr["type_name"] = token.sem
            match(LexType.ID)
        else:
            token = readNextToken()
            LOG.e(TAG, "unexpected token is in typeName()!")


def baseType(t):
    global token

    if token.lex == LexType.INTEGER:
        match(LexType.INTEGER)
        t.kind["dec"] = DecKind.IntegerK
    elif token.lex == LexType.CHAR:
        match(LexType.CHAR)
        t.kind["dec"] = DecKind.CharK
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is in baseType()!")


def structureType(t):
    global token

    if token.lex == LexType.ARRAY:
        arrayType(t)
    elif token.lex == LexType.RECORD:
        t.kind["dec"] = DecKind.RecordK
        recType(t)
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is in structureType()!")


def arrayType(t):
    global token

    match(LexType.ARRAY)
    match(LexType.LMIDPAREN)
    if token.lex == LexType.INTC:
        t.attr["ArrayAttr"]["low"] = int(token.sem)
    match(LexType.INTC)
    match(LexType.UNDERANGE)
    if token.lex == LexType.INTC:
        t.attr["ArrayAttr"]["up"] = int(token.sem)
    match(LexType.INTC)
    match(LexType.RMIDPAREN)
    match(LexType.OF)
    baseType(t)
    t.attr["ArrayAttr"]["childtype"] = t.kind["dec"]
    t.kind["dec"] = DecKind.ArrayK


def recType(t):
    p = None
    match(LexType.RECORD)
    p = fieldDecList()
    if p != None:
        t.child[0] = p
    else:
        LOG.e(TAG, "a record body is requested!")
    match(LexType.END)


def fieldDecList():
    global token

    t = newDecNode()
    p = None

    if t != None:
        t.linePos = currentLine

        if token.lex == LexType.INTEGER or token.lex == LexType.CHAR:
            baseType(t)
            idList(t)
            match(LexType.SEMI)
            p = fieldDecMore()
        elif token.lex == LexType.ARRAY:
            arrayType(t)
            idList(t)
            match(LexType.SEMI)
            p = fieldDecMore()
        else:
            token = readNextToken()
            LOG.e(TAG, "unexpected token is in fieldDecList()!")

        t.brother = p

    return t


def fieldDecMore():
    global token

    t = None
    if token.lex == LexType.END:
        pass
    elif token.lex == LexType.INTEGER or token.lex == LexType.CHAR or \
                    token.lex == LexType.ARRAY:
        t = fieldDecList()
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is in fieldDecMore()!")
    return t


def idList(t):
    global token

    if token.lex == LexType.ID:
        t.name[t.idnum] = token.sem
        match(LexType.ID)
        t.idnum += 1

    idMore(t)


def idMore(t):
    global token

    if token.lex == LexType.SEMI:
        pass
    elif token.lex == LexType.COMMA:
        match(LexType.COMMA)
        idList(t)
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is in idMore()!")


def varDec():
    global token

    t = None
    if token.lex == LexType.PROCEDURE or token.lex == LexType.BEGIN:
        pass
    elif token.lex == LexType.VAR:
        t = varDeclaration()
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is in varDec()!")

    return t


def varDeclaration():
    match(LexType.VAR)
    t = varDecList()
    if t == None:
        LOG.e(TAG, "a var declaration is expected!")
    return t


def varDecList():
    global token

    t = newDecNode()
    p = None

    if t != None:
        t.linePos = currentLine
        typeName(t)
        varIdList(t)
        match(LexType.SEMI)
        p = varDecMore()
        t.brother = p

    return t


def varDecMore():
    global token

    t = None

    if token.lex == LexType.PROCEDURE or token.lex == LexType.BEGIN:
        pass
    elif token.lex == LexType.INTEGER or token.lex == LexType.CHAR or \
                    token.lex == LexType.ARRAY or token.lex == LexType.RECORD or \
                    token.lex == LexType.ID:
        t = varDecList()
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is in varDexMore()!")

    return t


def varIdList(t):
    global token

    if token.lex == LexType.ID:
        t.name[t.idnum] = token.sem
        match(LexType.ID)
        t.idnum += 1
    else:
        LOG.e(TAG, "a varid is expected here!")
        token = readNextToken()
    varIdMore(t)


def varIdMore(t):
    global token

    if token.lex == LexType.SEMI:
        pass
    elif token.lex == LexType.COMMA:
        match(LexType.COMMA)
        varIdList(t)
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is in varIdMore()!")


def procDec():
    global token

    t = None

    if token.lex == LexType.BEGIN:
        pass
    elif token.lex == LexType.PROCEDURE:
        t = procDeclaration()
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is in procDec()!")

    return t


def procDeclaration():
    global token

    t = newProcNode()
    match(LexType.PROCEDURE)
    if t != None:
        t.linePos = currentLine
        if token.lex == LexType.ID:
            t.name[0] = token.sem
            t.idnum += 1
            match(LexType.ID)
        match(LexType.LPAREN)
        paramList(t)
        match(LexType.RPAREN)
        match(LexType.SEMI)
        t.child[1] = procDecPart()
        t.child[2] = procBody()
        t.brother = procDec()

    return t


def paramList(t):
    global token

    if token.lex == LexType.RPAREN:
        pass
    elif token.lex == LexType.INTEGER or token.lex == LexType.CHAR or \
                    token.lex == LexType.ARRAY or token.lex == LexType.RECORD or \
                    token.lex == LexType.ID or token.lex == LexType.VAR:
        p = paramDecList()
        t.child[0] = p
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is in paramList()!")


def paramDecList():
    t = param()
    p = paramMore()
    if p != None:
        t.brother = p
    return t


def paramMore():
    global token

    t = None

    if token.lex == LexType.RPAREN:
        pass
    elif token.lex == LexType.SEMI:
        match(LexType.SEMI)
        t = paramDecList()
        if t == None:
            LOG.e(TAG, "a param declaration is request!")
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is in paramMore()!")

    return t


def param():
    global token

    t = newDecNode()
    if t != None:
        t.linePos = currentLine
        if token.lex == LexType.INTEGER or token.lex == LexType.CHAR or \
                        token.lex == LexType.ARRAY or token.lex == LexType.RECORD or \
                        token.lex == LexType.ID:
            t.attr["ProcAttr"]["paramt"] = ParamType.valparamType
            typeName(t)
            formList(t)
        elif token.lex == LexType.VAR:
            match(LexType.VAR)
            t.attr["ProcAttr"]["paramt"] = ParamType.varparamType
            typeName(t)
            formList(t)
        else:
            token = readNextToken()
            LOG.e(TAG, "unexpected token is in param()!")

    return t


def formList(t):
    global token

    if token.lex == LexType.ID:
        t.name[t.idnum] = token.sem
        t.idnum = t.idnum + 1
        match(LexType.ID)

    fidMore(t)


def fidMore(t):
    global token

    if token.lex == LexType.SEMI or token.lex == LexType.RPAREN:
        pass
    elif token.lex == LexType.COMMA:
        match(LexType.COMMA)
        formList(t)
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is in fidMore()!")


def procDecPart():
    return declarePart()


def procBody():
    t = programBody()

    if t == None:
        LOG.e(TAG, "a program body is requested!")

    return t


def programBody():
    global token

    t = newStmlNode()
    match(LexType.BEGIN)

    if t != None:
        t.linePos = 0
        t.child[0] = stmList()

    match(LexType.END)
    return t


def stmList():
    t = stm()
    p = stmMore()

    if t != None:
        if p != None:
            t.brother = p

    return t


def stmMore():
    global token

    t = None

    if token.lex == LexType.ELSE or token.lex == LexType.FI or \
                    token.lex == LexType.END or token.lex == LexType.ENDWH:
        pass
    elif token.lex == LexType.SEMI:
        match(LexType.SEMI)
        t = stmList()
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is in stmMore()!")

    return t


def stm():
    global token, temp_name

    t = None
    if token.lex == LexType.IF:
        t = conditionalStm()
    elif token.lex == LexType.WHILE:
        t = loopStm()
    elif token.lex == LexType.READ:
        t = inputStm()
    elif token.lex == LexType.WRITE:
        t = outputStm()
    elif token.lex == LexType.RETURN:
        t = returnStm()
    elif token.lex == LexType.ID:
        temp_name = token.sem
        match(LexType.ID)
        t = assCall()
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is here!")

    return t


def assCall():
    global token

    t = None

    if token.lex == LexType.ASSIGN or token.lex == LexType.LMIDPAREN or \
                    token.lex == LexType.DOT:
        t = assignmentRest()
    elif token.lex == LexType.LPAREN:
        t = callStmRest()
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is here!")

    return t


def assignmentRest():
    global token, temp_name

    t = newStmtNode(StmtKind.AssignK)

    if t != None:
        t.linePos = currentLine

        child1 = newExpNode(ExpKind.VariK)
        if child1 != None:
            child1.linePos = currentLine
            child1.name[0] = temp_name
            child1.idnum += 1
            variMore(child1)
            t.child[0] = child1

        match(LexType.ASSIGN)

        t.child[1] = exp()

    return t


def conditionalStm():
    global token

    t = newStmtNode(StmtKind.IfK)
    match(LexType.IF)
    if t != None:
        t.linePos = currentLine
        t.child[0] = exp()

    match(LexType.THEN)
    if t != None:
        t.child[1] = stmList()
    if token.lex == LexType.ELSE:
        match(LexType.ELSE)
        if t != None:
            t.child[2] = stmList()

    match(LexType.FI)
    return t


def loopStm():
    global token

    t = newStmtNode(StmtKind.WhileK)
    match(LexType.WHILE)
    if t != None:
        t.linePos = currentLine
        t.child[0] = exp()
        match(LexType.DO)
        t.child[1] = stmList()
        match(LexType.ENDWH)

    return t


def inputStm():
    global token

    t = newStmtNode(StmtKind.ReadK)
    match(LexType.READ)
    match(LexType.LPAREN)
    if t != None and token.lex == LexType.ID:
        t.linePos = currentLine
        t.name[0] = token.sem
        t.idnum += 1

    match(LexType.ID)
    match(LexType.RPAREN)
    return t


def outputStm():
    global token

    t = newStmtNode(StmtKind.WriteK)
    match(LexType.WRITE)
    match(LexType.LPAREN)
    if t != None:
        t.linePos = currentLine
        t.child[0] = exp()

    match(LexType.RPAREN)

    return t


def returnStm():
    global token

    t = newStmtNode(StmtKind.ReturnK)
    match(LexType.RETURN)
    if t != None:
        t.linePos = currentLine
    return t


def callStmRest():
    global token

    t = newStmtNode(StmtKind.CallK)
    match(LexType.LPAREN)

    if t != None:
        t.linePos = currentLine

        child0 = newExpNode(ExpKind.VariK)
        if child0 != None:
            child0.linePos = currentLine
            child0.name[0] = temp_name
            child0.idnum += 1
            t.child[0] = child0

        t.child[1] = actParamList()

    match(LexType.RPAREN)
    return t


def actParamList():
    global token

    t = None

    if token.lex == LexType.RPAREN:
        pass
    elif token.lex == LexType.ID or token.lex == LexType.INTC:
        t = exp()
        if t != None:
            t.brother = actParamMore()
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is here!")

    return t


def actParamMore():
    global token

    t = None

    if token.lex == LexType.RPAREN:
        pass
    elif token.lex == LexType.COMMA:
        match(LexType.COMMA)
        t = actParamList()
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is here!")

    return t


def exp():
    global token

    t = simple_exp()

    if token.lex == LexType.LT or token.lex == LexType.EQ:
        p = newExpNode(ExpKind.OpK)

        if p != None:
            p.linePos = currentLine
            p.child[0] = t
            p.attr["ExpAttr"]["op"] = token.lex

            t = p

        match(token.lex)

        if t != None:
            t.child[1] = simple_exp()

    return t


def simple_exp():
    global token

    t = term()

    while token.lex == LexType.PLUS or token.lex == LexType.MINUS:
        p = newExpNode(ExpKind.OpK)

        if p != None:
            p.linePos = currentLine
            p.child[0] = t
            p.attr["ExpAttr"]["op"] = token.lex

            t = p

            match(token.lex)

            t.child[1] = term()

    return t


def term():
    global token

    t = factor()

    while token.lex == LexType.TIMES or token.lex == LexType.OVER:
        p = newExpNode(ExpKind.OpK)

        if p != None:
            p.linePos = currentLine
            p.child[0] = t
            p.attr["ExpAttr"]["op"] = token.lex
            t = p

        match(token.lex)

        p.child[1] = factor()

    return t


def factor():
    global token

    t = None

    if token.lex == LexType.INTC:
        t = newExpNode(ExpKind.ConstK)

        if t != None and token.lex == LexType.INTC:
            t.linePos = currentLine
            t.attr["ExpAttr"]["val"] = int(token.sem)

        match(LexType.INTC)

    elif token.lex == LexType.ID:
        t = variable()

    elif token.lex == LexType.LPAREN:

        match(LexType.LPAREN)
        t = exp()
        match(LexType.RPAREN)
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is in factor()!")

    return t


def variable():
    global token

    t = newExpNode(ExpKind.VariK)

    if t != None and token.lex == LexType.ID:
        t.linePos = currentLine
        t.name[0] = token.sem
        t.idnum += 1

    match(LexType.ID)
    variMore(t)

    return t


def variMore(t):
    global token

    if token.lex == LexType.ASSIGN or token.lex == LexType.TIMES or \
                    token.lex == LexType.EQ or token.lex == LexType.LT or \
                    token.lex == LexType.PLUS or token.lex == LexType.MINUS or \
                    token.lex == LexType.OVER or token.lex == LexType.RPAREN or \
                    token.lex == LexType.RMIDPAREN or token.lex == LexType.SEMI or \
                    token.lex == LexType.COMMA or token.lex == LexType.THEN or \
                    token.lex == LexType.ELSE or token.lex == LexType.FI or \
                    token.lex == LexType.DO or token.lex == LexType.ENDWH or \
                    token.lex == LexType.END:
        pass
    elif token.lex == LexType.LMIDPAREN:
        match(LexType.LMIDPAREN)

        t.child[0] = exp()
        t.attr["ExpAttr"]["varkind"] = VarKind.ArrayMembV
        t.child[0].attr["ExpAttr"]["varkind"] = VarKind.IdV
        match(LexType.RMIDPAREN)
    elif token.lex == LexType.DOT:
        match(LexType.DOT)
        t.child[0] = fieldvar()
        t.attr["ExpAttr"]["varkind"] = VarKind.FieldMembV
        t.child[0].attr["ExpAttr"]["varkind"] = VarKind.IdV
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is in variMore()!")


def fieldvar():
    global token

    t = newExpNode(ExpKind.VariK)

    if t != None and token.lex == LexType.ID:
        t.linePos = currentLine
        t.name[0] = token.sem
        t.idnum += 1

    match(LexType.ID)

    fieldvarMore(t)

    return t


def fieldvarMore(t):
    global token

    if token.lex == LexType.ASSIGN or token.lex == LexType.TIMES or \
                    token.lex == LexType.EQ or token.lex == LexType.LT or \
                    token.lex == LexType.PLUS or token.lex == LexType.MINUS or \
                    token.lex == LexType.OVER or token.lex == LexType.RPAREN or \
                    token.lex == LexType.END or token.lex == LexType.SEMI or \
                    token.lex == LexType.COMMA or token.lex == LexType.THEN or \
                    token.lex == LexType.ELSE or token.lex == LexType.FI or \
                    token.lex == LexType.DO or token.lex == LexType.ENDWH:
        pass
    elif token.lex == LexType.LMIDPAREN:
        match(LexType.LMIDPAREN)

        t.child[0] = exp()
        t.child[0].attr["ExpAttr"]["varkind"] = VarKind.ArrayMenbV
        match(LexType.RMIDPAREN)
    else:
        token = readNextToken()
        LOG.e(TAG, "unexpected token is here!")


def getTreeRoot():
    global lexicalCache,LOG,tokenList,currentLine,root,DEBUG,tokenPos

    lexicalCache = "lexicalCache.data"
    LOG = Log()
    tokenList = []
    tokenPos = 0
    currentLine = 0
    TAG = "parse.py"
    DEBUG = "debug"

    if not os.path.isdir("cache") :
        os.mkdir("cache")
    os.chdir("cache")

    if not os.path.isfile(lexicalCache) :
        LOG.e(TAG,lexicalCache + " doesn't exist.")
        exit(-1)

    #LOG.d(TAG,"start reading data.")
    fp = open(lexicalCache,'rb')
    tokenList = pickle.load(fp)
    fp.close()
    os.chdir("..")
    #LOG.d(TAG,"finish reading data.")

    root = parse()
    return root

if __name__ == '__main__':
    global lexicalCache, LOG, tokenList, currentLine, root

    lexicalCache = "lexicalCache.data"
    LOG = Log()
    tokenList = []
    tokenPos = 0
    currentLine = 0
    TAG = "parse.py"
    DEBUG = "debug"

    gramma = Grammatical()

    if not os.path.isdir("cache"):
        os.mkdir("cache")
    os.chdir("cache")

    if not os.path.isfile(lexicalCache):
        LOG.e(TAG, lexicalCache + " doesn't exist.")
        exit(-1)

    #LOG.d(TAG, "start reading data.")
    fp = open(lexicalCache, 'rb')
    tokenList = pickle.load(fp)
    fp.close()
    os.chdir("..")
    #LOG.d(TAG, "finish reading data.")

    root = parse()
    gramma.printTree(root)
