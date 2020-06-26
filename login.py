from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from colorama import Fore, Style, init
import pickle
import os
import time

#########################################

def save_cookies(driver, location):
    pickle.dump(driver.get_cookies(), open(location, "wb"))


def load_cookies(driver, location, url=None):
    cookies = pickle.load(open(location, "rb"))
    driver.delete_all_cookies()
    # have to be on a page before you can add any cookies, any page - does not matter which
    driver.get("https://google.com" if url is None else url)
    for cookie in cookies:
        if isinstance(cookie.get('expiry'), float):#Checks if the instance expiry a float 
            cookie['expiry'] = int(cookie['expiry'])# it converts expiry cookie to a int 
        driver.add_cookie(cookie)


def delete_cookies(driver, domains=None):

    if domains is not None:
        cookies = driver.get_cookies()
        original_len = len(cookies)
        for cookie in cookies:
            if str(cookie["domain"]) in domains:
                cookies.remove(cookie)
        if len(cookies) < original_len:  # if cookies changed, we will update them
            # deleting everything and adding the modified cookie object
            driver.delete_all_cookies()
            for cookie in cookies:
                driver.add_cookie(cookie)
    else:
        driver.delete_all_cookies()

class wait_for_the_attribute_value(object):
    def __init__(self, locator, attribute, value):
        self.locator = locator
        self.attribute = attribute
        self.value = value

    def __call__(self, driver):
        try:
            element_attribute = EC._find_element(driver, self.locator).get_attribute(self.attribute)
            return element_attribute == self.value
        except StaleElementReferenceException:
            return False

#########################################

init()

cookies_location = "C:/Users/Rishabh Pandey/Desktop/web_scrapping/cookies.txt"

userid = 'learner_rp' #input("Enter Handle/E-mail: ")
password = 'rilosh@1312' #input("Enter Password: ")
contest_id= '1370' #input("Enter Contest Id: ")
url='https://codeforces.com/enter?back=%2F/'

chromedriver="C:/Users/Rishabh Pandey/Downloads/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(chromedriver)
wait=WebDriverWait(driver,10,0.05)
driver.minimize_window()
try:
    driver.get(url)
    element=wait.until(EC.element_to_be_clickable((By.ID,'handleOrEmail')))
    element.send_keys(userid)
    element=wait.until(EC.element_to_be_clickable((By.ID,'password')))
    element.send_keys(password)
    element.send_keys(Keys.RETURN)
        
except:
    print(Fore.RED+'Poor Internet Connection'+Style.RESET_ALL)
    
else:

    try:
        url='https://codeforces.com/contest/'+contest_id+'/submit'
        wait.until(EC.title_is('HTTP Status 500 – Internal Server Error'))
        driver.get(url)

    except :
        print(Fore.RED+'Invalid Log-in Credentials'+Style.RESET_ALL)


    else:
        element=wait.until(EC.element_to_be_clickable((By.NAME,'submittedProblemIndex')))
        sel=Select(element)
        sel.select_by_value('A')
        element=wait.until(EC.element_to_be_clickable((By.NAME,'programTypeId')))
        sel=Select(element)
        sel.select_by_visible_text('GNU G++17 7.3.0')
        element=wait.until(EC.element_to_be_clickable((By.NAME,'sourceFile')))
        element.send_keys('C:/Users/Rishabh Pandey/Desktop/web_scrapping/1370A.cpp')
        element=wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "submit")))
        element.click()
        try:
            element=wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME,'error for__sourceFile'),'You have submitted exactly the same code before'))
        
        except:
           print(Fore.RED+'You have submitted exactly the same code before'+Style.RESET_ALL)
        
finally:
    temp_wait=wait.until(wait_for_the_attribute_value((By.XPATH,'//*[@id="pageContent"]/div[2]/div[6]/table/tbody/tr[2]/td[6]'),'waiting','false'))
    element=wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="pageContent"]/div[2]/div[6]/table/tbody/tr[2]')))
    v=''
    s = [elem.text for elem in element]
    verdict = (v.join(s)).split()
    print('Submission #: ',verdict[0])
    if(verdict[10]=='Accepted'):
        print('Verdict: '+Fore.GREEN+verdict[10]+Style.RESET_ALL)
        print('Time: '+verdict[11]+' '+verdict[12])
        print('Memory: '+verdict[13]+' '+verdict[14])
    else:
        wrong=''
        for i in range(10,len(verdict)-4):
            wrong=wrong+' '+verdict[i]
        print('Verdict: '+Fore.RED+wrong+Style.RESET_ALL)
    #driver.close()