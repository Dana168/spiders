import time
from selenium import webdriver
from urllib import request
from lxml import etree
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
def getpagedata(file,driver):
    pagesource=driver.page_source
    mytree=etree.HTML(pagesource)
    page=eval(mytree.xpath("//span[@class='span totalNum']/text()")[0])
    for i in range(page-1):
        pagesource = driver.page_source
        jobnamelist=mytree.xpath("//a[@class='position_link']//h3/text()")
        salarylist=mytree.xpath("//span[@class='money']/text()")
        experiencelistold=mytree.xpath("//div[@class='p_bot']/div[@class='li_b_l']/text()")
        companylist=mytree.xpath("//div[@class='company_name']/a/text()")
        newexperiencelist=[]
        for i in range(len(experiencelistold)):
            if experiencelistold[i]=="\n                        ":
                pass
            else:
                newexperiencelist.append(experiencelistold[i].replace("\n                    ","").replace(" ",""))
        for i in range(len(jobnamelist)):
            file.write(("工作名称："+jobnamelist[i]+" 工资："+salarylist[i]+" 要求经验："+newexperiencelist[i]+" 招聘公司："
                        +companylist[i]+"\r\n").encode("utf-8","ignore"))
            file.flush()
            getdata(salarylist[i])
        driver.find_element_by_class_name("pager_next ").click()
        time.sleep(1)
def getdata(salary):
    newsalary=salary.replace("k","").replace("K","").split("-")
    min=eval(newsalary[0])
    max=eval(newsalary[1])
    minlist.append(min)
    maxlist.append(max)
    pass
if __name__ == '__main__':

    kw=input("请输入城市名:")
    kw2=input("请输入岗位名称:")
    key=request.quote(kw)
    job=request.quote(kw2)
    url="https://www.lagou.com/jobs/list_"+job+"?px=default&city="+key
    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 处理无界面浏览器
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
    )
    driver=webdriver.PhantomJS(executable_path=r"./phantomjs-2.1.1-windows/bin/phantomjs.exe",desired_capabilities=dcap)
    driver.get(url)
    time.sleep(2)
    file=open("lagoujob-"+kw+kw2+".txt","wb")
    maxlist=[]
    minlist=[]
    maxcount=0
    mincount=0
    print("抓取数据中......")
    getpagedata(file,driver)
    print("计算数据中......")
    for i in range(len(maxlist)):
        maxcount+=maxlist[i]
        mincount+=minlist[i]
    maxavg=int(maxcount/len(maxlist))
    minavg=int(mincount/len(minlist))
    avg=(maxavg+minavg)/2
    file.write((kw+"的"+kw2+"岗位的职位总数为:"+str(len(minlist))+",最小平均工资为:"+str(minavg)+"k/月,"+"最大平均工资为:"+str(maxavg)+"k/月,"+"平均工资为:"+str(avg)+"k/月").encode("utf-8","ignore"))
    driver.close()
    file.close()
    print(kw,"的",kw2,"岗位的职位总数为:",len(minlist),",最小平均工资为:",minavg,"k/月,","最大平均工资为:",maxavg,"k/月,","平均工资为:",avg,"k/月")