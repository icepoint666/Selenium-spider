from selenium import webdriver

firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--headless')
driver = webdriver.Firefox(firefox_options=firefox_options)

url = 'http://www.baidu.com'
driver.get(url)
print(driver.page_source)
driver.close()

# Finish a basic crawler Firefox+Selenium+getodriver