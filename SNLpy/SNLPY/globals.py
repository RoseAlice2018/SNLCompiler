'''
# 全局变量
'''
import sys
from enum import Enum


class LexType(Enum):
    ENDFILE = 1
    ERROR = 2
    PROGRAM = 3
    PROCEDURE = 4
    TYPE = 5
    VAR = 6
    IF = 7
    THEN = 8
    ELSE = 9
    FI = 10
    WHILE = 11
    DO = 12
    ENDWH = 13
    BEGIN = 14
    END = 15
    READ = 16
    WRITE = 17
    ARRAY = 18
    OF = 19
    RECORD = 20
    RETURN = 21
    INTEGER = 22
    CHAR = 23
    ID = 24
    INTC = 25
    ASSIGN = 26
    CHARC = 27
    LT = 28
    EQ = 29
    PLUS = 30
    MINUS = 31
    TIMES = 32
    OVER = 33
    LPAREN = 34
    RPAREN = 35
    DOT = 36
    COLON = 37
    SEMI = 38
    COMMA = 39
    LMIDPAREN = 40
    RMIDPAREN = 41
    UNDERANGE = 42
    DEFAULT = 43


class ParamType(Enum):
    valparamType = 1
    varparamType = 2


class NodeKind(Enum):
    ProK = 1
    PheadK = 2
    DecK = 3
    TypeK = 4
    VarK = 5
    ProcDecK = 6
    StmLK = 7
    StmtK = 8
    ExpK = 9


class DecKind(Enum):
    ArrayK = 1
    CharK = 2
    IntegerK = 3
    RecordK = 4
    IdK = 5


class StmtKind(Enum):
    IfK = 1
    WhileK = 2
    AssignK = 3
    ReadK = 4
    WriteK = 5
    CallK = 6
    ReturnK = 7


class ExpKind(Enum):
    OpK = 1
    ConstK = 2
    VariK = 3


class VarKind(Enum):
    IdV = 1
    ArrayMembV = 2
    FieldMembV = 3


class ExpType(Enum):
    Void = 1
    Integer = 2
    Boolean = 3


class ParamType(Enum):
    valparamType = 1
    varparamType = 2


class AccessKind(Enum):
    dir = 1
    indir = 2


class IdKind(Enum):
    typeKind = 1
    varKind = 2
    procKind = 3


class ParamTable():
    def __init__(self):
        entry = Symbtable()
        next = ParamTable()


class AttributeIR():
    def __init__(self):
        self.idtype = None
        self.kind = None
        self.More = {
            "VarAttr": {
                "access": None,
                "level": 0,
                "off": 0,
                "isParam": False
            },
            "ProcAttr": {
                "level": 0,
                "param": None,
                "mOff": 0,
                "nOff": 0,
                "procEntry": 0,
                "codeEntry": 0
            }
        }


class Symbtable():
    def __init__(self):
        self.idName = ""
        self.attrIR = AttributeIR()
        self.next = None


class Token():
    def __init__(self, line=0, lex=LexType.DEFAULT, sem=None):
        self.line = line
        self.lex = lex
        self.sem = sem

    def setLine(self, line):
        self.line = line

    def setLex(self, lex):
        self.lex = lex

    def setSem(self, sem):
        self.sem = sem

    def toString(self):
        if self.sem != None:
            return "<" + str(self.line) + "," + self.lex.name + "," + str(self.sem) + ">"
        else:
            return "<" + str(self.line) + "," + self.lex.name + ">"


class Log():
    def e(self, tag, word):
        sys.stderr.write("[error] from " + tag + " " + word + "\n")


    def d(self, tag, word):
        sys.stdout.write("[log] from " + tag + " " + word + "\n")


class TreeNode:
    def __init__(self, nodeKind=None):
        self.brother = None
        self.child = [None, None, None]
        self.linePos = 0
        self.kind = {"dec": None, "stmt": None, "exp": None}
        self.nodeKind = nodeKind
        self.idnum = 0
        self.name = [""] * 10
        self.table = [None] * 10
        self.attr = \
            {
                "ArrayAttr": {"low": 0, "up": 0, "childtype": None},
                "ProcAttr": {"paramt": None},
                "ExpAttr": {"op": None, "val": 0, "varkind": None, "type": None},
                "type_name": ""
            }

    def add(self, TreeNode):
        self.children.append(TreeNode)

    def get(self, id):
        return self.children[id]


class TypeKind(Enum):
    intTy = 1
    charTy = 2
    arrayTy = 3
    recordTy = 4
    boolTy = 5


class fieldchain():
    def __init__(self):
        self.id = [] * 10
        self.off = None
        self.UnitType = None
        self.Next = None


def newRootNode():
    return TreeNode(NodeKind.ProK)


def newPheadNode():
    return TreeNode(NodeKind.PheadK)


def newDecANode(kind):
    return TreeNode(kind)


def newDecNode():
    return TreeNode(NodeKind.DecK)


def newProcNode():
    return TreeNode(NodeKind.ProcDecK)


def newStmtNode(kind=None):
    t = TreeNode(NodeKind.StmtK)
    t.kind["stmt"] = kind
    return t


def newStmlNode():
    t = TreeNode(NodeKind.StmLK)
    return t

def newExpNode(kind):
    t = TreeNode(NodeKind.ExpK)
    t.kind["exp"] = kind
    t.attr["ExpAttr"]["varkind"] = VarKind.IdV
    t.attr["ExpAttr"]["type"] = ExpType.Void
    return t


class TypeIR():
    def __init__(self):
        self.size = 0
        self.kind = None
        self.More = \
            {
                "ArrayAttr":{"indexTy":None,"elemTy":None,"low":0,"up":0},
                "body":None
            }

#scope = [0] *1000
#Level = None
#Off = None
INITOFF = 7
SCOPESIZE = 1000
savedOff = None
Error = None