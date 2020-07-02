import problem_parser
import requests
from bs4 import BeautifulSoup
import os
import shutil
import sys
from colorama import Fore,Style,init

init()
def parse_contest(contest_id,folder):
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
    problems.append(g[x+1:y].strip().replace('.','').replace('<','').replace('>','').replace(':','').replace('/','').replace('/','').replace('|',''))
  try:
    problems.pop(0)
  except IndexError:
    print(Fore.RED+'Invalid contest Id'+Style.RESET_ALL)
    sys.exit()
  # folder="C:/Users/Rishabh Pandey/Desktop/web_scrapping"


  directory=contest_name
  path=os.path.join(folder,directory)
  try:
    os.mkdir(path)
  except FileExistsError:
    print('Contest is already parsed, to reparse delete the earlier contest and run this again')
    sys.exit()

  for problem in problems:
      problem=problem[0:problem.find("-",0,len(problem)-1)-1].strip()
      problem_parser.parse_problem(contest_id,path,problem)

