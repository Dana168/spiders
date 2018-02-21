import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import gevent
import gevent.pool


def login(webDriver):
    # 登录
    name = webDriver.find_element_by_css_selector("#loginname")
    name.send_keys("xxxxxxxx")

    password = webDriver.find_element_by_css_selector(
        "#pl_login_form > div > div:nth-child(3) > div.info_list.password > div > input")
    password.send_keys("xxxxxxxx")

    loginBtn = webDriver.find_element_by_css_selector(
        "#pl_login_form > div > div:nth-child(3) > div.info_list.login_btn > a")
    loginBtn.send_keys(Keys.ENTER)

    # 点击进入个人主页
    webDriver.find_element_by_css_selector(
        "#v6_pl_rightmod_myinfo > div > div > div.WB_innerwrap > div > a.name.S_txt1").send_keys(Keys.ENTER)
    time.sleep(5)


def myInfor(webDriver):
    # html = webDriver.page_source
    try:
        # 获取个人信息
        name = webDriver.find_element_by_css_selector(
            "#Pl_Official_Headerv6__1 > div.PCD_header > div > div.shadow > div.pf_username > h1").text
        faceImgUrl = webDriver.find_element_by_css_selector(
            "#Pl_Official_Headerv6__1 > div.PCD_header > div > div.shadow > div.pf_photo > p > a > img").get_attribute(
            "src")
        # print(html)
        # content = webDriver.find_element_by_css_selector(".PCD_person_info").text   #Pl_Core_UserInfo__7 > div:nth-child(2) > div.WB_cardwrap.S_bg2 > div > div.verify_area.W_tog_hover.S_line2 > p.info > span
        signature = webDriver.find_element_by_css_selector(
            ".WB_cardwrap.S_bg2 > .PCD_person_info > div > p.info > span").text.strip()
        city = webDriver.find_element_by_css_selector(
            ".WB_cardwrap.S_bg2 > .PCD_person_info  > .WB_innerwrap > .m_wrap > .detail > ul > li:nth-child(1) > span:nth-child(2)").text.strip()
        school = webDriver.find_element_by_css_selector(
            ".WB_cardwrap.S_bg2 > .PCD_person_info  > .WB_innerwrap > .m_wrap > .detail > ul > li:nth-child(2) > span:nth-child(2) > a").text
        company = webDriver.find_element_by_css_selector(
            ".WB_cardwrap.S_bg2 > .PCD_person_info  > .WB_innerwrap > .m_wrap > .detail > ul > li:nth-child(3) > span:nth-child(2) > a").text
        brithday = webDriver.find_element_by_css_selector(
            ".WB_cardwrap.S_bg2 > .PCD_person_info  > .WB_innerwrap > .m_wrap > .detail > ul > li:nth-child(4) > span:nth-child(2)").text.strip()
        introduce = webDriver.find_element_by_css_selector(
            ".WB_cardwrap.S_bg2 > .PCD_person_info  > .WB_innerwrap > .m_wrap > .detail > ul > li:nth-child(5) > span:nth-child(2)").text.strip()
        print(name, faceImgUrl)
        print(signature)
        print(city)
        print(school)
        print(company)
        print(brithday)
        print(introduce)

        inforList.append(
            {"name": name, "content1": signature, "content2": city, "content3": school, "content4": company,
             "content5": brithday, "content6": introduce, "faceImgUrl": faceImgUrl})
        # print(content)
    except:
        pass


def fansInfor(webDriver,file):
    # html = webDriver.page_source
    tempDict = {}
    try:
        # 获取个人信息                                  # #Pl_Official_Headerv6__1 > div > div > div.shadow.S_shadow > div.pf_photo > p > img
        name = webDriver.find_element_by_css_selector("#Pl_Official_Headerv6__1 > div > div > div.shadow > div.pf_username > h1").text
        faceImgUrl = webDriver.find_element_by_css_selector("#Pl_Official_Headerv6__1 > div > div > div.shadow > div.pf_photo > p > img").get_attribute("src")
        print(name, faceImgUrl)

        tempDict = {"name": name, "faceImgUrl": faceImgUrl}
        contentStr =  name + "\n" + faceImgUrl + "\n"


        contents = webDriver.find_elements_by_css_selector(".PCD_person_info > .WB_innerwrap > .m_wrap > .detail > ul > li")
        print(len(contents))
        count = 0
        for c in contents:
            count += 1
            content = c.find_element_by_css_selector("span:nth-child(2)").text
            print(content)
            tempStr = "content" + str(count)
            tempDict={tempStr:content}
            contentStr += content + "\n"

        file.write(contentStr)
        file.flush()

        inforList.append(tempDict)


    except Exception as e:
        print(e)


def getAllMyFansUrl(webDriver):
    # 点击进入粉丝页
    webDriver.find_element_by_css_selector(
        ".PCD_counter > .WB_innerwrap > .tb_counter > tbody > tr > td:nth-child(2) > a ").send_keys(Keys.ENTER)
    time.sleep(5)

    # 获取页数总数
    # #Pl_Official_RelationFans__89 > div > div > div > div.follow_box > div.WB_cardpage.S_line1 > div > a:nth-child(9)
    # #Pl_Official_HisRelation__61 > div > div > div > div.follow_box > div.WB_cardpage.S_line1 > div > a:nth-child(9)
    # div.WB_cardwrap S_bg2:nth-child(2) > div.PCD_connectlist > div.follow_box > div.WB_cardpage S_line1 > div > a:nth-last-child(2)
    pageNum = webDriver.find_elements_by_class_name("page")[-2].text
    print(pageNum)

    count = 0
    # 获取所有粉丝页面的URL
    # for i in range(int(pageNum)):
    for i in range(1):
        newUrlList = webDriver.find_elements_by_css_selector("#Pl_Official_RelationFans__89 > div > div > div > div.follow_box > div.follow_inner > ul > li > dl > dd.mod_info.S_line1 > div.info_name.W_fb.W_f14 > a.S_txt1")

        for newUrl in newUrlList:
            count += 1
            url = newUrl.get_attribute("href")

            # if type(url)==type("a") and url not in allFansUrlList:

            if url not in allFansUrlList:
                allFansUrlList.append(url)

                print(count, url)

        try:

            # 翻页
            nextPage = webDriver.find_elements_by_class_name("page")[-1].send_keys(Keys.ENTER)
            time.sleep(1)


        except:
            pass


def getAllFansUrl(webDriver):
    try:
        # 点击进入粉丝页
        webDriver.find_element_by_css_selector(".PCD_counter > .WB_innerwrap > .tb_counter > tbody > tr > td:nth-child(2) > a ").send_keys(Keys.ENTER)
        time.sleep(5)

        # 获取页数总数
        # #Pl_Official_RelationFans__89 > div > div > div > div.follow_box > div.WB_cardpage.S_line1 > div > a:nth-child(9)
        # #Pl_Official_HisRelation__61 > div > div > div > div.follow_box > div.WB_cardpage.S_line1 > div > a:nth-child(9)
        # div.WB_cardwrap S_bg2:nth-child(2) > div.PCD_connectlist > div.follow_box > div.WB_cardpage S_line1 > div > a:nth-last-child(2)
        pageNum = webDriver.find_elements_by_class_name("page")[-2].text
        print(pageNum)

        count = 0

        # 获取所有粉丝页面的URL  # #Pl_Official_RelationFans__89 > div > div > div > div.follow_box > div.follow_inner > ul > li:nth-child(1) > dl > dd.mod_info.S_line1 > div.info_name.W_fb.W_f14 > a.S_txt1
        #                      #Pl_Official_HisRelation__61 > div > div > div > div.follow_box > div.follow_inner > ul > li:nth-child(1) > dl > dd.mod_info.S_line1 > div.info_name.W_fb.W_f14 > a.S_txt1
        #                      #Pl_Official_HisRelation__61 > div > div > div > div.follow_box > div.follow_inner > ul > li:nth-child(1) > dl > dd.mod_info.S_line1 > div.info_name.W_fb.W_f14 > a.S_txt1
        for i in range(len(pageNum)):
            newUrlList = webDriver.find_elements_by_css_selector("#Pl_Official_HisRelation__61 > div > div > div > div.follow_box > div.follow_inner > ul > li > dl > dd.mod_info.S_line1 > div.info_name.W_fb.W_f14 > a.S_txt1")

            for newUrl in newUrlList:
                count += 1
                url = newUrl.get_attribute("href")

                if type(url) == type("a") and url not in allFansUrlList:
                    allFansUrlList.append(url)

                    print(count, url)

            # try:
            #   webDriver.find_element_by_id("layer_15095981194591")
            #
            #   break
            #
            # except:
            # 翻页
            nextPage = webDriver.find_elements_by_class_name("page")[-1].send_keys(Keys.ENTER)
            # print(nextPage)
            time.sleep(3)
    except:
        pass


def BFS(url):
    # webDriver.maximize_window()
    file = open(r"./weiboSB.txt", "w", encoding="utf-8")
    # 无图形设置
    options = selenium.webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values": {"images": 2}}
    options.add_experimental_option("prefs", prefs)  # 不加载图片
    webDriver = selenium.webdriver.Chrome(chrome_options=options)

    webDriver.get(url)
    time.sleep(10)

    login(webDriver)
    myInfor(webDriver)

    getAllMyFansUrl(webDriver)

    for newUrl in allFansUrlList:
        webDriver.get(newUrl)
        time.sleep(5)
        fansInfor(webDriver,file)
        getAllFansUrl(webDriver)



    file.close()


    "Done!"


if __name__ == '__main__':
    allFansUrlList = []
    inforList = []
    url = r"http://weibo.com/"
    BFS(url)

