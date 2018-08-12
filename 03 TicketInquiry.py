'''
借助12306官网查询火车票
用法如：python "03 TicketInquiry.py" 杭州东 南京南 2018-09-01
'''
#实验楼里这个项目只有会员才能看，但是看了它的免费预览内容就基本知道接下去怎么写了。
from urllib.request import urlopen
import json
import prettytable as pt
import re
import argparse

#处理参数
parser = argparse.ArgumentParser()
parser.add_argument("from_station")
parser.add_argument("to_station")
parser.add_argument("date")
#实验楼里还有车型的选择，这里为了偷懒就不要了，即输出所有的车型。
args = parser.parse_args()
#我们默认输入都是正常的，即站点都是存在的，时期的格式是正确的。
from_station = args.from_station
to_station = args.to_station
date = args.date


#先取得站点的对应代码
stationcode = urlopen("https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9061")
stationcode = re.findall("([\u4e00-\u9fa5]+)\|([A-Z]+)", stationcode.read().decode("utf-8"))
stationcode = dict(stationcode)
#代码对应站点
codestation = {value: key for key, value in stationcode.items()}

url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date="     \
      + date + "&leftTicketDTO.from_station=" + stationcode[from_station]        \
      + "&leftTicketDTO.to_station=" + stationcode[to_station]                   \
      + "&purpose_codes=ADULT"

data = json.loads(urlopen(url).read())
result = data["data"]["result"]

#通过ANSI转移实现彩色输出。
#注意：在cmd中，有时转义字符中的"\0"会被输出成"□"而剩余字符原样输出。但在PowerShell中总是可以正常彩色输出的。
RED = "\033[1;31m"          #红色
GREEN = "\033[1;32m"        #绿色
YELLOW = "\033[1;33m"       #黄色
DEFAULT = "\033[1;0m"       #控制台默认颜色

table = pt.PrettyTable()

for index in range(len(result)):
    info = result[index].split("|")
    item = {}
    item["车次"] = YELLOW + info[3] + DEFAULT
    item["始发站"] = GREEN + codestation[info[6]] + DEFAULT
    item["终点站"] = RED + codestation[info[7]] + DEFAULT
    item["出发时间"] = GREEN + info[8] + DEFAULT
    item["到站时间"] = RED + info[9] + DEFAULT
    item["历时"] = info[10]
    item["商务座"] = info[32]
    item["一等座"] = info[31]
    item["二等座"] = info[30]
    item["高级软卧"] = info[21]
    item["软卧"] = info[23]
    item["动卧"] = info[27]
    item["硬卧"] = info[28]
    item["软座"] = info[24]
    item["硬座"] = info[29]
    item["无座"] = info[26]
    item["其他"] = info[22]
    for key, value in item.items():
        if value == "":             
            item[key] = "--"
    if index == 0:
        table.field_names = list(item.keys())
    table.add_row(list(item.values()))

print(table)
