#ifndef _GLOBALS_H_
#define _GLOBALS_H_

#include <stdio.h>
#include <stdlib.h>
#include <map>
#include <set>
#include <string>


enum LexType 
{

    ENDFILE,	ERROR,
    PROGRAM,	PROCEDURE,	TYPE,	VAR,		IF,
	THEN,		ELSE,		FI,		WHILE,		DO,
	ENDWH,		BEGIN,		END,	READ,		WRITE,
	ARRAY,		OF,			RECORD,	RETURN, 
    INTEGER_T,	CHAR_T,
    ID,			INTC_VAL,		CHARC_VAL,
	ASSIGN,		EQ,			LT,		PLUS,		MINUS,
    TIMES,DIVIDE,		LPAREN,	RPAREN,		DOT,
    COLON,		SEMI,		COMMA,	LMIDPAREN,	RMIDPAREN,
    UNDERRANGE,
    Program,	      ProgramHead,	    ProgramName,	DeclarePart,
    TypeDec,        TypeDeclaration,	TypeDecList,	TypeDecMore,
    TypeId,	      TypeName,			BaseType,	    StructureType,
    ArrayType,      Low,	            Top,            RecType,
    FieldDecList,   FieldDecMore,	    IdList,	        IdMore,
    VarDec,	      VarDeclaration,	VarDecList,		VarDecMore,
    VarIdList,	  VarIdMore,		ProcDec,		ProcDeclaration,
    ProcDecMore,    ProcName,		    ParamList,		ParamDecList,
    ParamMore,      Param,		    FormList,		FidMore,
    ProcDecPart,    ProcBody,	    	ProgramBody,	StmList,
    StmMore,        Stm,				AssCall,		AssignmentRest,
    ConditionalStm, StmL,			    LoopStm,		InputStm,
    InVar,          OutputStm,		ReturnStm,		CallStmRest,
    ActParamList,   ActParamMore,		RelExp,			OtherRelE,
    Exp,			  OtherTerm,		Term,           OtherFactor,
    Factor,         Variable,			VariMore,		FieldVar,
    FieldVarMore,   CmpOp,			AddOp,          MultOp
} ;

extern std::map<LexType,std::string> lexname;

class Token{
    public:
        Token(int line,LexType lex,std::string sem){
            this->line = line;
            this->lex = lex;
            this->sem = sem;
        }
        Token(){
            
        }
        int getLine() const{return line;}
        std::string getLexName() const{return lexname[lex];}
        LexType getLex() const {return lex;}
        std::string getSem()const {return sem;}

        Token *next;
    private:
        int line;
        LexType lex;
        std::string sem;
};


//记录语法树节点类型
typedef enum{Prok,PheadK,DecK,TypeK,VarK,ProcDecK,StmLK,StmtK,ExpK}NodeKind;
extern std::map<NodeKind,std::string> nodeKindMap;

//DecKind 成员
typedef enum{ArrayK,CharK,IntegerK,RecordK,IdK} DecKind;
extern std::map<DecKind,std::string> decKindMap;

//StmtKind 成员
typedef enum{IfK,WhileK,AssignK,ReadK,WriteK,CallK,ReturnK}StmtKind;
extern std::map<StmtKind,std::string> stmtKindMap;


//ExpKind 成员
typedef enum{OpK,ConstK,VariK} ExpKind;
extern std::map<ExpKind,std::string> expKindMap;



//VarKind 成员
typedef enum{IdV,ArrayMembV,FieldMembV}VarKind;
extern std::map<VarKind,std::string> varKindMap;

//ExpType 成员
typedef enum{Void,Integer,Boolean}ExpType;
extern std::map<ExpType,std::string> expTypeMap;

//ParamType 成员
typedef enum{valparamType,varparamType}ParamType;
extern std::map<ParamType,std::string> paramTypeMap;


#define MAXCHILDREN 3

struct symbtable;

typedef struct treeNode{
    //指向子语法树节点指针
    struct treeNode* child[MAXCHILDREN];
    //指向兄弟语法树节点指针
    struct treeNode* sibling;
    //记录源程序
    int lineno;
    NodeKind nodekind;
    //成员Kind 记录语法树节点的具体内容，为共用体结构
    union
    {
        DecKind dec;
        StmtKind stmt;
        ExpKind  exp;
    }kind;
    //记录一个节点中标识符的个数
    int idnum;
    //字符串数组，数组成员是节点中的标识符的名字
    char name[10][10];
    //指针数组，数组成员是节点中的各个标识符在符号表中的入口
    struct symbtable *table[10];
    //记录类型名，当节点为声明类型，且类型是由类型标识符表表示时有效
    char type_name[10];
    //记录语法树节点其他属性，为结构体类型
    //成员attr:记录语法树节点的其他属性，为结构体类型
    struct 
    {
        //attr成员ArrayAttr:记录数组类型的属性
        struct 
        {
            //Arrayttr成员low:整数类型变量，记录数组的下界
            int low;
            //Arrayttr成员up:整数类型变量，记录数组的上界
            int up;
            //记录数组的成员类型
            DecKind childtype;
        }ArrayAttr;

        //attr成员procAttr:记录过程的属性
        struct 
        {
            //记录过程的参数类型 valparam or varparam 值参数或者变参数
            ParamType paramt;
        }ProcAttr;

        // attr成员ExpAttr:记录表达式的属性
        struct 
        {
            /*
            ExpAttr成员op：记录语法树节点的运算符单词，为单词类型。
				当语法树节点为“关系运算表达式”对应节点时，取值LT,EQ；
				当语法树节点为“加法运算简单表达式”对应节点时，取值为PLUS,MINUS;
				当语法树节点为“乘法运算项”对应节点时，取值TIMES,OVER；
				其他情况下无效
            */
           LexType op;
           //记录语法树节点的数值，为数字才有效
           int val;
           
           VarKind varkind;
           ExpType type;
        }ExpAttr;
    }attr;
}TreeNode;

extern std::set<LexType> NTSet;
extern std::set<LexType> TTSet;

/*清单的行号*/
//int lineno;
#endif