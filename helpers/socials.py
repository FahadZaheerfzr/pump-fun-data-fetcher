from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time


options = Options() 
options.add_argument("--user-data-dir=/Users/fahadzaheer/Library/Application Support/Google/Chrome/")
driver = webdriver.Chrome(options=options)

time.sleep(2)

driver.get("https://web.telegram.org")


time.sleep(5)

url = 'https://t.me/LolaSolanaCat'

name = url.split('/')[-1]

driver.find_element(By.CLASS_NAME, 'input-search-input').send_keys(name)

# Press enter
time.sleep(5)

driver.find_element(By.CLASS_NAME, 'chatlist-chat-abitbigger').click()

time.sleep(5)

