
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import getpass
from tkinter import filedialog as fd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from App_Logging import getLogger
# driver = webdriver.Chrome("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
logger = getLogger('app.py')
    # while True:
    #     continue


def subscribe(df:object, driver:object) -> bool:

    for row in df.itertuples():

        # time.sleep(3)
        sub_url = row[2]
        sub_name = row[3]
        logger.info(f"subscribing - {sub_name} - {sub_url}")
        driver.get(sub_url)   
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#logo-icon")))

        try:
            sub_status = driver.find_element(By.CSS_SELECTOR, "#subscribe-button > ytd-subscribe-button-renderer > tp-yt-paper-button").get_attribute("aria-label")
        except NoSuchElementException:
            terminated_sub = driver.find_element(By.CSS_SELECTOR, "#container").get_attribute("class")
            if "ERROR" in terminated_sub:
                logger.info(f"{sub_name} has been terminated! skip!")
            continue

        if "Unsubscribe" in sub_status:
            logger.info(f"{sub_name} was subscribed previously! skip!")
            continue
        else:
            btn_subscribe = driver.find_element(By.CSS_SELECTOR, "#subscribe-button")
            btn_subscribe.click()
            logger.info(f"{sub_name} was successfully subscribed!")
        
    return True
       

if __name__ == '__main__':
    
    logger.info("-----------------------------App is launching!!!-----------------------------")
    
    filename = fd.askopenfilename(title="pleas select the CSV !!! : ) ")
    logger.info(" {} is in use".format(filename))

    csv = pd.read_csv(filename)

    user = input("Youtube User: ")
    pw = getpass.getpass("Youtube Password: ")

    driver.get("https://www.youtube.com/")
    
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#topbar > div > div:nth-child(2) > ytd-button-renderer > a")))
    btn_signin = driver.find_element(By.CSS_SELECTOR, "#topbar > div > div:nth-child(2) > ytd-button-renderer > a")
    btn_signin.click()

    input_email = driver.find_element(By.CSS_SELECTOR, "#identifierId")
    input_email.send_keys(user)

    btn_next = driver.find_element(By.CSS_SELECTOR, "#identifierNext > div > button")
    btn_next.click()

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#password > div > div > div > input")))
    input_pw = driver.find_element(By.CSS_SELECTOR, "#password > div > div > div > input")
    input_pw.send_keys(pw)

    btn_next = driver.find_element(By.CSS_SELECTOR, "#passwordNext > div > button")
    btn_next.click()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#search")))

    if subscribe(csv, driver):
        logger.info("Done!")

    
    
    

    