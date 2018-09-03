## 显性等待（WebDriverWait）
Selenium中的wait模块的WebDriverWait()方法，它指定要查找的节点，并规定一个最长等待时间，配合until或者until_not方法，until 也属于WebDriverWait,代表一直等待,直到某元素可见，until_not与其相反，判断某个元素直到不存在，再辅助以一些判断条件，就可以构成这样一个场景：每经过多少秒就查看一次所查找元素是否可见，如果可见就停止等待，如果不可见就继续等待直到超过规定的时间后，报超时异常；当然也可以判断某元素是否在规定时间内不可见等，需要根据你自己实际的场景选择判断条件。

示例：
```python
from datetime import datetime
from selenium import webdriver  
from selenium.webdriver.support.wait import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
url = 'www.baidu.com'
driver.get(url)
try:


# 首先判断一个已知网页上存在的节点
    print(datetime.now())  
    # presence_of_element_located传入定位元组，主要判断页面元素kw在页面中存在。
  element = WebDriverWait(driver,5).until( EC.presence_of_element_located((By.ID, "kw"))) 
# 判断一个不存在的节点
    print(datetime.now())
 # 'kw123'为随意设置的节点id，网页中找不到
    element = WebDriverWait(driver,10).until_not( EC.presence_of_element_located((By.ID, "kw123")))


finally:
    print(datetime.now())
    driver.quit()
```

显示等待判断准确，不会浪费时间，相对来说提高了执行效率。不过使用显示等待相对比较复杂，需要根据实际需要选择。

显示等待的条件还有很多，比如判断标题内容，判断节点中包含哪些文字，判断节点是否可见等等。具体更多等待条件的参数及用法可见等待条件及其含义

斗鱼直播总界面，模拟点击下一页不断获取相应的数据的示例。
```python

动态页面模拟点击
# python的测试模块
import unittest
from bs4 import BeautifulSoup
from selenium import webdriver


class Douyu_Spider(unittest.TestCase):
    # 初始化方法
    def setUp(self):
        self.driver = webdriver.PhantomJS()


    # 具体的测试方法
    def testDouyu(self):
        url = 'http://www.douyu.com/directory/all'
        self.driver.get(url)
        while True:
            soup = BeautifulSoup(self.driver.page_source,'lxml')
            # 返回当前页面内所有房间标题列表，房间类型和观众人数
            titles = soup.find_all('h3',{'class':'ellipsis'})
            nums = soup.find_all('span',{'class':'dy-num fr'})
            categories = soup.find_all('span',{'class':'tag ellipsis'})
            # 使用zip()函数将列表合并
            for title,num,category in zip(titles,nums,categories):
                title = title.get_text().strip()
                category = category.get_text().strip()
                num = num.get_text().strip()


                print('房间名称：' + '{:<20}\t'.format(title),'房间类型：' + '{:<10}\t'.format(category),'观众人数：' + num)
            # 没有找到“下一页”时返回1
            if self.driver.page_source.find('shark-pager-disable-next') != -1:
                break
            # 模拟下一次点击
            self.driver.find_element_by_class_name('shark-pager-next').click()
 


    def tearDown(self):
        print('加载完成')
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
```

上面这个案例用到了unittest模块中的TestCase这个概念，什么是TestCase呢？一个TestCase的实例就是一个测试用例。测试用例指的是一个完整的测试流程，包括测试前准备环境的搭建(setUp)，执行测试代码(run)，以及测试后环境的还原(tearDown)。unittest是python的一个单元测试框架，用来规范与组织用例的的编写

https://zhuanlan.zhihu.com/p/38900589
