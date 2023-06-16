from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from lxml import etree
import time,os


def HeadlessChromeDriver(x,headless = True,Proxy = None):
    

    chrome_options = Options()
    if(headless == True):
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')        #一些情况下使用headless GPU会有问题（我没遇到）
        chrome_options.add_argument('window-size=1920x1080')#页面部分内容是动态加载得时候，无头模式默认size为0x0，需要设置最大化窗口并设置windowssize，不然会出现显示不全的问题
        chrome_options.add_argument('--start-maximized')    #页面部分内容是动态加载得时候，无头模式默认size为0x0，需要设置最大化窗口并设置windowssize，不然会出现显示不全的问题
        chrome_options.add_argument('lang=zh_CN.UTF-8')
    if(Proxy != None):
        chrome_options.add_argument("--proxy-server=" + Proxy)
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
    #添加user-agent，避免被当作爬虫脚本
    driver = Chrome(  options=chrome_options)
    with open('stealth.min.js') as f:
        js = f.read()
 
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })#加载stealth.min.js 文件，该文件会修改http协议中得head信息，避免被从其他方面识别为爬虫脚本
 
    driver.get(x)    #加载机器人检测页面，可以从各项指标判断当前程序是否为机器人
    # 保存源代码为 html 再双击打开，查看机器人检测页面返回的完整结果
    html = driver.execute_script("return document.documentElement.outerHTML")
    # with open('result.html', 'w',encoding='utf-8') as f:
    #     f.write(html)
 
    return html


def run(x, T, TS, LS, LB, IS, IB,):
    

    # print(x, T, TS, LS, LB, IS, IB)
    
    html = HeadlessChromeDriver(x)
    html = etree.HTML(html)

    T = html.xpath(T)[0]
    # print(T)
    TS = html.xpath(TS)
    # print(TS)
    LS = html.xpath(LS)
    # print(LS)
    LB = LB
    # print(LB)
    IS = html.xpath(IS)
    # print(IS)
    IB = IB
    # print(IB)

    # print(T,TS,LS,LB,IS,IB)

    # exit()

    return T, TS, LS, LB, IS, IB


def pin(T, TS, LS, LB, IS, IB,SJ,n):
    with open('qc.txt', 'r', encoding='utf-8') as f:
        qc = f.read()
        qc = qc.rstrip("\n")
        qc = qc.split("\n")
        f.close()
    # print(qc)
    A = F'''<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
<channel>
<title>
<![CDATA[ {T} ]]>
</title>
<link></link>
<description>
</description>
'''
    C = '''</channel>
</rss>'''
    
    B = ""
    if os.path.exists(f"RSS/bilibili/{n}.XML"):
        with open(F'RSS/bilibili/{n}.XML', 'r', encoding='utf-8') as f:
            x = f.read()
            x = x.replace(F"{A}","\n")
            x = x.replace(F"{C}",'\n')
            f.close()
            B = B+x
    s = 0
    for x in TS:
        if LS[s] in qc:
            s += 1
            continue
        B += f"""
<item>
<title>
<![CDATA[ {x} ]]>
</title>
<description>
<![CDATA[ <img src="{IB}{IS[s]}" referrerpolicy="no-referrer"> ]]>
</description>
<link>{LB}{LS[s]}</link>
<pubDate>{SJ}</pubDate>
</item>

"""
        
        s += 1
        
        with open('qc.txt', 'w',encoding='utf-8') as f:
                    qcc = ""
                    for x in qc:
                        qcc = qcc+x+"\n"
                    for x in LS:
                        qcc = qcc+x+"\n"

                    f.write(qcc)
                    f.close()
    return A+B+C


with open('rss.txt', 'r', encoding='utf-8') as f:
    rss = f.read()
    rss = rss.split("\n")
    f.close()

def app():
    订阅地址 = []
    
    for x in rss:
        print(x)
        if "bilibili" in x:
                n = x.split("/")[3]
                print(n)
                T, TS, LS, LB, IS, IB = run(x=x,
                                            T='//*[@id="h-name"]/text()',
                                            TS='//*[@id="submit-video-list"]/ul[2]/li/a[2]/text()',
                                            LS='//*[@id="submit-video-list"]/ul[2]/li/a[2]/@href',
                                            LB="https:",
                                            IS='//*[@id="submit-video-list"]/ul[2]/li/a[1]//img/@src',
                                            IB="https:",)
                
                

                from time import strftime, localtime
                SJ = strftime('%Y-%m-%d %H:%M:%S',localtime())
                XML = pin(T, TS, LS, LB, IS, IB,SJ,n,)
                with open(f'RSS/bilibili/{n}.XML', 'w', encoding='utf-8') as f:
                    f.write(XML)
                    f.close()
                订阅xml = F'http://127.0.0.1:1222/RSS/bilibili/{n}.XML'
                订阅地址.append(订阅xml)
                print("\n")
                print(T)
                print(订阅xml)
                print("完成")
                print("\n")
                print("反反爬等待60秒")
                time.sleep(60)

    for x in 订阅地址:
        print("订阅地址")
        print(x)
    with open('dy.txt', 'w',encoding='utf-8') as f:
        xx = ""
        for x in 订阅地址:
            xx = xx+x+"\n"

        f.write(xx)
        f.close()

while 1:
    try:
        app()
    except:
        pass