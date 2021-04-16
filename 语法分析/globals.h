#ifndef _GLOBALS_H_
#define _GLOBALS_H_

#include <stdio.h>
#include <stdlib.h>
#include <map>
#include <set>
#include <string>


typedef enum 
{
    //���ǵ��ʷ���
    ENDFILE,	ERROR,

    //������
    PROGRAM,	PROCEDURE,	TYPE,	VAR,		IF,
	THEN,		ELSE,		FI,		WHILE,		DO,
	ENDWH,		BEGIN,		END,	READ,		WRITE,
	ARRAY,		OF,			RECORD,	RETURN, 

    //����
    INTEGER_T,	CHAR_T,

    //���ַ����ʷ���
    ID,			INTC_VAL,		CHARC_VAL,

    //�������
	ASSIGN,		EQ,			LT,		PLUS,		MINUS,
    TIMES,DIVIDE,		LPAREN,	RPAREN,		DOT,
    COLON,		SEMI,		COMMA,	LMIDPAREN,	RMIDPAREN,
    UNDERRANGE,




    //���ս��
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
} LexType;

extern std::map<LexType,std::string> lexname;

class Token{
    public:
        Token(int line,LexType lex,std::string sem){
            this->line = line;
            this->lex = lex;
            this->sem = sem;
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


//��¼�﷨���ڵ�����
typedef enum{Prok,PheadK,DecK,TypeK,VarK,ProcDecK,StmLK,StmtK,ExpK}NodeKind;
extern std::map<NodeKind,std::string> nodeKindMap;

//DecKind ��Ա
typedef enum{ArrayK,CharK,IntegerK,RecordK,IdK} DecKind;
extern std::map<DecKind,std::string> decKindMap;

//StmtKind ��Ա
typedef enum{IfK,WhileK,AssignK,ReadK,WriteK,CallK,ReturnK}StmtKind;
extern std::map<StmtKind,std::string> stmtKindMap;


//ExpKind ��Ա
typedef enum{OpK,ConstK,VariK} ExpKind;
extern std::map<ExpKind,std::string> expKindMap;



//VarKind ��Ա
typedef enum{IdV,ArrayMembV,FieldMembV}VarKind;
extern std::map<VarKind,std::string> varKindMap;

//ExpType ��Ա
typedef enum{Void,Integer,Boolean}ExpType;
extern std::map<ExpType,std::string> expTypeMap;

//ParamType ��Ա
typedef enum{valparamType,varparamType}ParamType;
extern std::map<ParamType,std::string> paramTypeMap;


#define MAXCHILDREN 3

struct symbtable;

typedef struct treeNode{
    //ָ�����﷨���ڵ�ָ��
    struct treeNode* child[MAXCHILDREN];
    //ָ���ֵ��﷨���ڵ�ָ��
    struct treeNode* sibling;
    //��¼Դ�����к�
    int lineno;
    NodeKind nodekind;
    //��ԱKind ��¼�﷨���ڵ�ľ������ݣ�Ϊ������ṹ
    union
    {
        DecKind dec;
        StmtKind stmt;
        ExpKind  exp;
    }kind;
    //��¼һ���ڵ��б�ʶ���ĸ���
    int idnum;
    //�ַ������飬�����Ա�ǽڵ��еı�ʶ��������
    char name[10][10];
    //ָ�����飬�����Ա�ǽڵ��еĸ�����ʶ���ڷ��ű��е����
    struct symbtable *table[10];
    //��¼�����������ڵ�Ϊ�������ͣ��������������ͱ�ʶ�����ʾʱ��Ч
    char type_name[10];
    //��¼�﷨���ڵ��������ԣ�Ϊ�ṹ������
    //��Աattr:��¼�﷨���ڵ���������ԣ�Ϊ�ṹ������
    struct
    {
        //attr��ԱArrayAttr:��¼�������͵�����
        struct
        {
            //Arrayttr��Աlow:�������ͱ�������¼������½�
            int low;
            //Arrayttr��Աup:�������ͱ�������¼������Ͻ�
            int up;
            //��¼����ĳ�Ա����
            DecKind childtype;
        }ArrayAttr;

        //attr��ԱprocAttr:��¼���̵�����
        struct
        {
            //��¼���̵Ĳ������� valparam or varparam ֵ�������߱����
            ParamType paramt;
        }ProcAttr;

        // attr��ԱExpAttr:��¼���ʽ������
        struct 
        {
            /*
            ExpAttr��Աop����¼�﷨���ڵ����������ʣ�Ϊ�������͡�
				���﷨���ڵ�Ϊ����ϵ������ʽ����Ӧ�ڵ�ʱ��ȡֵLT,EQ��
				���﷨���ڵ�Ϊ���ӷ�����򵥱��ʽ����Ӧ�ڵ�ʱ��ȡֵΪPLUS,MINUS;
				���﷨���ڵ�Ϊ���˷��������Ӧ�ڵ�ʱ��ȡֵTIMES,OVER��
				�����������Ч
            */
           LexType op;
           //��¼�﷨���ڵ����ֵ��Ϊ���ֲ���Ч
           int val;
           
           VarKind varkind;
           ExpType type;
        }ExpAttr;
    }attr;
}TreeNode;

extern std::set<LexType> NTSet;
extern std::set<LexType> TTSet;

/*�嵥���к�*/
extern int lineno;
#endif
