from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

# 以chrome為例

# selenium version is under 4.6
# chrome = webdriver.Chrome(service=Service('./chromedriver'))

# selenium version is 4.6 or above
chrome = webdriver.Chrome()

chrome.get("https://www.google.com.tw/")

try:
    WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='搜尋']")))
    input_block = chrome.find_element(By.XPATH,"//textarea[@aria-label='搜尋']")
    input_block.send_keys("中央大學")
    input_block.send_keys(Keys.ENTER)

    input("Press Enter to exit...")
    
except TimeoutException as e:
    print(e)    
