# 操作指南

申明：此爬虫基于selenium制作，仅供学习使用，如有违规操作那是你的事，和我无关



## 浏览器驱动

1.先去下载chrome浏览器的驱动，并找到chrome浏览器的位置，注意要绝对路径，当然可以相对路径，并填写在第200行中

```py
browserDriver = r''#填写chrome浏览器驱动位置
```

2.获取chrome浏览器保存本地用户数据的地方

先去chrome浏览器搜索chrome://version

在**个人资料路径**中找到用户数据的地址并复制![屏幕截图 2024-11-19 174129.png](屏幕截图 2024-11-19 174129.png)

注意：只用复制到 User Data 那

## 搜索框class Name

接下来打开pixiv去获取搜索框的class Name

对着搜索框右键，点击检查，即可看到class Name

![屏幕截图 2024-11-19 174432](C:\Users\julia\Desktop\屏幕截图 2024-11-19 174432.png)

在第215行填入

```py
searchContent = driver.find_element(By.CSS_SELECTOR,'')#去pixiv获取搜索框的className，并填写在  ''   内，注意要以 . 开头，且空格要用 . 代替，不能有空格，如'.button.active'
```



## 获取其他元素的class Name（如果有报错说没找到元素）

1.去找下一页按钮的className

在第229行填入

```py
next_button_selector = '.sc-d98f2c-0.sc-xhhh7v-2.cCkJiq.sc-xhhh7v-1-filterProps-Styled-Component.kKBslM'#注意可以去看看下一页的className是否相同，应该是一样的
```

2.去找查看全部的按钮className

在第77行填入

```py
elements = driver.find_elements(By.CSS_SELECTOR, ".sc-emr523-0.guczbC")#此处填写查看全部的按钮className
```

3.去找图片的className

在第82行填入

```py
oringalImages = driver.find_elements(By.CSS_SELECTOR, '.gtm-expand-full-size-illust')#图片的className
```

