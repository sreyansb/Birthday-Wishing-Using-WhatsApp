from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import mysql.connector
from datetime import datetime
import os

def sendwishes(x,event="Birthday"):
    PATH="C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=C:/Users/sreya/yo/User_Data')

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

            inp_xpath = "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]"
            input_box = WebDriverWait(driver,20).until(EC.presence_of_element_located((
                By.XPATH, inp_xpath)))
            time.sleep(5)
            string="Happy "+event+"!"
            input_box.send_keys(string)
            time.sleep(1)
            input_box.send_keys(Keys.ENTER)
            time.sleep(2)
            print("Successfully Send Message to : "+ target + '\n')
            print("DONE")
    except:
        print()
    finally:
        print("DONE all")
        #whenever qr code dena padega, usko driver.quit() nahi karke
        #khud hi quit karna hoga->manually
        driver.quit()

def fn(curday,curmonth):
    curday=str(curday)
    curmonth=str(curmonth)
    f=open("C:/Users/sreya/Downloads/birthdays.csv","r")
    s=f.readlines()
    f.close()
    s=s[1:]
    res=[i[-1] for i in s if (i[1]==curday and i[2]==curmonth)]
    flag=1
    if res:
        flag=0
        sendwishes(res)
    else:
        print("NO birthday")
    time.sleep(1)
    
    f=open("C:/Users/sreya/Downloads/anniversaries.csv","r")
    s=f.readlines()
    f.close()
    s=s[1:]
    
    res=[i[-1] for i in s if (i[1]==curday and i[2]==curmonth)]
    if res:
        flag=0
        sendwishes(res,"Anniversary")
    else:
        print("NO anniversaries")
    if flag:
        sendwishes(["me"],"NONE")
    time.sleep(1)

curday=str(datetime.now().day)
curmonth=str(datetime.now().month)
fn(curday,curmonth)

'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import mysql.connector
from datetime import datetime
import os

def sendwishes(x,event="Birthday"):
    PATH="C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=C:/Users/sreya/yo/User_Data')

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

            inp_xpath = "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]"
            input_box = WebDriverWait(driver,20).until(EC.presence_of_element_located((
                By.XPATH, inp_xpath)))
            time.sleep(5)
            string="Happy "+event+"!"
            input_box.send_keys(string)
            time.sleep(1)
            input_box.send_keys(Keys.ENTER)
            time.sleep(2)
            print("Successfully Send Message to : "+ target + '\n')
            print("DONE")
    except:
        print()
    finally:
        print("DONE all")
        #whenever qr code dena padega, usko driver.quit() nahi karke
        #khud hi quit karna hoga->manually
        driver.quit()

def fn(curday,curmonth):
    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="mydatabase")
    myc=mydb.cursor()
    sql=("SELECT name_as_per_whatsapp from birthdays where DAY=%s and MONTH=%s")
    myc.execute(sql,(curday,curmonth))#for %s ->curday
    res=myc.fetchall()#many people can have birthdays on same day
    res=[x[0] for x in res]
    k=res.copy()
    if res:
        sendwishes(res)
    else:
        print("NO birthday")
    time.sleep(1)
    sql=("SELECT name_as_per_whatsapp from anniversaries where DAY=%s and MONTH=%s")
    myc.execute(sql,(curday,curmonth))
    res=myc.fetchall()#many people can have anniversaries on same day
    res=[x[0] for x in res]
    k+=res
    if res:
        sendwishes(res,"Anniversary")
    else:
        print("NO anniversaries")
    if not(k):
        sendwishes(["me"],"NONE")
    time.sleep(1)
    mydb.close()

curday=str(datetime.now().day)
curmonth=str(datetime.now().month)
os.system("start C:/xampp/xampp-control.exe")
time.sleep(25)
fn(curday,curmonth)
os.system("taskkill /f /im xampp-control.exe")
'''

"""
c=input("FIND EVENTS?")
if c=='Y' or c=='y':
    curday=input("DAY")
    curmonth=input("MONTH")
    fn(curday,curmonth)"""


    
""" 
import mysql.connector
#To create a new schema
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    #passwd='##############'
    )
myc=mydb.cursor()
myc.execute("CREATE schema mydatabase")
"""
"""
#TO create a table within it
#using the database/schema mydatabase
import mysql.connector

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    database="mydatabase")

myc=mydb.cursor()
s='''Create table anniversaries
    (id int not null AUTO_INCREMENT PRIMARY KEY,
     DAY int,
     MONTH int check(MONTH>0 and MONTH<13),
     Name_as_per_whatsapp varchar(100));
     ALTER table birthdays AUTO_INCREMENT=1;'''
#problems ho sakti hai idhar.multi hata dena->error aayega, waapas multi daal dena
myc.execute(s,multi=True)
myc.execute("SHOW TABLES")
"""


"""
#inserting records within the table birthdays.
#using the database/schema mydatabase
import mysql.connector
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    database="mydatabase")
myc=mydb.cursor()
#multi=True when multiple queries in s
s='''Insert into anniversaries(DAY,MONTH,name_as_per_whatsapp) values
    (5,2,"Minaxi Bothra"),
    (5,2,"Sanjeev Bothra"),
    (23,11,"Rohit Giya"),
    (17,4,"Pankaj Giya"),
    (17,4,"Preeti Giya")
    ;'''
myc.execute(s)#doesn't push a tuple into the table
mydb.commit()#very important
"""
