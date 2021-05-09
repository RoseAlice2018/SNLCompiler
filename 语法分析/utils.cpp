

#include "utils.h"
#include <cstring>
extern int lineno;
std::map<NodeKind,std::string> NodeKindtostring = {
	{Prok,"Prok"},
	{PheadK,"PheadK"},
	{DecK,"DecK"},
	{TypeK,"TypeK"},
	{VarK,"VarK"},
	{ProcDecK,"ProcDecK"},
	{StmLK,"StmLK"},
	{StmtK,"StmtK"},
	{ExpK,"ExpK"},
};
std::map<LexType,std::string> lexname = { {PROGRAM, "PROGRAM"},
								  {TYPE, "TYPE"},
								  {VAR, "VAR"},
								  {PROCEDURE, "PROCEDURE"},
								  {BEGIN, "BEGIN"},
								  {END, "END"},
								  {ARRAY, "ARRAY"},
								  {OF, "OF"},
								  {RECORD, "RECORD"},
								  {IF, "IF"},
								  {THEN, "THEN"},
								  {ELSE, "ELSE"},
								  {FI, "FI"},
								  {WHILE, "WHILE"},
								  {DO, "DO"},
								  {ENDWH, "ENDWH"},
								  {READ, "READ"},
								  {WRITE, "WRITE"},
								  {RETURN, "RETURN"},
								  {INTEGER_T, "INTEGER"},
								  {CHAR_T, "CHAR"},
								  {ID, "ID"},
								  {INTC_VAL, "INTC_VAL"},
								  {CHARC_VAL, "CHAR_VAL"},
								  {ASSIGN, "ASSIGN"},
								  {EQ, "EQ"},
								  {LT, "LT"},
								  {PLUS, "PLUS"},
								  {MINUS, "MINUS"},
								  {TIMES, "TIMES"},
								  {DIVIDE, "DIVIDE"},
								  {LPAREN, "LPAREN"},
								  {RPAREN, "RPAREN"},
								  {DOT, "DOT"},
								  {COLON, "COLON"},
								  {SEMI, "SEMI"},
								  {COMMA, "COMMA"},
								  {LMIDPAREN, "LMIDPAREN"},
								  {RMIDPAREN, "RMIDPAREN"},
								  {UNDERRANGE, "UNDERRANGE"},
								  {ENDFILE, "EOF"},
								  {ERROR, "ERROR"} };
std::map<std::string,LexType> lexname_s = {{"PROGRAM",PROGRAM},
								  { "TYPE" , TYPE},
								  { "VAR" , VAR},
								  {"PROCEDURE", PROCEDURE},
								  {"BEGIN", BEGIN},
								  {"END", END},
								  {"ARRAY", ARRAY},
								  {"OF", OF},
								  {"RECORD",  RECORD},
								  {"IF",  IF },
								  {"THEN",  THEN },
								  {"ELSE",  ELSE },
								  {"FI",  FI },
								  {"WHILE",  WHILE },
								  {"DO",  DO },
								  {"ENDWH",  ENDWH },
								  {"READ",  READ },
								  {"WRITE",  WRITE },
								  {"RETURN",  RETURN },
								  {"INTEGER_T",INTEGER_T},
								  {"CHAR_T", CHAR_T},
								  {"ID",  ID },
								  {"INTC_VAL",  INTC_VAL },
								  {"CHARC_VAL", CHARC_VAL},
								  {"ASSIGN",  ASSIGN },
								  {"EQ",  EQ },
								  {"LT",  LT },
								  {"PLUS",  PLUS },
								  {"MINUS",  MINUS },
								  {"TIMES",  TIMES },
								  {"DIVIDE",  DIVIDE },
								  {"LPAREN",  LPAREN },
								  {"RPAREN",  RPAREN },
								  {"DOT",  DOT },
								  {"COLON",  COLON },
								  {"SEMI",  SEMI },
								  {"COMMA",  COMMA },
								  {"LMIDPAREN",  LMIDPAREN },
								  {"RMIDPAREN",  RMIDPAREN },
								  {"UNDERRANGE",  UNDERRANGE },
								  {"EOF",ENDFILE},
								 {"ERROR", ERROR},
								  };
TreeNode *newRootNode() {
    return newSpecNode(Prok);
}


TreeNode *newPheadNode() {
    return newSpecNode(PheadK);
}


TreeNode *newDecANode(NodeKind kind) {
    return newSpecNode(kind);
}




TreeNode *newTypeNode() {
    return newSpecNode(TypeK);
}


TreeNode *newVarNode() {
    return newSpecNode(VarK);
}


TreeNode *newDecNode() {
    return newSpecNode(DecK);
}



TreeNode *newProcNode() {
    return newSpecNode(ProcDecK);
}


TreeNode *newStmlNode() {
    return newSpecNode(StmLK);
}


TreeNode *newStmtNode(StmtKind kind) {
    TreeNode* t = newSpecNode(StmtK);

    t->kind.stmt = kind;
    return t;
}



TreeNode *newExpNode(ExpKind kind) {
    TreeNode* t = newSpecNode(ExpK);
    t->kind.exp = kind;
    return t;
}

TreeNode *newSpecNode(NodeKind kind)
{

    TreeNode* t = new TreeNode;

    int i;

    for (i = 0; i < MAXCHILDREN; i++) t->child[i] = NULL;
    t->sibling = NULL;
    t->nodekind = kind;
    t->lineno = lineno;
    t->idnum=0;
    for (i = 0; i < 10; i++) {
        strcpy(t->name[i], "\0");
        t->table[i] = NULL;
    }
    return t;
}
