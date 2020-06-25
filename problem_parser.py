import requests
from bs4 import BeautifulSoup
import os

def parse_problem(contest_id,folder,problem_name):
    
    idx=problem_name.find("-",0,len(problem_name)-1)
    problem=problem_name[0:idx-1]

    path=os.path.join(folder,problem_name)
    os.mkdir(path)
    url="https://codeforces.com/contest/"+contest_id+"/problem/"+problem
    req=requests.get(url)

    input_file=open(path+"/input"+problem+".txt","w")
    output_file=open(path+"/output"+problem+".txt","w")

    sample_input=""
    sample_output=""

    soup=BeautifulSoup(req.content,'html5lib')
    sample_test_cases=soup.find_all('pre')

    for idx,obj in enumerate(sample_test_cases):
        current=obj.text
        t=str(idx//2)
        if(idx%2==0):
            sample_input+="Test #"+t+"\n"+current+"\n"
        else:
            sample_output+="Test #"+t+"\n"+current+"\n"

    input_file.write(sample_input)
    output_file.write(sample_output)

    input_file.close()
    output_file.close()


