from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from datetime import datetime

BIRTHDAY_FILE_LOCATION = "<file where you keep your people's birthdays in a TSV format. First line is id\tday\tmonth\tname_as_per_whatsapp. Next lines follow the pattern >"
ANNIVERSARY_FILE_LOCATION = "<file where you keep your people's anniversaries in a TSV format. First line is id\tday\tmonth\tname_as_per_whatsapp. Next lines follow the pattern >"
BIRTHDAY_GREETING = "Happy Birthday!"
ANNIVERSARY_GREETING = "Happy Anniversary!"
CHROME_DRIVER_PATH = "<location of the chromedriver. Can be downloaded from https://chromedriver.chromium.org/downloads>"
USER_DATA_DIRECTORY = "<data directory to store session data between multiple chrome sessions (so as to avoid scanning Whatsapp QR every time)>"
WEB_DRIVER_STARTUP_TIME_IN_SECONDS = 200
WHATSAPP_SEARCH_BAR_XPATH = "/html/body/div[1]/div/div/div[3]/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div/p"
WHATSAPP_LOADING_TIME_IN_SECONDS = 20
WHATSAPP_SEARCH_SANITY_DELAY_IN_SECONDS = 1
WHATSAPP_CHAT_MESSAGE_BOX_XPATH = "/html/body/div[1]/div/div/div[3]/div/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p"
WHATSAPP_MESSAGE_PUBLISHING_DELAY_IN_SECONDS = 6
WHATSAPP_PER_CHAT_LOAD_TIME_IN_SECONDS=20
WHATSAPP_PERSONAL_CHANNEL_NAME = "<your personal group / private channel to notify if nobody has an event on the current day>"

def wish_sender(people_and_event_tuples):
    
    PATH=CHROME_DRIVER_PATH
    options = webdriver.ChromeOptions()
    user_data_directory = f"--user-data-dir={USER_DATA_DIRECTORY}"
    print(user_data_directory)
    options.add_argument(user_data_directory)
    driver = webdriver.Chrome(options=options, service=webdriver.ChromeService(executable_path=os.path.join(os.getcwd(), PATH)))
    driver.get('https://web.whatsapp.com/')
    
    try:
        web_drver_initializer = WebDriverWait(driver, WEB_DRIVER_STARTUP_TIME_IN_SECONDS).until(
            expected_conditions.presence_of_element_located(
                tuple([By.XPATH, WHATSAPP_SEARCH_BAR_XPATH])
            )
        )
        time.sleep(WHATSAPP_LOADING_TIME_IN_SECONDS)
        for person_to_be_wished, wish in people_and_event_tuples:
            print(f"{person_to_be_wished} : {wish}")

            whatsapp_search_box=driver.find_element(by = By.XPATH, value = WHATSAPP_SEARCH_BAR_XPATH)
            time.sleep(WHATSAPP_SEARCH_SANITY_DELAY_IN_SECONDS)
            whatsapp_search_box.click()
            whatsapp_search_box.send_keys(person_to_be_wished,Keys.ENTER)
            print("Target Successfully Selected")
            time.sleep(WHATSAPP_SEARCH_SANITY_DELAY_IN_SECONDS)

            chat_message_box = WebDriverWait(driver,WHATSAPP_PER_CHAT_LOAD_TIME_IN_SECONDS).until(
                expected_conditions.presence_of_element_located(
                    tuple([By.XPATH, WHATSAPP_CHAT_MESSAGE_BOX_XPATH])
                )
            )
            wish_to_be_sent=f"{wish}\n"
            time.sleep(WHATSAPP_MESSAGE_PUBLISHING_DELAY_IN_SECONDS)
            chat_message_box.send_keys(wish_to_be_sent)
            time.sleep(WHATSAPP_MESSAGE_PUBLISHING_DELAY_IN_SECONDS)
            chat_message_box.send_keys(Keys.ENTER)
            time.sleep(WHATSAPP_MESSAGE_PUBLISHING_DELAY_IN_SECONDS)
            print(f"Successfully sent message to : {person_to_be_wished}")
    except Exception as exception:
        print(f"THERE IS AN EXCEPTION {exception}")
    finally:
        print("DONE all")
        '''
        Whenever you have to login for the first time or relogin i.e. basically scan the QR code,
        you have to comment the following line and manually quit the browser yourself
        '''
        driver.quit()


def determine_people_to_be_wished(file_name, current_day, current_month):
    file_of_people = open(file_name)
    file_content = file_of_people.readlines()
    file_of_people.close()
    all_people_with_their_respective_event_dates = [line.strip("\n").split("\t") for line in file_content[1:]]
    people_to_be_wished = [
        line[3].strip() for line in all_people_with_their_respective_event_dates if (int(line[1])==current_day and int(line[2])==current_month)
    ]
    return people_to_be_wished



def orchestrate_wish_sending(current_day,current_month):

    people_whose_birthday_is_today = determine_people_to_be_wished(BIRTHDAY_FILE_LOCATION, current_day, current_month)
    people_whose_anniversary_is_today = determine_people_to_be_wished(ANNIVERSARY_FILE_LOCATION, current_day, current_month)
    all_wishes_to_be_sent = [(birthday_person, BIRTHDAY_GREETING) for birthday_person in people_whose_birthday_is_today] 
    all_wishes_to_be_sent.extend([(anniversary_person, ANNIVERSARY_GREETING) for anniversary_person in people_whose_anniversary_is_today])
    if not all_wishes_to_be_sent:
        all_wishes_to_be_sent = [(WHATSAPP_PERSONAL_CHANNEL_NAME, "Happy None!")]
    print(all_wishes_to_be_sent)
    wish_sender(all_wishes_to_be_sent)



current_day=(datetime.now().day)
current_month=(datetime.now().month)
orchestrate_wish_sending(current_day,current_month)
