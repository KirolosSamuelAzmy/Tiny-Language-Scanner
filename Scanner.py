import re
import os
import sys
## Regex Patterns for identifier,numbers,comments and special characters
# Comments_pattern = '{(.|\n)*}'
number_pattern='[+\-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?'
identifier_pattern='^[a-zA-Z_][0-9a-zA-Z_]*$'

Reserved_Words_dict={'if':'IF',
'else':'ELSE',
'then': 'THEN',
'until' : 'UNTIL',
'read' : 'READ',
'write' : 'WRITE',
'repeat':'REPEAT',
'end':'END'}

special_characters_dict = {
'+': 'PLUS',
'-': 'MINUS',
'*': 'MULT',
'/': 'DIV',
':': 'COLON',
'=': 'EQUAL',
':=': 'ASSIGN',
'>': 'GREATERTHAN',
'<': 'LESSTHAN',
';': 'SEMICOLON',
'(': 'OPENBRACKET',
')': 'CLOSEDBRACKET'
}



open_curly_brackets=list()
closed_curly_brackets=list()
list_comments=list()
token_type_list=list()

def comment_find_open_Curly_brackets(file):
    index=0
    while index <  len(file):
        index=file.find('{',index)
        if index==-1:
            break
        open_curly_brackets.append(index)
        index+=1
    
    return open_curly_brackets
        


def comment_find_closed_curly_brackets(file):
    index2=0
    while index2 <  len(file):
        index2=file.find('}',index2)
        if index2==-1:
            break
        closed_curly_brackets.append(index2)
        index2+=1
    
    return closed_curly_brackets
        

def remove_comments(file,list_comments):
    for i in range(0,len(list_comments)):
        file=file.replace(list_comments[i],"")
    return file

def comment_parsing(file):
    for i in range (0,len(open_curly_brackets)):
        comment=file[open_curly_brackets[i]:closed_curly_brackets[i]+1]
        # comment=comment.replace("\n"," ")
        list_comments.append(comment)
    return list_comments


def Modify_code(file):
    file=file.replace("\n"," ")
   
    for key in special_characters_dict.keys():
            file=file.replace(key," "+key+" ")
    
    return file
def Lex_Analyzer(file):
    Scanning_count=0 
    Tokens=file.split()
    i=-1
    for token in Tokens:
        i+=1
        if token == ":" and Tokens[i+1]=="=" :
             Scanning_count+=1
             token_type_list.append("ASSIGN")
             f.write("\n")
             f.write("%d"%Scanning_count+")"+" "+":="+" ----> "+"ASSIGN")
             f2.write("%d"%Scanning_count+")"+" "+":="+"\n"+"ASSIGN"+"\n")
             f2.write("##########################################"+"\n")

            
        elif token =="=" and Tokens[i-1]==':':
            continue

        elif token in Reserved_Words_dict:
            Scanning_count+=1
            token_type_list.append(Reserved_Words_dict[token])
            f.write("\n")
            f.write("%d"%Scanning_count+")"+" "+token+" ----> "+Reserved_Words_dict[token])
            f2.write("%d"%Scanning_count+")"+" "+token+"\n"+Reserved_Words_dict[token]+"\n")
            f2.write("##########################################"+"\n")


        elif token in special_characters_dict:
            if token=="-":
                Number_result=re.match(number_pattern,Tokens[i-1])
                identifier_result=re.match(identifier_pattern,Tokens[i-1]) 

                if Number_result or identifier_result and Tokens[i-1] not in Reserved_Words_dict:
                    Scanning_count+=1
                    token_type_list.append(token)
                    f.write("\n")
                    f.write("%d"%Scanning_count+")"+" "+token+" ----> "+special_characters_dict[token])
                    f2.write("%d"%Scanning_count+")"+" "+token+"\n"+special_characters_dict[token]+"\n")
                    f2.write("##########################################"+"\n")
                else :
                    Number_result=re.match(number_pattern,Tokens[i+1])
                    identifier_result=re.match(identifier_pattern,Tokens[i+1]) 

                    if Number_result:
                         Scanning_count+=1
                         token_type_list.append("NUMBER") 
                         f.write("\n")
                         f.write("%d"%Scanning_count+")"+" "+"-"+Tokens[i+1]+" ----> NUMBER")
                         f2.write("%d"%Scanning_count+")"+" "+"-"+Tokens[i+1]+"\n"+"NUMBER"+"\n")
                         f2.write("##########################################"+"\n")

                    elif identifier_result:
                         Scanning_count+=1
                         token_type_list.append("IDENTIFIER")
                         f.write("\n")
                         f.write("%d"%Scanning_count+")"+" "+"-"+Tokens[i-1]+" ----> IDENTIFIER")
                         f2.write("%d"%Scanning_count+")"+" "+"-"+Tokens[i+1]+"\n"+"IDENTIFIER"+"\n")
                         f2.write("##########################################"+"\n")

            else:
                Scanning_count+=1
                token_type_list.append(special_characters_dict[token])
                f.write("\n")
                f.write("%d"%Scanning_count+")"+" "+token+" ----> "+special_characters_dict[token])
                f2.write("%d"%Scanning_count+")"+" "+token+"\n"+special_characters_dict[token]+"\n")
                f2.write("##########################################"+"\n")

        else :
            Number_result=re.match(number_pattern,token)
            identifier_result=re.match(identifier_pattern,token)
            if Number_result and token_type_list[-1] != "NUMBER":
                token_type_list.append("NUMBER")
                Scanning_count+=1
                f.write("\n")
                f.write("%d"%Scanning_count+")"+" "+token+" ---> NUMBER ")
                f2.write("%d"%Scanning_count+")"+" "+token+"\n"+"NUMBER"+"\n")
                f2.write("##########################################"+"\n")
            elif identifier_result:
                token_type_list.append("IDENTIFIER")
                Scanning_count+=1
                f.write("\n")
                f.write("%d"%Scanning_count+")"+" "+token+" ----> IDENTIFIER ")
                f2.write("%d"%Scanning_count+")"+" "+token+"\n"+"IDENTIFIER"+"\n")
                f2.write("##########################################"+"\n")



pathname = os.path.dirname(sys.argv[0])        
file=open(pathname+r'/data.txt', 'r').read()
comment_find_open_Curly_brackets(file)
comment_find_closed_curly_brackets(file)
list_comments=comment_parsing(file)
file=remove_comments(file,list_comments)
f=open(pathname+r"/scanout.txt","w+") 
f2=open(pathname+r"/tokenlist.txt","w+")
#FindingComments
#printing comments
if len(list_comments)>0:
    f.write("Comments are : \n")
    for i in range (0,len(list_comments)):
        if i==0:
            f.write(list_comments[0])
        else:
            if i==len(list_comments)-1:
                f.write("\n")
                f.write(list_comments[i])
                f.write("\n*********************************************************************")
            else :
                f.write("\n")
                f.write(list_comments[i])
        
#Removing Comments
Modified_code=Modify_code(file)
Tokens=Lex_Analyzer(Modified_code)

f.close()
f2.close()