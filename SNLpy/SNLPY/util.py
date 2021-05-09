'''
# 文件 util.py
# 说明 辅助类，基于python实现
# 作者 lkk
'''
from globals import *


def printInLine(word):
    print(word, end="")


def printTab(num):
    i = 0
    while i < num:
        printInLine(" ")
        i += 1


class Lexical():
    def __init__(self):
        self.name = "Lexical"

    def showTokenList(tokenList):
        for token in tokenList:
            print(token.toString())


# Add gra
class Grammatical():
    def __init__(self):
        self.name = "Grammatical"
        self.indentno = 0

    def INDENT(self):
        self.indentno += 4

    def UNINDENT(self):
        self.indentno -= 4

    def printSpaces(self):
        i = 0
        while i < self.indentno:
            printInLine(" ")
            i += 1

    def printTree(self, tree):
        # i = 0
        self.INDENT()

        while tree != None:
            if tree.linePos == 0:
                printTab(9)
            else:
                t = tree.linePos / 10
                printInLine("line:" + str(tree.linePos))
                if t == 0:
                    printTab()
                elif t <= 9 and t >= 1:
                    printTab(2)
                else:
                    printTab(1)
            self.printSpaces()

            if tree.nodeKind == NodeKind.ProK:
                printInLine("Prok  ")
            elif tree.nodeKind == NodeKind.PheadK:
                printInLine("PheadK  ")
                printInLine(tree.name[0] + "  ")
            elif tree.nodeKind == NodeKind.DecK:
                printInLine("Deck  ")
                if tree.attr["ProcAttr"]["paramt"] == ParamType.varparamType:
                    printInLine("var param:  ")
                if tree.attr["ProcAttr"]["paramt"] == ParamType.valparamType:
                    printInLine("value param:  ")

                if tree.kind["dec"] == DecKind.ArrayK:
                    printInLine("ArrayK  ")
                    printInLine(str(tree.attr["ArrayAttr"]["up"]) + "  ")
                    printInLine(str(tree.attr["ArrayAttr"]["low"]) + " ")
                    if tree.attr["ArrayAttr"]["childtype"] == DecKind.CharK:
                        printInLine("Chark  ")
                    elif tree.attr["ArrayAttr"]["childtype"] == DecKind.IntegerK:
                        printInLine("IntegerK  ")
                elif tree.kind["dec"] == DecKind.CharK:
                    printInLine("Chark  ")
                elif tree.kind["dec"] == DecKind.IntegerK:
                    printInLine("IntegerK  ")
                elif tree.kind["dec"] == DecKind.RecordK:
                    printInLine("RecordK  ")
                elif tree.kind["dec"] == DecKind.IdK:
                    printInLine("IdK  ")
                    printInLine(tree.attr["type_name"] + "  ")
                else:
                    printInLine("error1!")

                if tree.idnum != 0:
                    i = 0
                    while i < tree.idnum:
                        printInLine(tree.name[i] + "  ")
                        i += 1
                else:
                    printInLine("wrong!no var!\n")

            elif tree.nodeKind == NodeKind.TypeK:
                printInLine("TypeK  ")

            elif tree.nodeKind == NodeKind.VarK:
                printInLine("VarK  ")
                if tree.table[0] != None:
                    printInLine(str(tree.table[0].attrIR["More"]["VarAttr"]["off"]) + "  " + \
                                str(tree.table[0].attrIR["More"]["VarAttr"]["level"]) + "  ")

            elif tree.nodeKind == NodeKind.ProcDecK:
                printInLine("ProcDeck  ")
                printInLine(tree.name[0] + "  ")
                if tree.table[0] != None:
                    printInLine(str(tree.table[0].attrIR["More"]["ProcAttr"]["mOff"]) + "  " + \
                                str(tree.table[0].attrIR["More"]["ProcAttr"]["nOff"]) + "  " + \
                                str(tree.table[0].attrIR["More"]["ProcAttr"]["nOff"]) + "  ")

            elif tree.nodeKind == NodeKind.StmLK:
                printInLine("StmLK  ")

            elif tree.nodeKind == NodeKind.StmtK:
                printInLine("StmtK  ")

                if tree.kind["stmt"] == StmtKind.IfK:
                    printInLine("If  ")
                elif tree.kind["stmt"] == StmtKind.WhileK:
                    printInLine("While  ")
                elif tree.kind["stmt"] == StmtKind.AssignK:
                    printInLine("Assign  ")
                elif tree.kind["stmt"] == StmtKind.ReadK:
                    printInLine("Read  ")
                    printInLine(tree.name[0] + "  ")
                    if tree.table[0] != None:
                        printInLine(str(tree.table[0].attrIR["More"]["VarAttr"]["off"]) + "  " + \
                                    str(tree.table[0].attrIR["More"]["VarAttr"]["level"]) + "  ")
                elif tree.kind["stmt"] == StmtKind.WriteK:
                    printInLine("Write  ")
                elif tree.kind["stmt"] == StmtKind.CallK:
                    printInLine("Call  ")
                    printInLine(tree.name[0] + "  ")
                elif tree.kind["stmt"] == StmtKind.ReturnK:
                    printInLine("Return  ")
                else:
                    printInLine("error2!")
            elif tree.nodeKind == NodeKind.ExpK:
                printInLine("ExpK  ")
                if tree.kind["exp"] == ExpKind.OpK:
                    printInLine("Op  ")
                    if tree.attr["ExpAttr"]["op"] == LexType.EQ:
                        printInLine("=  ")
                    elif tree.attr["ExpAttr"]["op"] == LexType.LT:
                        printInLine("<  ")
                    elif tree.attr["ExpAttr"]["op"] == LexType.PLUS:
                        printInLine("+  ")
                    elif tree.attr["ExpAttr"]["op"] == LexType.TIMES:
                        printInLine("*  ")
                    elif tree.attr["ExpAttr"]["op"] == LexType.MINUS:
                        printInLine("-  ")
                    elif tree.attr["ExpAttr"]["op"] == LexType.OVER:
                        printInLine("/  ")
                    else:
                        printInLine("error3!")

                    if tree.attr["ExpAttr"]["varkind"] == VarKind.ArrayMembV:
                        printInLine("ArrayMember  ")
                        printInLine(tree.name[0] + "  ")

                elif tree.kind["exp"] == ExpKind.ConstK:
                    printInLine("Const  ")
                    if tree.attr["ExpAttr"]["varkind"] == VarKind.IdV:
                        printInLine("Id  ")
                        printInLine(tree.name[0])
                    elif tree.attr["ExpAttr"]["varkind"] == VarKind.FieldMembV:
                        printInLine("FieldMember  ")
                        printInLine(tree.name[0])
                    elif tree.attr["ExpAttr"]["varkind"] == VarKind.ArrayMembV:
                        printInLine("ArrayMember  ")
                        printInLine(tree.name[0])
                    else:
                        printInLine("var type error!")

                    printInLine(str(tree.attr["ExpAttr"]["val"]) + "  ")

                elif tree.kind["exp"] == ExpKind.VariK:
                    printInLine("Vari  ")
                    if tree.attr["ExpAttr"]["varkind"] == VarKind.IdV:
                        printInLine("Id  ")
                        printInLine(tree.name[0] + "  ")
                    elif tree.attr["ExpAttr"]["varkind"] == VarKind.FieldMembV:
                        printInLine("FieldMember  ")
                        printInLine(tree.name[0])
                    elif tree.attr["ExpAttr"]["varkind"] == VarKind.ArrayMembV:
                        printInLine("ArrayMember  ")
                        printInLine(tree.name[0])
                    else:
                        printInLine("var type error!")

                    if tree.table[0] != None:
                        printInLine(tree.table[0].attrIR["More"]["VarAttr"]["off"] + "  " + \
                                    tree.table[0].attrIR["More"]["VarAttr"]["level"] + "  ")

                else:
                    printInLine("error4!")

            else:
                printInLine("error5!")

            printInLine("\n")

            i = 0
            while i < 3:
                self.printTree(tree.child[i])
                i += 1

            tree = tree.brother

        self.UNINDENT()


