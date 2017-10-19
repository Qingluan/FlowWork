

### 自动化脚本库

## 环境

### 系统环境

> Mac 测试没问题
> Linux 应该也没问题
> Windows 无力拯救，自求多福

### Python环境

> python3 (3.5以上最好)
> chrome, firefox [如果不做推特相关的话，这条忽略]

## Install

> cd FlowWork 
> pip3 install mroylib-min
> pip3 install .
> 
> > #安装对应的chromedriver 
> > cd WebDriverExecutor/
> > unzip chromedriver_{version}.zip && cp chromedriver_{version} /usr/local/bin/
> > 


## Usage DOc

### easy use

> 这个库本身包含了一些浏览器的模拟操作，并且没种操作有好几个模式。可以读取一个批量流程命令
> 
> #examp

```py
In [1]: from FlowWork.Net.flownet import  FLowNet

In [3]: FLowNet?
#Init signature: FLowNet(url=None, proxy=False, load_img=False, driver=None, #random_agent=False, agent=None, **options)
#Type:           type
# proxy 可以不用这里需要翻墙所以加上
# driver 驱动设置，为空时自动使用 phantomjs [不会弹窗]
# load_img 每个网页是否加载图片，(只对phantomjs 有效)

In [4]: f = FLowNet(proxy='socks5://127.0.0.1:1080', driver='chrome') 

# 加载流程脚本
In [5]: f.flow_doc("tw/test2")
In [5]: f.flow('loc', 'ac', 1) # 或者自己输入命令

# 没读取一行会自动截图的也可以手动截图

```


## 命令
### 指令

> 主要行为分为以下几种

1. go
2. click
3. send_keys
4. clear
5. scroll

### 结构

##### css_loc/ac[options/keys] #结构

```js
//普通的点击，左边的为css定位
.btn/C

//带有多模式检查的点击，多用于js复杂渲染的按钮
span.monit-btn/C[check]

// 输入字符
// 如果结尾带R则自动加上换行不带为普通输入
input.text/I'hello world'
input.text/I'hello world'R

// 下滑
// 截图
//自动下拉一页高度并截图
->/S 
//当前位置截图
-/S
//
```

### 流程控制

```js
// [int]决定最多重复的次数
for::[int]::loc/actions  
...
endfor

//测试是否有这个loc显示
if::[loc] 
...
enfif
```

### 可嵌入变量

```py
#如果flow脚本: test.fl 如下

for::2::input.user/I'{username}'
input.user/I'{passwd}'R
... other action
endfor


~ f.flow_doc("test.fl", username='./user.txt', passwd='./passwd.txt')
~ #会根据 读取次数自动填装文本到 flow脚本中


# username.txt如下
user1
user2

# passwd.txt 如下
passwd1
passwd2
```