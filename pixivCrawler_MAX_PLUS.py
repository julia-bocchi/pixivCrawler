from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import requests
from requests.exceptions import ChunkedEncodingError, ConnectionError
import re
import pyautogui
import time
from selenium.common.exceptions import WebDriverException, NoSuchElementException, NoSuchWindowException


#配置浏览器驱动
def openUrl(arguments=[], browserDriver=None, url=None):
    try:
        chrome_options = webdriver.ChromeOptions()  # 配置和定制 Chrome 浏览器
        chrome_options.add_argument("--disable-gpu")  # 禁用gpu
        # chrome_options.add_argument('--headless')#无头模式
        # 其他配置和定制
        for arg in arguments:
            chrome_options.add_argument(arg)
        # 若没有提供 ChromeDriver 的路径，就使用 webdriver.Chrome() 自带的 ChromeDriver
        services = Service(executable_path=browserDriver)
        driver = webdriver.Chrome(service=services, options=chrome_options)
        # 返回webdriver对象
        if url:
            driver.get(url)  # 直接打开URL，不返回结果
        return driver
    except WebDriverException as e:
        print(f"WebDriverException: {e}")
        return None



#滚动页面
def Scroll_tobottom(driver = None):
    last_height = driver.execute_script("return document.body.scrollHeight")#循环滚动，直到到达页面底部为止
    while True:
        time.sleep(2)
        #滚动到页面底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")#等待一段时间，让页面有机会加载新内容
        driver.implicitly_wait(3)#等待最多3秒
        #计算新的页面高度
        new_height= driver.execute_script("return document.body.scrollHeight")#如果页面高度没有变化，说明没有加载新内容，退出循环
        if new_height == last_height:
            break
        # 更新页面高度
        last_height= new_height

#获取图片
def get_imgElement(driver=None, mode=0, path=None):
    # 检查传参是否正确
    if driver is None or mode == 0 or path is None:
        print("driver is None or mode == 0 or path is wrong ")
        return
    try:
        # 获取每个图片元素
        imgElements = driver.find_elements(By.TAG_NAME, 'li')
        
        # 要根据实际去修改遍历开始的位置，如下作者的话要从2~5索引开始，通过搜索下的话要从5开始
        for imgElement in imgElements[4:]:
            
            # 获取图片详情页的链接并跳转到图片详情页
            match = re.search(r'href="(.*?)"', imgElement.get_attribute('outerHTML'))
            if match:
                url = 'https://www.pixiv.net' + match.group(1)
                print("href:", url)
                driver.execute_script(f'window.open("{url}")')
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(1)
                driver.implicitly_wait(5)
                
                # 尝试点击按钮并获取图片
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, ".sc-emr523-0.guczbC")#此处填写查看全部的按钮className
                    if elements:
                        btn = elements[0]
                        btn.click()
                        time.sleep(1)
                        oringalImages = driver.find_elements(By.CSS_SELECTOR, '.gtm-expand-full-size-illust')#图片的className
                        print(f'{len(oringalImages)} 张原图')
                        for i in oringalImages:
                            # 获取图片id和格式，href里存放的是原图片的链接
                            match_title = re.search(r'([^\/]+)$', i.get_attribute('href'))
                            title = match_title.group(1)
                            print(title)
                            print(fr'{path}\{title}')
                            # 根据mode决定保存方式
                            if mode == 1:
                                download_image1(driver, i, path, title)
                            elif mode == 2:
                                print(fr'{path}\{title}')
                                download_image2(i.get_attribute('href'), fr'{path}\{title}')
                        # 关闭页面并回到主页面
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(3)
                    else:
                        # 如果找不到按钮（按钮返回的是空列表时），直接尝试获取原图链接
                        oringalImage = driver.find_element(By.CSS_SELECTOR, '[role="presentation"]')#图片的属性选择
                        print(f'1 张原图')
                        # 获取图片链接
                        match_url = re.search(r'href="(.*?)"', oringalImage.get_attribute('outerHTML'))
                        if match_url:
                            image_url = match_url.group(1)
                            # 获取图片id和格式
                            match_title = re.search(r'([^\/]+)$', image_url)
                            title = match_title.group(1)
                            print(f'{title}正在下载')
                            # 根据mode决定保存方式
                            if mode == 1:
                                download_image1(driver, oringalImage, path, title)
                            elif mode == 2:
                                print(fr'{path}\{title}')
                                download_image2(image_url, fr'{path}\{title}')
                        # 关闭页面
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(3)
                except NoSuchElementException:
                    # 如果找不到元素，直接尝试获取原图链接
                    oringalImage = driver.find_element(By.CSS_SELECTOR, '[role="presentation"]')#图片的className
                    print(f'1 张原图')
                    # 获取图片链接
                    match_url = re.search(r'href="(.*?)"', oringalImage.get_attribute('outerHTML'))
                    if match_url:
                        image_url = match_url.group(1)
                        # 获取图片id和格式
                        match_title = re.search(r'([^\/]+)$', image_url)
                        title = match_title.group(1)
                        print(f'{title}正在下载')
                        # 根据mode决定保存方式
                        if mode == 1:
                            download_image1(driver, oringalImage, path, title)
                        elif mode == 2:
                            print(fr'{path}\{title}')
                            download_image2(image_url, fr'{path}\{title}')
                    # 关闭页面
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(3)
                except Exception as e:
                    #如果打开页面什么都找不到就直接关闭页面
                    print(f"处理图片时发生错误：{e}")
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(3)
            else:
                # 如果没有找到图片详情页的链接，直接跳过
                print("未找到 href")
                continue
    except Exception as e:
        print(f"获取图片元素时发生错误：{e}")


#使用pyautogui保存
def download_image1(driver = None,element = None,path = None,title = None):
    if driver is None or element is None:
        raise ValueError("driver 和 element 参数不能为 None")
    # 右键另为存
    elementAction = ActionChains(driver).move_to_element(element)
    elementAction.context_click(element)
    elementAction.perform()
    pyautogui.typewrite(['v'])
    time.sleep(1)
    # 输入保存路径
    pyautogui.write(fr'{path}\{title}',interval=0.1)
    pyautogui.press('enter')
    time.sleep(1)


# 使用requests保存，可在后台运行(ai加的处理错误真的牛)
def download_image2(image_url, save_path,  retries=3, timeout=10):
    headers = {
    'referer': "https://www.pixiv.net/",  # 携带referer是因为p站的插画链接都是防盗链
    "user-agent": '',  # 自行填入请求头信息
    "cookie":  '' # 自行去获取cookies
    }
    for attempt in range(retries):
        try:
            response = requests.get(image_url, headers=headers, timeout=timeout)
            response.raise_for_status()  # 如果响应状态码不是200，将引发HTTPError
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print("Download complete")
            break  # 如果下载成功，跳出循环
        except (ChunkedEncodingError, ConnectionError, requests.HTTPError) as e:
            print(f"下载失败，正在尝试第 {attempt + 1} 次重试...")
            if attempt == retries - 1:
                print(f"尝试了 {retries} 次后仍然失败，放弃下载。")
    time.sleep(1)   



if __name__ == '__main__':
    # 谷歌浏览器的用户信息位置和驱动位置
    option = [r'--user-data-dir=']#在  --user-data-dir=   后填写chrome浏览器用户数据的位置，用于跳过登录
    browserDriver = r''#填写chrome浏览器驱动位置
    
    # 输入搜索内容和执行方式
    mode = int(input("输入你想要的执行方式（输入1为使用pyautogui保存，2为使用requests保存，可在后台运行）"))
    path = input("输入保存路径：")
    way = int(input('你想要怎么爬取（输入0为输入关键词来爬取，输入1为输入作者id来爬取作者的全部作品）'))
    
    if way == 0:
        # 打开浏览器并跳转到 Pixiv
        driver = openUrl(option, browserDriver, 'https://www.pixiv.net/')
    
        driver.implicitly_wait(30)  # 设置隐式等待
    
        # 找到搜索框并输入关键词
        content = input('请输入想要搜索的内容：')
        searchContent = driver.find_element(By.CSS_SELECTOR,'')#去pixiv获取搜索框的className，并填写在  ''   内，注意要以 . 开头，且空格要用 . 代替，不能有空格，如'.button.active'
        searchContent.send_keys(f'{content}\n')
    
    elif way == 1:
        authorId = input('请输入作者id：')
        # 打开浏览器并跳转到 Pixiv
        driver = openUrl(option, browserDriver, f'https://www.pixiv.net/users/{authorId}/artworks')
        
    if driver is not None:
        try:
            driver.implicitly_wait(30)  # 设置隐式等待
            
            # 使用显式等待来等待下一页按钮出现
            wait = WebDriverWait(driver, 10)
            next_button_selector = '.sc-d98f2c-0.sc-xhhh7v-2.cCkJiq.sc-xhhh7v-1-filterProps-Styled-Component.kKBslM'#注意可以去看看下一页的className是否相同，应该是一样的
            while True:
                #滚动页面
                Scroll_tobottom(driver=driver)
                
                # 下载本页图片
                get_imgElement(driver=driver, mode=mode, path=path)
                
                # 等待下一页按钮出现或直到超时
                next_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, next_button_selector)))
                if len(next_buttons) > 1:
                    nextButton = next_buttons[1]
                    isnext = nextButton.get_attribute('outerHTML')
                    if 'hidden' in isnext:
                        print("没有更多图片了")
                        break
                    else:
                        nextButton.click()
                        time.sleep(5)
                else:
                    print("没有找到下一页按钮")
                    break
        except WebDriverException as e:
            print(f"发生错误：{e}")
        finally:
            driver.quit()
    else:
        print("浏览器打开失败")
        
