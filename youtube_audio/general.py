import os
import re

#for detect if a string is english word
english_pattern = re.compile(r'[a-zA-Z]')
hebrew_pattern = re.compile(r'[\u0590-\u05EA]')
CHARS_TO_REMOVE=""
SHARPS="################################\n"


#s string if english ignore if hebrew reverse for printing
def hebrew_fix(s):
    s=str(s)
    if(s is None):
        return "None"
    if re.search(hebrew_pattern, s):
        if s.endswith("\n"):
            s=s[:-1]
            return s[::-1]+"\n"
        return s[::-1]
    return s

def deleteFile(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print("The file {path} does not exist: ".format(path))

def str_list(l, newLine=True):
    s=""
    for i in l:
        if newLine:
            s=s+i+"\n"
        else:
            s=s+i
    return s[:-1] if  newLine else s

def print_msg(msg,sharps=False,strartLine=False,endLine=False):
    if(sharps):
        if (strartLine):
            print("\n"+SHARPS+msg+"\n"+SHARPS)
        else:
            print(SHARPS+msg+"\n"+SHARPS)
    else:
        if (strartLine and endLine):
            print("\n"+msg+"\n")
        elif(strartLine):
            print("\n"+msg)
        elif(endLine):
            print(msg+"\n")
        else:
            print(msg)