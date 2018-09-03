from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

def get_index_page(page):
    print("Get from page {}.".format(page))
    url = 'https://s.taobao.com/search?q=' + keyword
    driver.get(url)

    element = wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                            '#spulist-pager > div > div > div > ul > li.item.active'), str(1)))

    if page >= 1:
        inp = wait.until(EC.presence_of_all_elements_located((By.XPATH,
                            '//div[@class="form"]/input')))
        sub = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                            '#spulist-pager > div > div > div > div.form > span.btn.J_Submit')))

        # Go to the specified page
        driver.find_element_by_xpath('//div[@class="form"]/input').clear()
        driver.find_element_by_xpath('//div[@class="form"]/input').send_keys(str(page))
        driver.find_element_by_css_selector('#spulist-pager > div > div > div > div.form > span.btn.J_Submit').click()

        # View the page slowly to load item information ( Otherwise, driver can't load all the item info.)
        js = "var q=document.documentElement.scrollTop=1000"
        driver.execute_script(js)
        time.sleep(2)
        js = "var q=document.documentElement.scrollTop=1500"
        driver.execute_script(js)
        time.sleep(2)
        js = "var q=document.documentElement.scrollTop=2000"
        driver.execute_script(js)
        time.sleep(2)
        js = "var q=document.documentElement.scrollTop=2500"
        driver.execute_script(js)
        time.sleep(2)
        js = "var q=document.documentElement.scrollTop=3000"
        driver.execute_script(js)
        time.sleep(2)
        js = "var q=document.documentElement.scrollTop=3500"
        driver.execute_script(js)
        time.sleep(2)
        js = "var q=document.documentElement.scrollTop=4000"
        driver.execute_script(js)
        time.sleep(2)
        js = "var q=document.documentElement.scrollTop=4500"
        driver.execute_script(js)
        time.sleep(2)


if __name__ == '__main__':
    driver = webdriver.Firefox()

    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    keyword = "笔记本电脑"

    for i in range(1, 19):
        get_index_page(i)