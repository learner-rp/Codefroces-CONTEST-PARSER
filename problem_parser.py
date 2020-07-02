import requests
from bs4 import BeautifulSoup
import os
import shutil
from shutil import copy2

def extract(s):
    if(s.find('<br/>',0,len(s)-1)==-1):
        i=s.find('>',0,len(s)-1)
        j=s.find('<',i+1,len(s)-1)
        return s[i+1:j]
    newline='\n'
    i=0
    i=s.find('<pre>',i,len(s)-1)+5
    filtered_string=''
    while(True):
        j=s.find('<br/>',i,len(s)-1)
        if(j==-1):
            break
        filtered_string+=s[i:j]
        filtered_string+=newline
        i=j+5
    return filtered_string

def parse_problem(contest_id,folder,problem):

    path=os.path.join(folder,problem)
    os.mkdir(path)
    url="https://codeforces.com/contest/"+contest_id+"/problem/"+problem
    req=requests.get(url)
    
    # simple_problem_name=problem[0:problem.find('-',0,len(problem)-1)].strip()
    input_file=open(path+"/input"+problem+".txt","w")
    output_file=open(path+"/output"+problem+".txt","w")
    source_file=open(path+"/"+problem+".cpp","w")
    shutil.copy2('C:/Users/Rishabh Pandey/Desktop/Codeforces/template.cpp',path+'/'+problem+'.cpp');

    sample_input=""
    sample_output=""

    soup=BeautifulSoup(req.content,'html.parser')
    sample_test_cases=soup.find('div',{'class':'sample-test'})

    tests=sample_test_cases.find_all('div',{'class':'input'})
    for idx,test in enumerate(tests):
        current=extract(str(test.find('pre')))
        if(current[0]=='\n'):
            current=current[1:]
        sample_input+='Test #'+str(idx)+'\n'+current+'\n'

    tests=sample_test_cases.find_all('div',{'class':'output'})
    
    for idx,test in enumerate(tests):
        current=extract(str(test.find('pre')))
        if(current[0]=='\n'):
            current=current[1:]
        sample_output+='Test #'+str(idx)+'\n'+current+'\n'

    input_file.write(sample_input)
    input_file.close()
    output_file.write(sample_output)
    output_file.close()

