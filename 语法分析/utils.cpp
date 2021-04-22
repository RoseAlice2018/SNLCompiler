//
// Created by tender on 18-5-11.
//

#include "utils.h"
#include <cstring>

TreeNode *newRootNode() {
    return newSpecNode(Prok);
}


TreeNode *newPheadNode() {
    return newSpecNode(PheadK);
}


TreeNode *newDecANode(NodeKind kind) {
    return newSpecNode(kind);
}



//尝试
/********************************************************/
/* 功  能 类型标志语法树节点创建函数					*/
/********************************************************/
TreeNode *newTypeNode() {
    return newSpecNode(TypeK);
}

/********************************************************/
/* 功  能 变量声明标志语法树节点创建函数				*/
/********************************************************/
TreeNode *newVarNode() {
    return newSpecNode(VarK);
}







/********************************************************/
/* 功  能 创建声明类型语法树节点函数					*/
/********************************************************/
TreeNode *newDecNode() {
    return newSpecNode(DecK);
}


/********************************************************/
/* 功  能 创建函数类型语法树节点函数					*/
/********************************************************/
TreeNode *newProcNode() {
    return newSpecNode(ProcDecK);
}

/********************************************************/
/* 功  能 创建语句标志类型语法树节点函数				*/
/********************************************************/
TreeNode *newStmlNode() {
    return newSpecNode(StmLK);
}

/********************************************************/
/* 功  能 创建语句类型语法树节点函数					*/
/********************************************************/
TreeNode *newStmtNode(StmtKind kind) {
    TreeNode* t = newSpecNode(StmtK);

    t->kind.stmt = kind;
    return t;
}


/********************************************************/
/* 功  能 表达式类型语法树节点创建函数					*/
/********************************************************/
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
