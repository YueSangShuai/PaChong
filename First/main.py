import xlwt
from getAirRescult import pachong
import getTrainRescult


chushi = "厦门"
mudi = "上海"
date = "2022-12-10"
traindatatime = "9:30"

datas = getTrainRescult.cli(chushi, mudi, date)
datas2=pachong(chushi,mudi,date)
workbook = xlwt.Workbook()
workbooksheet = workbook.add_sheet('火车')

workbooksheet2 = workbook.add_sheet('飞机')
title = '车次 起始站 终点站 出发时间 到达时间 历时 商务（特等）座 一等座 二等座 高级软卧 一等（软）卧 动卧 二等（硬）卧 软座 硬座 无座'.split()
title2='航空公司 航班号 机型 出发时间 出发机场 到达时间 到达机场 成人票 成人头等舱 儿童票 儿童头等舱'.split()

for i in range(len(title)):
    workbooksheet.write(0, i, title[i])

for i in range(len(title2)):
    workbooksheet2.write(0, i, title2[i])

count = 0
for data in datas:
    if getTrainRescult.JudegeTime(traindatatime, data[3]):
        count += 1
        for i in range(len(data)):
            workbooksheet.write(count, i, data[i])

count2=0
for data in datas2:
    count2 += 1
    for i in range(len(data)):
        workbooksheet2.write(count2, i, data[i])

workbook.save("temp.xls")