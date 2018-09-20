from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml.html import etree
import xlwt

if __name__ == '__main__':
    # 定义驱动依赖的浏览器为Firefox
    driver = webdriver.Firefox()

    driver.maximize_window()
    # 定义驱动最大响应时间，等待超过10s就会报错
    wait = WebDriverWait(driver, 10)
    # 抓取的初始链接
    url = "http://apps.webofknowledge.com"
    # 抓取刊物发行年份
    year = '2016'

    # 连接前面指定的url
    driver.get(url)
    inp = wait.until(EC.presence_of_all_elements_located((By.XPATH,
                                                          '//div[@class="block-search block-search-header"]')))

    # 切换到 advanced search 模式
    driver.find_element_by_xpath('//div[@class="block-search block-search-header"]/div[1]/ul[1]/li[3]/a').click()
    # 等待直到advanced search页面加载出来
    sub = wait.until(EC.presence_of_all_elements_located((By.XPATH,
                                                          '//form[@id="UA_AdvancedSearch_input_form"]')))
    # 清除搜索框里的内容
    driver.find_element_by_xpath(
        '//form[@id="UA_AdvancedSearch_input_form"]/div[1]/table/tbody/tr/td[1]/div[@class="AdvSearchBox"]/textarea').clear()

    # 输入搜索字段
    adv_search_words = "SO=(INTERNATIONAL JOURNAL OF MACHINE LEARNING \"AND\" CYBERNETICS) AND PY=" + year
    driver.find_element_by_xpath(
        '//form[@id="UA_AdvancedSearch_input_form"]/div[1]/table/tbody/tr/td[1]/div[@class="AdvSearchBox"]/textarea').send_keys(
            adv_search_words)

    # 点击搜索按钮
    driver.find_element_by_xpath(
        '//form[@id="UA_AdvancedSearch_input_form"]/div[1]/table/tbody/tr/td[1]/div[@class="AdvSearchBox"]/div[1]/table/tbody/tr/td[1]/span[1]/button').click()

    # 之后在下方的搜索历史中点击最近的搜索结果
    driver.find_element_by_xpath('//div[@class="block-history"]/form/table/tbody/tr[3]/td[2]/div/a').click()
    sub1 = wait.until(EC.presence_of_all_elements_located((By.XPATH,
                                                            '//div[@class="EPAMdiv main-container"]')))

    # 获取当前响应的html页面文档
    html = driver.page_source
    html_lxml = etree.HTML(html)

    # 获取总页数
    pages = int(str(html_lxml.xpath('//span[@id="pageCount.top"]/text()')[0]))

    # 表示论文编号，从1开始计数
    count = 1

    # 存放论文各项信息的列表
    infos = []

    # 存放论文引用文章的页面链接地址
    hrefs = []

    # 表示论文各项信息的xpath
    prefix = '//span[@id="records_chunks"]/div[@class="search-results"]/div[@id="RECORD_'
    posfix = ['"]/div[@class="search-results-content"]/div[1]/div[1]/a/value/text()',
              '"]/div[@class="search-results-content"]/div[2]/text()',
              '"]/div[@class="search-results-content"]/div[3]/value/span/text()',
              '"]/div[@class="search-results-content"]/div[3]/span[last()-3]/value/text()',
              '"]/div[@class="search-results-content"]/div[3]/span[last()-1]/value/text()',
              '"]/div[@class="search-results-data"]/div[1]/a/text()',
              '"]/div[@class="search-results-data"]/div[1]/a/@href']
    # 从每个page爬取所有文章
    for page in range(pages):
        # 获取当前page的html页面文档
        html = driver.page_source
        html_lxml = etree.HTML(html)
        # 从1-10每条信息，因为一页最多加载10条信息
        for i in range(1,11):
            num = str(count)
            # 存放爬到的每个paper的信息
            data = []
            # 加上前面计数的编号
            data.append(str(count))
            # 因为最后一页不一定有10条信息，所以判定如果最后一页的最后一条信息已经爬取，那么爬到的是个空的list，所以len=0就表示已经不用再爬了，break
            if len(html_lxml.xpath(prefix + num + posfix[0])) == 0:
                break
            data.append(str(html_lxml.xpath(prefix + num + posfix[0])[0])) # 文章标题
            data.append(str(html_lxml.xpath(prefix + num + posfix[1])[1])) # 文章作者
            data.append(str(html_lxml.xpath(prefix + num + posfix[2])[0])) # 文章所属刊物/会议
            data.append(str(html_lxml.xpath(prefix + num + posfix[3])[0])) # 文章页码
            data.append(str(html_lxml.xpath(prefix + num + posfix[4])[0])) # 文章发行时间
            # 如果cited times = 0 那么将会不显示链接，所以把空字符串加入到存放cited信息的list中，后面判断的时候直接看是后为空就可以判断
            if len(html_lxml.xpath(prefix + num + posfix[5])) == 0:
                data.append(str(0))
                hrefs.append("")
            # 如果cited times > 0 就把链接保存到list中去
            else:
                data.append(str(html_lxml.xpath(prefix + num + posfix[5])[0]))
                tmp_str = str(html_lxml.xpath(prefix + num + posfix[6])[0])
                # 因为爬下来的链接没有加网页地址的前缀，所以我们加上
                hrefs.append('http://apps.webofknowledge.com' + tmp_str)
            # 把单个paper的信息列表，添加到总列表里
            infos.append(data)
            # 计数+1
            count = count + 1
        # 如果到达最后一页，因为没有下一页的按钮可以点击，防止下一行报错，提前判定，如果是最后一页，那么提前终止
        if page == pages - 1:
            break
        # 点击下一页按钮
        driver.find_element_by_xpath('//i[@class="snowplow-navigation-nextpage-top"]').click()
    #print(infos)
    #print(hrefs)
    # 存放引用论文年份信息的列表，每一行表示一个论文的信息，各列分别表示（网站）检索到的所有引用数，15，16，17，18文章引用次数，最后一项表示18年自引用数（共6项）
    href_infos = []
    for i,href in enumerate(hrefs):
        h_info = []
        # 如果是前面添加的空链接，表示0引用数，全添加为0
        if href == '':
            h_info.append("0")
            h_info.append('0')
            h_info.append('0')
            h_info.append('0')
            h_info.append('0')
            h_info.append('0')
        # 表示前面有添加该文章链接
        else:
            # 访问该链接
            driver.get(href)

            # 重置各年份引用数
            num_2015 = 0
            num_2016 = 0
            num_2017 = 0
            num_2018 = 0
            num_self_2018 =  0

            html = driver.page_source
            html_lxml = etree.HTML(html)
            # 如果存在这样的情况，引用数不为0，但是检索到引用数为0，这样的情况页面会产生error，所以如果检测到html页面中有这个error的标签，自动当0引用数处理
            if len(html_lxml.xpath('//div[@id="noRecordsDiv"]/text()')) > 0:
                h_info.append("0")
                h_info.append('0')
                h_info.append('0')
                h_info.append('0')
                h_info.append('0')
                h_info.append('0')
                href_infos.append(h_info)
                continue
            pages_v2 = int(str(html_lxml.xpath('//span[@id="pageCount.top"]/text()')[0]))
            pre = '(//span[@id="records_chunks"]/div[@class="search-results"]/div[@id="RECORD_'
            cnt = 1
            pos = '"]/div[@class="search-results-content"]/div[last()-2]/span[@class="data_bold"])[last()]/value/text()'
            # 进入文章的引用文章列表，对每一页进行爬取
            for page_v2 in range(pages_v2):
                # 获取html页面文档
                html = driver.page_source
                html_lxml = etree.HTML(html)
                # 原理同上最多有10条信息
                for i in range(1, 11):
                    subnum = str(cnt)
                    if len(html_lxml.xpath(pre + subnum + pos)) == 0:
                        break
                    # 爬取表示年份的标签，获取发行年份，因为那个标签text字符串后四位必然是年份，所以取后四位
                    year_info = str(html_lxml.xpath(pre + subnum + pos)[0])[-4:]
                    # 判断并添加，这里在2018里面可以加个对是不是引用自己期刊的判定（未完成）
                    if int(year_info) == 2015:
                        num_2015 = num_2015 + 1
                    elif int(year_info) == 2016:
                        num_2016 = num_2016 + 1
                    elif int(year_info) == 2017:
                        num_2017 = num_2017 + 1
                    elif int(year_info) == 2018:
                        num_2018 = num_2018 + 1
                    else:
                        pass

                    cnt = cnt + 1
                if page_v2 == pages_v2 - 1:
                    break
                driver.find_element_by_xpath('//a[@class="paginationNext snowplow-navigation-nextpage-top"]').click()
            h_info.append(str(cnt-1))
            h_info.append(str(num_2015))
            h_info.append(str(num_2016))
            h_info.append(str(num_2017))
            h_info.append(str(num_2018))
            h_info.append(str(num_self_2018))
        href_infos.append(h_info)

    # 创建excel表
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 创建工作簿
    sheet = book.add_sheet(year, cell_overwrite_ok=True)
    # 手动在第一行写上表头
    sheet.write(0, 1, '文章标题')
    sheet.write(0, 2, '作者')
    sheet.write(0, 3, '刊物')
    sheet.write(0, 4, '页数')
    sheet.write(0, 5, '出版时间')
    sheet.write(0, 6, '引用数')
    sheet.write(0, 7, '检索到的引用数')
    sheet.write(0, 8, '2015')
    sheet.write(0, 9, '2016')
    sheet.write(0, 10, '2017')
    sheet.write(0, 11, '2018')
    sheet.write(0, 12, '2018(自)')
    # 将每篇论文的信息写入excel表格
    for i, info in enumerate(infos):
        for j, inf in enumerate(info):
            sheet.write(i+1, j, inf)
    # 将每篇论文的引用信息写入excel表格
    for i, info in enumerate(href_infos):
        for j, inf in enumerate(info):
            sheet.write(i+1, j+7, inf)
    # 保存.xls文件
    book.save('/home/icepoint/result.xls')
