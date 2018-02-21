#coding:utf-8
import redis
import numpy as np
import matplotlib
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt #数据可视化
import matplotlib.animation as animation
import matplotlib.transforms as mtransforms
from matplotlib.transforms import offset_copy
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
matplotlib.rcParams["font.sans-serif"]=["simhei"] #配置字体
matplotlib.rcParams["font.family"]= "sans-serif"
# 从redis数据库读取数据
StockRedis = redis.Redis(host="127.0.0.1", port=6379, db=0)
stockNameList=StockRedis.lrange("stock:name2",0,-1)
totalNumList=StockRedis.lrange("stock:totalFundNum2",0,-1)
mainParticipationRateList=StockRedis.lrange("stock:mainParticipationRate2",0,-1)
mianFundNumList=StockRedis.lrange("stock:maniFundNum2",0,-1)
retailFundNumList=StockRedis.lrange("stock:retailFundNum2",0,-1)
flowRateList=StockRedis.lrange("stock:flowRate2",0,-1)

names=[]
total=[]
mainNum=[]
retailNum=[]
mianRates=[]
flowRates=[]
data=[]
for i in range(StockRedis.llen("stock:name2")):

    # 每个字段构建一个列表，方便画柱状图
    names.append(stockNameList[i].decode('utf-8','ignore'))
    total.append(eval(totalNumList[i].decode('utf-8','ignore').replace(",","")))
    mianRates.append(eval(mainParticipationRateList[i].decode('utf-8','ignore').replace("%","").replace("+","")))
    mainNum.append(eval(mianFundNumList[i].decode('utf-8','ignore').replace(",","")))
    retailNum.append(eval(retailFundNumList[i].decode('utf-8','ignore').replace(",","")))
    flowRates.append(eval(flowRateList[i].decode('utf-8','ignore').replace("%","").replace("+","")))


# print(names,total,mainNum,retailNum,mianRates,flowRates,data)

#归一化处理，为每支股票构造一个五维字典，方便作雷达图
def normalize(list):
    newlist=[]
    Max = max(list)
    Min = min(list)
    for i in range(len(list)):
        newitem=(list[i]-Min)/(Max-Min)
        newlist.append(newitem)
    return newlist
newtotal=normalize(total)
newmainNum=normalize(mainNum)
newretailNum=normalize(retailNum)
print(newtotal,newmainNum,newretailNum)
# print(data)
# 每支股票构造一个字典，并将所有字典放入一个列表

for i in range(len(names)):
    elemDict = {}
    key = names[i]
    value = [newtotal[i], newmainNum[i], newretailNum[i], mianRates[i], flowRates[i]]
    elemDict[key] = value
    data.append(elemDict)
print(data)



# 分布图
xs = newtotal
ys = flowRates

fig = plt.figure(figsize=(5, 10))
ax = plt.subplot(2, 1, 1)

# If we want the same offset for each text instance,
# we only need to make one transform.  To get the
# transform argument to offset_copy, we need to make the axes
# first; the subplot command above is one way to do this.
trans_offset = mtransforms.offset_copy(ax.transData, fig=fig,
                                       x=0.05, y=0.10, units='inches')

for x, y in zip(xs, ys):
    plt.plot((x,), (y,), 'ro')
    plt.text(x, y, '%d, %d' % (int(x), int(y)), transform=trans_offset)


ax = plt.subplot(2, 1, 2, projection='polar')

trans_offset = mtransforms.offset_copy(ax.transData, fig=fig,
                                       y=6, units='dots')

for x, y in zip(xs, ys):
    plt.polar((x,), (y,), 'ro')
    plt.text(x, y, '%d, %d' % (int(x), int(y)),
             transform=trans_offset,
             horizontalalignment='center',
             verticalalignment='bottom')

plt.show()

'''


# 分布图
xs = newtotal
ys = flowRates

fig = plt.figure(figsize=(5, 10))
ax = plt.subplot(2, 1, 1)

# If we want the same offset for each text instance,
# we only need to make one transform.  To get the
# transform argument to offset_copy, we need to make the axes
# first; the subplot command above is one way to do this.
trans_offset = mtransforms.offset_copy(ax.transData, fig=fig,
                                       x=0.05, y=0.10, units='inches')

for x, y in zip(xs, ys):
    plt.plot((x,), (y,), 'ro')
    plt.text(x, y, '%d, %d' % (int(x), int(y)), transform=trans_offset)


# offset_copy works for polar plots also.
ax = plt.subplot(2, 1, 2, projection='polar')

trans_offset = mtransforms.offset_copy(ax.transData, fig=fig,
                                       y=6, units='dots')

for x, y in zip(xs, ys):
    plt.polar((x,), (y,), 'ro')
    plt.text(x, y, '%d, %d' % (int(x), int(y)),
             transform=trans_offset,
             horizontalalignment='center',
             verticalalignment='bottom')

plt.show()


# 三维散点图
def randrange(n, vmin, vmax):
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n = 512

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    xs = newtotal
    ys = newmainNum
    zs = newretailNum
    ax.scatter(xs, ys, zs, c=c, marker=m)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()








# 波浪图
y = np.vstack([newtotal, newmainNum,newretailNum, mianRates])
labels = ["总资金流 ", "主力资金", "散户资金"]
fig, ax = plt.subplots()
ax.stackplot(names, newtotal,newmainNum,newretailNum, labels=labels)
ax.legend(loc=2)
plt.show()

fig, ax = plt.subplots()
ax.stackplot(names, y)
plt.show()

# 三维图
X = newtotal
Y = flowRates
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

fig = plt.figure()
ax = Axes3D(fig)
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.viridis)

plt.show()


# 柱状图
plt.bar(names,total,label="个股资金流动")
plt.legend()
plt.show()

# Fixing random state for reproducibility
#
matplotlib.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots()
ax.plot(names, mianRates, 'o')
ax.set_title('股票')
plt.show()

#散点图
fig, ax = plt.subplots()
ax.plot(mianRates, '-o', ms=20, lw=2, alpha=0.7, mfc='orange')
ax.grid()
# position bottom right
fig.text(0.95, 0.05, 'Property of MPL',
         fontsize=50, color='gray',
         ha='right', va='bottom', alpha=0.5)
plt.show()

#
fig, ax = plt.subplots()
line, = ax.plot(mianRates)
ax.set_ylim(-0.5, 1)
def update(data):
    line.set_ydata(mianRates)
    return line,
def data_gen():
    while True:
        yield mianRates
ani = animation.FuncAnimation(fig, update, data_gen, interval=100)
plt.show()

'''
