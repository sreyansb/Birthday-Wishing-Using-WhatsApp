from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import os

def sendwishes(x,event="Birthday"):
    PATH="C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=C:/Users/sreyans/yo/User_Data')

    driver = webdriver.Chrome(executable_path=PATH,options=options)
    driver.get('https://web.whatsapp.com/')
    try:
        #wait for max 200s
        #whatsapp loads but the search button does not appear and hence WebDriverWait to wait until search loads
        initi = WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]")))
        #initi = WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.CLASS_NAME, "C28xL")))
        for target in x:
            print("Wishing",target,"on their",event)
            input_box_search=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]')
            input_box_search.click()
            input_box_search.send_keys(target,Keys.ENTER)
            print("Target Successfully Selected")
            time.sleep(1)
            '''/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]/div/div[1]'''
            #inp_xpath = "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[1]"
            #inp_xpath="/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]/div/div[1]"
            #inp_xpath="/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/div/div[2]/div[1]"
            inp_xpath="/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]"
            input_box = WebDriverWait(driver,20).until(EC.presence_of_element_located((
                By.XPATH, inp_xpath)))
            print(input_box)
            string="Happy "+event+"!\n"
            time.sleep(3)
            input_box.send_keys(string)
            time.sleep(4)
            input_box.send_keys(Keys.ENTER)
            time.sleep(3)
            print("Successfully Send Message to : "+ target + '\n')
            print("DONE")
    except Exception as E:
        print(E)
    finally:
        print("DONE all")
        #whenever qr code dena padega, usko driver.quit() nahi karke
        #khud hi quit karna hoga->manually
        driver.quit()

def fn(curday,curmonth):
    
    #print(curday,curmonth,type(curday))
    f=open("C:/Users/sreyans/Downloads/birthdays.tsv","r")
    s=f.readlines()
    f.close()
    s=s[1:]
    s=[i.strip("\n").split("\t") for i in s]
    #print(s)
    res=[i[3] for i in s if (int(i[1])==curday and int(i[2])==curmonth)]
    print(res)
    flag=1
    if res:
        flag=0
        sendwishes(res)
    else:
        print("NO birthday")
    time.sleep(1)
    
    f=open("C:/Users/sreyans/Downloads/anniversaries.tsv","r")
    s=f.readlines()
    f.close()
    s=s[1:]
    s=[i.split("\t") for i in s]
    #print(s)
    res=[i[3] for i in s if (int(i[1])==curday and int(i[2])==curmonth)]
    if res:
        flag=0
        sendwishes(res,"Anniversary")
    else:
        print("NO anniversaries")
    if flag:
        sendwishes(["me"],"NONE")
    time.sleep(1)

curday=(datetime.now().day)
curmonth=(datetime.now().month)
fn(curday,curmonth)
