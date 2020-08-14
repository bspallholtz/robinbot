#!/usr/bin/python3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=800,600")
options.add_argument("--disable-dev-shm-usage")
#options.set_headless()
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
print(driver.get("https://www.tipranks.com/stocks/iova/forecast"))
exit()
#import os
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.options import Options

#chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.binary_location = '/opt/google/chrome/chrome'

#driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),chrome_options=chrome_options)
#driver.get("http://www.duo.com")
