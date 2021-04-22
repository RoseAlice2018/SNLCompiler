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
            begin = begin + 1;
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
            begin++;
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
    std::ifstream in("test.txt");
    std::string line;
    Token* head = new Token();
    Token* tmp = head;
    if(in)//文件找到
    {
        while(getline(in,line))
        {
            //得到文件的一行
            int begin = 0;
            int line_num = 0;
            LexType type_this_line ;
            string sem;
            //1. 得到行号
            line_num =  getLine(line,begin);
            //2. 得到LexType
            type_this_line = getLexType(line,begin);
            //3. 得到sem 语义信息
            sem  = getSem(line,begin);
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
int main()
{
    Token* tokenHead = getToken();
    //Parse* test = new Parse(tokenHead);
   // TreeNode* t = test->get_parsetree_head();
    return 0;
}