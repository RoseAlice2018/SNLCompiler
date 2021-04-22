

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
