import problem_parser
import requests
from bs4 import BeautifulSoup
import os

contest_id=input("Enter contest ID: ")
url="https://codeforces.com/contest/"+contest_id

req=requests.get(url)
soup=BeautifulSoup(req.content,'html5lib')

j=soup.find_all('meta', attrs={"property":"og:title"})
j=str(j)
i=j.find("-",0,len(j)-1)
k=j.find("-",i+1,len(j)-1)
contest_name=j[i+1:k].strip()

g=soup.find('select', attrs={"name":"submittedProblemIndex"})
g=str(g)
problems=[]
i=g.find('option value=',0,len(g)-1)
while(i!=-1):
  x=g.find(">",i,len(g)-1)
  y=g.find("<",x,len(g)-1)
  i=g.find('option value=',y,len(g)-1)
  problems.append(g[x+1:y].strip())

problems.pop(0)
folder="C:/Users/Rishabh Pandey/Desktop/web_scrapping"


directory=contest_name
path=os.path.join(folder,directory)
os.mkdir(path)

for problem in problems:
    problem_parser.parse_problem(contest_id,path,problem)
