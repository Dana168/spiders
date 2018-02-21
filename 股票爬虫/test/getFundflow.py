# -*- coding: utf-8 -*-

import lxml
import lxml.etree
import requests

    # 抓取个股【资金流向（fundFlowUrl）页面的详细信息】：
    # 包括【单日汇总】——个股、涨跌幅、资金流入数量、资金流入率、主力资金流入（万）、散户资金流入（万）、主力参与度
    # 【区间统计】——个股、涨跌幅、资金流入数量、资金流入率、主力资金流入（万）、散户资金流入（万）、主力参与度
def getFundFlowInfo(fundFlowUrls):


    for each in fundFlowUrls:
        pagedata=requests.get(each).content.decode("utf-8")
        mytree=lxml.etree.HTML(pagedata)

        # 单日汇总
        name=mytree.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[1]/a/text()")
        changeRate=mytree.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[2]/text()")[0].strip()
        totalFundNum=mytree.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[3]/text()")[0].strip()
        flowRate=mytree.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[4]/text()")[0].strip()
        maniFundNum=mytree.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[5]/text()")[0].strip()
        retailFundNum=mytree.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[6]/text()")[0].strip()
        mainParticipationRate=mytree.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[7]/text()")[0].strip()
        print(name,changeRate,totalFundNum,flowRate,maniFundNum,retailFundNum,mainParticipationRate)

    return name,changeRate,totalFundNum,flowRate,maniFundNum,retailFundNum,mainParticipationRate



    '''
    #区间统计
    # 近5日
    changeRate5=mytree.xpath("//*[@class=\"border data-table _areaFunds\"]/tbody/tr//td[2]/text()")
    totalFundNum5=mytree.xpath("//*[@class=\"border data-table _areaFunds\"]/tbody/tr//td[3]/text()")
    maniFundNum5=mytree.xpath("//*[@class=\"border data-table _areaFunds\"]/tbody/tr//td[4]/text()")
    print(changeRate5,totalFundNum5,maniFundNum5,"___________")
    #近20日
    changeRate20=mytree.xpath("//*[@class=\"border data-table _areaFunds\"]/tbody/tr//td[5]/text()")
    totalFundNum20=mytree.xpath("//*[@class=\"border data-table _areaFunds\"]/tbody/tr//td[6]/text()")
    maniFundNum20=mytree.xpath("//*[@class=\"border data-table _areaFunds\"]/tbody/tr//td[7]/text()")
    print(changeRate20,totalFundNum20,maniFundNum20,"________________")
    #近60日
    changeRate60=mytree.xpath("//*[@class=\"border data-table _areaFunds\"]/tbody/tr//td[8]/text()")
    totalFundNum60=mytree.xpath("//*[@class=\"border data-table _areaFunds\"]/tbody/tr//td[9]/text()")
    maniFundNum60=mytree.xpath("//*[@class=\"border data-table _areaFunds\"]/tbody/tr//td[10]/text()")
    print(changeRate60,totalFundNum60,maniFundNum60,"______________________")
    '''



if __name__ == '__main__':

    stockNums=["002156","300676","002466","601989"]
    stockUrls=stockUrls(stockNums)
    fundFlowUrls=getFundFlowUrls(stockUrls)
    getFundFlowInfo(fundFlowUrls)