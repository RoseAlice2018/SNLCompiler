#ifndef PARSE_H
#define PARSE_H

#include "../globals.h"
#include "../utils.h"
#include <iostream>
class Parse
{
   public:
    TreeNode* get_parsetree_head(){
        return root;
    }
    //Parse(Token* head){};
    Parse(const Token* root);
   private:
    std::string temp_name;
    // Parse(const Token* root);
    TreeNode* program();
   public:
    void run();
   private:
    const Token* head;
    TreeNode* root;
    int line0;

    void syntaxError(std::string msg);

    bool match(LexType expected);
    //程序头部分处理分析程序
    TreeNode* programHead();
    //程序声明部分分析处理程序
    TreeNode* declarePart();
    //类型声明处理分析程序
    TreeNode* typeDec();
    /*产生式： <TypeDeclaration> ::= TYPE TypeDecList
        依据文法产生式，匹配保留字Type，分析TypeDecList
    */
    TreeNode* typeDeclaration();
    /*产生式：<TypeDecList> ::= TypeId = TypeDef;TypeDecMore;*/
    TreeNode* typeDecList();
    /*产生式：<TypeId> ::= ID */
    void typeId(TreeNode* pNode);

    void typeName(TreeNode* pNode);

    void baseType(TreeNode* pNode);

    void structureType(TreeNode* pNode);

    void arrayType(TreeNode* pNode);

    void recType(TreeNode* pNode);

    TreeNode* fieldDecList();

    void idList(TreeNode* pNode);

    void idMore(TreeNode* pNode);

    TreeNode* fieldDecMore();
    
    TreeNode* typeDecMore();

    TreeNode* varDec();

    TreeNode* varDeclaration();

    TreeNode* varDecList();

    TreeNode* varDecMore();

    
    void varIdList(TreeNode *t);

    void varIdMore(TreeNode *t);

    TreeNode *programBody();

    TreeNode *stmList();

    TreeNode *stmMore();

    TreeNode *stm();

    TreeNode *assCall();

    TreeNode *assignmentRest();

    TreeNode *conditionalStm();

    TreeNode *loopStm();

    TreeNode *inputStm();

    TreeNode *outputStm();

    TreeNode *returnStm();

    TreeNode *callStmRest();

    TreeNode *actParamList();

    TreeNode *actParamMore();

    TreeNode *mexp();

    TreeNode *simple_exp();

    TreeNode *term();

    TreeNode *factor();

    TreeNode *variable();

    void variMore(TreeNode *t);

    void fieldvarMore(TreeNode *t);

    TreeNode *fieldvar();

    TreeNode *mparam();

    TreeNode *paramMore();

    void paramList(TreeNode *t);

    TreeNode *procDec();

    void formList(TreeNode *t);

    void fidMore(TreeNode *t);

    TreeNode *procDeclaration();

    TreeNode *procBody();

    TreeNode *procDecPart();

    TreeNode *paramDecList();
};
#endif //PARSE_H