#include "parse.h"
#include "../globals.h"


/*
    产生式： <Program>::= ProgramHead DeclarePart ProgramBody
    算法说明： 该函数根据文法产生式生成语法树的根节点root，调用程序头部分分析函数，声明部分
    分析函数，程序体部分分析函数，分别为语法树的3个儿子节点。匹配程序结束标志"."
    如果处理成功，函数返回程序根节点语法树节点root；否则返回NULL
*/
TreeNode* Parse::program(){
    TreeNode *ph = programHead();
    TreeNode *dp = declarePart();
    TreeNode *pb = programBody();

    root = newRootNode();
    if (NULL != root){
        root->lineno = 0;
        if(NULL != ph) root->child[0] = ph;
        else syntaxError("need a program head");
        if(NULL != dp) root->child[1] = dp;
        
        if(NULL != pb) root->child[2] = pb;
        else syntaxError("need a program body");
    }
    //当前单词和DOT匹配
    match(DOT);
    return root;
}

//终极符匹配函数
//该函数将当前单词与函数参数给定单词相比较，如果一致，则取下一单词；否则，退出语法分析程序。
bool Parse::match(LexType expected)
{
    if(NULL != head && head->getLex() == expected){
        head = head->next;
        if(head != NULL){
            line0 = head->getLine();
            lineno = line0;
            
            return true;
        }
    }
    else 
    {
        syntaxError("ERROR not match,except:"+lexname[expected]+"get:"+lexname[head->getLex()]+"in line:"+lineno);
        return false;
    }
}

/*
    产生式：programHead ::=PROGRAM ProgramName
    程序头部处理分析程序
    该函数根据读入的单词，匹配保留字PROGRAM，然后记录程序名于程序头节点，匹配ID。
    如果处理成功，函数返回生成的程序头节点类型语法树节点；否则返回NULL。
*/

TreeNode* Parse::programHead(){
    //1. 创建新的程序头节点类型
    TreeNode* t = newPheadNode();
    //2. 当前单词和program匹配
    if(!match(PROGRAM)){
        delete t;
        t = NULL;
        return t;
    }
    //3. 新语法树节点t创建成功，且当前单词为ID，则将当前单词的语义信息赋给新语法树节点t的成员attr.name[0]，作为程序的名字。
    
}