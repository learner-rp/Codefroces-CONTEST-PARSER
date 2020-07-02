import login
import contest_parser
import os
from os import system,path
import requests
from bs4 import BeautifulSoup

def get_contest_name(contest_id):
    url="https://codeforces.com/contest/"+contest_id

    req=requests.get(url)
    soup=BeautifulSoup(req.content,'html5lib')

    j=soup.find_all('meta', attrs={"property":"og:title"})
    j=str(j)
    i=j.find("-",0,len(j)-1)
    k=j.find("-",i+1,len(j)-1)
    contest_name=j[i+1:k].strip()
    return contest_name

contest_id=""
user_id=""
password=""
contest_name=""

folder="C:/Users/Rishabh Pandey/Desktop/Codeforces"
cookies_location = "C:/Users/Rishabh Pandey/Desktop/Codeforces/cookies.txt"

print("Choose option: ")
print("Type 1 for parsing the contest")
print("Type 2 to submit your problem")

inp=input()

if(inp=='1'):
    contest_id=input('Enter contest Id to be parsed: ')
    contest_parser.parse_contest(contest_id,folder)

else:
    if(os.path.getsize(cookies_location)==0):
        user_id=input('Enter user id: ')
        password=input('Enter password: ')
        login.login_codeforces(cookies_location,user_id,password,contest_id)
    # contest_name=get_contest_name(contest_id)
    problem=input('Enter the problem to submit, Example: to submit problem "1370 A" type 1370 A, for "1374 E1" type 1374 E1 ')
    details=problem.split()
    contest_id=details[0]
    submit_problem=details[1]
    contest_name=get_contest_name(contest_id)
    if(path.exists(folder+'/'+contest_name)):
        login.login_codeforces(cookies_location,user_id,password,contest_id,submit_problem)
    else:
        print('Contest is not yet parsed')


