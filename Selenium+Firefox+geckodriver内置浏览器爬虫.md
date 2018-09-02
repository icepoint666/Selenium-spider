# Selenium+Firefox+geckodriver内置浏览器爬虫
> 反爬虫手段：网页数据并不再直接渲染，而是由前端异步获取，并且通过 JavaScript 的加密库生成动态的 token，同时加密库再进行混淆（比较重要的步骤的确有网站这样做，参见淘宝和微博的登陆流程）。对于混淆过的加密库，可以选择内置浏览器引擎的爬虫(关键词：PhantomJS，Selenium)，在浏览器引擎运行页面，直接获取了正确的结果。

## Selenium
Selenium这个Web的自动化测试工具，它可以根据我们的指令，让浏览器自动加载页面，获取需要的数据，甚至页面截屏，或者判断网站上某些动作是否发生。但Selenium 自己不带浏览器，不支持浏览器的功能，它需要与第三方浏览器结合在一起才能使用。

再来简单说一下Selenium中常用的一些使用方法。

声明浏览器对象

Selenium支持很多浏览器，比如说：Chrome、Firefox还有手机端的浏览器，以及无界面浏览器PhantomJS。

#### 安装
```shell
$ sudo pip3 install selenium
```

```python
from selenium import webdriver

driver = webdriver.Chrome()
driver = webdriver.PhantomJS()
driver = webdriver.Firefox()
```
访问页面
我们和requests方法一样，使用get()方法请求网页，传入URL参数。下面这个示例主要使用get()方法访问百度首页，并打印出源代码。运行后会发现，Chrome浏览器会弹出，并自动访问了百度页面，然后在编辑器的控制界面输出百度界面的源代码，随后关闭浏览器。
```python
from selenium import webdriver

driver = webdriver.Chrome()
url = 'www.baidu.com'
driver.get(url)
print(driver.page_source)
driver.close
```
这里如果不想看到弹出浏览器，可以使用Headless模式，也就是无界面模式，在新版Selenium不推荐使用PhantomJS时候，Chrome的无界面模式就可以很好胜任PhantomJS的工作了。不过只用Chrome59版本以上的才可以使用该模式。
```python
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
```
先创建一个ChromeOptions对象，然后添加headless对象，最后声明浏览器对象的时候传递这个对象，这样就启用了无界面模式，也就不会弹出浏览器了。

Firefox浏览器也是同理：
```python
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--headless')
driver = webdriver.Firefox(firefox_options=firefox_options)
```

## 配合Firefox浏览器之前需要装插件
#### selenium IDE插件
第一步：打开火狐浏览器，找到最右边的菜单，选择附加组件

第二步：打开附件组件，选择“获取附件组件”，在搜索框中搜索selenium IDE

第三步：找到selenium IDE添加到Firefox,进行安装；

第四步：安装过后，重新启动浏览器，在工具列表下就会出现Selenium IDE；

## geckodriver
Firefox浏览器驱动

geckodriver的下载链接：https://github.com/mozilla/geckodriver/releases

下载对应版本的可执行文件之后：

windows: 将Firefox路径添加到环境变量中（C:\Program Files (x86)\Mozilla Firefox;）；在终端输入Firefox.exe，浏览器自动启用，则环境配置成功！！！

Linux: 直接把可执行文件的路径放入环境变量$PATH路径下，或者把可执行文件放入/usr/bin目录下也可以

#### 完整代码见[](demo/selenium_demo.py)

https://zhuanlan.zhihu.com/p/38900589

https://www.cnblogs.com/glumer/p/6088258.html
