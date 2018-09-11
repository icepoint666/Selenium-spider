import unittest
from bs4 import BeautifulSoup
from selenium import webdriver


class Douyu_Spider(unittest.TestCase):
    # 初始化方法
    def setUp(self):
        self.driver = webdriver.Firefox()

    # 具体的测试方法
    def testDouyu(self):
        url = 'http://www.douyu.com/directory/all'
        self.driver.get(url)
        while True:
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            # 返回当前页面内所有房间标题列表，房间类型和人气
            titles = soup.find_all('h3', {'class': 'ellipsis'})
            nums = soup.find_all('span', {'class': 'dy-num fr'})
            categories = soup.find_all('span', {'class': 'tag ellipsis'})
            # 使用zip()函数将列表合并
            for title, num, category in zip(titles, nums, categories):
                title = title.get_text().strip()
                category = category.get_text().strip()
                num = num.get_text().strip()

                print('房间名称：' + '{:<20}\t'.format(title), '房间类型：' + '{:<10}\t'.format(category), '人气：' + num)
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
