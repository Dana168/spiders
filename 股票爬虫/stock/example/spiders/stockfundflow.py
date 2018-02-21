from scrapy_redis.spiders import RedisSpider
import example.items

class StockSpider(RedisSpider):

    name = 'stockfundflow'
    redis_key = 'stock:fundFlowUrl2'

    def __init__(self, *args, **kwargs):

        domain = kwargs.pop('https://gupiao.baidu.com/stock/', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(StockSpider, self).__init__(*args, **kwargs)


    def parse(self,response):
        # 抓取个股【资金流向（fundFlowUrl）页面的详细信息】：
        # 包括【单日汇总】——个股、涨跌幅、资金流入数量、资金流入率、主力资金流入（万）、散户资金流入（万）、主力参与度
        # 【区间统计】——个股、涨跌幅、资金流入数量、资金流入率、主力资金流入（万）、散户资金流入（万）、主力参与度
        # 单日汇总
        self.names = response.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[1]/a/text()").extract()
        self.changeRates = response.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[2]/text()").extract()
        self.totalFundNums = response.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[3]/text()").extract()
        self.flowRates = response.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[4]/text()").extract()
        self.maniFundNums = response.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[5]/text()").extract()
        self.retailFundNums = response.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[6]/text()").extract()
        self.mainParticipationRates = response.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[7]/text()").extract()
        stockitem = example.items.StockItem()
        stockitem["name"]=self.names[0].strip()
        stockitem["changeRate"]=self.changeRates[0].strip()
        stockitem["totalFundNum"]=self.totalFundNums[0].strip()
        stockitem["flowRate"]=self.flowRates[0].strip()
        stockitem["maniFundNum"]=self.maniFundNums[0].strip()
        stockitem["retailFundNum"]=self.retailFundNums[0].strip()
        stockitem["mainParticipationRate"]=self.mainParticipationRates[0].strip()
        print(self.names,self.changeRates,self.totalFundNums,self.flowRates,self.maniFundNums,self.retailFundNums,self.mainParticipationRates)
        yield stockitem



