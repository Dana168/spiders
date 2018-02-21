import redis
myredis=redis.Redis(host="10.36.132.18",password="",port=6379)
print(myredis.info())
start_urlslist = ['http://new.tudou.com/category/c_97.html?spm=a2h28.8514923.filter.5~5!2~A',
              "http://new.tudou.com/category/c_96.html?spm=a2h28.8514923.filter.5~5!3~A",
              "http://new.tudou.com/category/c_85.html?spm=a2h28.8514923.filter.5~5!4~A",
              "http://new.tudou.com/category/c_100.html?spm=a2h28.8514923.filter.5~5!5~A",
              "http://new.tudou.com/category/c_87.html?spm=a2h28.8514923.filter.5~5!6~A",
              "http://new.tudou.com/category/c_84.html?spm=a2h28.8514923.filter.5~5!7~A",
              "http://new.tudou.com/category/c_98.html?spm=a2h28.8514923.filter.5~5!8~A",
              "http://new.tudou.com/category/c_91.html?spm=a2h28.8514923.filter.5~5!9~A",
              ]
for url in start_urlslist:
    myredis.lpush("tudou_redis:start_urls",url)