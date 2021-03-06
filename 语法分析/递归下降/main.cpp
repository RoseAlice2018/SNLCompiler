#include <iostream>
#include <fstream>
#include "parse.h"
using namespace std;
LexType to_LexType(string t)
{
    return lexname_s[t];
}
int getLine(string line,int& begin)
{
    int temp = 0;
    for(int i = begin;i<line.size();i++)
    {
        if(line[i]>='0'&&line[i]<='9')
        {
            temp*=10;
            temp+=line[i]-'0';
        }
        else 
        {
            begin = i + 1;
            return temp;
        }
    }
    return temp;
}
LexType getLexType(string line,int& begin)
{
    string temp;
    LexType ret;
    for(int i= begin;i<line.size();i++)
    {
        if(line[i]==' ')
        {
            begin=i+1;
            //cout<<temp<<endl;
            ret = to_LexType(temp);
            return ret;
        }
        else 
        {
            temp.push_back(line[i]);
        }
    }
    return ret;
}
string getSem(string line,int begin)
{
    string temp;
    for(int i=begin;i<line.size();i++)
    {
        if(line[i]!=' ')
            temp.push_back(line[i]);
    }
    return temp;
}
Token* getToken()
{
    cout<<"getToken"<<endl;
    std::ifstream in("tokens1.txt");
    std::string line;
    Token* head = new Token();
    Token* tmp = head;
    if(in)//文件找到
    {
        while(getline(in,line))
        {
            //得到文件的一行
            cout<<line<<endl;
            int begin = 0;
            int line_num = 0;
            LexType type_this_line;
            string sem;
            //1. 得到行号
            line_num =  getLine(line,begin);
           // cout<<"line_num is  "<<line_num<<endl;
            //2. 得到LexType
            type_this_line = getLexType(line,begin);
           // cout<<"type_this_line  "<<type_this_line<<endl;
            //3. 得到sem 语义信息
            sem  = getSem(line,begin);
           // cout<<"sem  "<<sem<<endl;
            Token* temp = new Token(line_num,type_this_line,sem);
            tmp->next = temp;
            tmp = tmp->next;
        }
    }
    else 
    {
        std::cout<<"error:No Such File"<<std::endl;
    }
    return head->next;
}
void showToken(Token* tokHead)
{
    //cout<<"show token"<<endl;
    Token* tmp = tokHead;
    while(tmp!=NULL)
    {
        
        cout<<"line_num is "<<tmp->getLine()<<endl<<"LexType is :"<<tmp->getLexName()<<endl<<"sem is "<<tmp->getSem()<<endl;
        tmp=tmp->next;
    }
}
void showdeclarepart(TreeNode* treehead)
{
    if(treehead->nodekind == TypeK)
    {
        //show

        //go on
        if(treehead->sibling!=NULL)
         showdeclarepart(treehead->sibling);
    }
    else if(treehead->nodekind == VarK)
    {
        //show

        //go on
        if(treehead->sibling!=NULL)
            showdeclarepart(treehead->sibling);
    }
    else if(treehead->nodekind == ProcDecK)
    {

        //show

        return;
    }
    return;
}
void showstmchild(TreeNode* treehead)
{
    if(treehead==NULL)
        return;
    //cout<<treehead->nodekind<<endl;
    
}
void showstmLk(TreeNode* treehead)
{
    if(treehead==NULL)
        return;
    cout<<"StmLK"<<endl;
    cout<<"{"<<endl;
    showstmchild(treehead->child[0]);
    cout<<"}"<<endl;
}
void showTree(TreeNode* treehead)
{
    if(treehead==NULL)
        return ;
    cout<<"ProK"<<endl;
    cout<<"PheadK"<<treehead->name<<endl;
    printf("{\n");
    showdeclarepart(treehead->child[1]);
    showstmLk(treehead->child[2]);
    printf("}\n");    
}
int main()
{
    Token* tokenHead = getToken();
    //showToken(tokenHead);
    Parse* test = new Parse(tokenHead);
    test->run();
    TreeNode* t = test->get_parsetree_head();
    //showTree(t);
    return 0;
}

