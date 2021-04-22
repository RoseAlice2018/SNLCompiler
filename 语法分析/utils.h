#ifndef UTILS_H
#define UTILS_H


#include  "globals.h"
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
								  //{"INTEGER_T",INTEGER},
								  //{"CHAR_T", CHAR},
								  {"ID",  ID },
								  {"INTC_VAL",  INTC_VAL },
								  //{"CHARC_VAL", CHAR_VAL},
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

class utils {

};
TreeNode *newSpecNode(NodeKind kind);

TreeNode *newTypeNode();

TreeNode *newVarNode();


TreeNode *newRootNode();

TreeNode *newPheadNode();

TreeNode *newDecANode(NodeKind kind);

TreeNode *newDecNode();

TreeNode *newProcNode();

TreeNode *newStmlNode();

TreeNode *newStmtNode(StmtKind kind);


TreeNode *newExpNode(ExpKind kind);

#endif 
