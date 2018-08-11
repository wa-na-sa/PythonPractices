#借助12306官网查询火车票
#实验楼里这个项目只有会员才能看，但是看了它的免费预览内容就基本知道接下去怎么写了
from urllib.request import urlopen
import json
import prettytable as pt
url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-08-20&leftTicketDTO.from_station=SHH&leftTicketDTO.to_station=BJP&purpose_codes=ADULT"
data = json.loads(urlopen(url).read())
result = data["data"]["result"]
n = len(result)#总数

#通过ANSI转移实现彩色输出
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
DEFAULT = "\033[1;0m"

table = pt.PrettyTable()
info_list = []
for index in range(n):
    info = result[index].split("|")
    item = {}
    item["车次"] = YELLOW + info[3] + DEFAULT
    item["始发站"] = GREEN + info[6] + DEFAULT
    item["终点站"] = RED + info[7] + DEFAULT
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
