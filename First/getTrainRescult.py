import datetime
import time

import xlwt
from prettytable import PrettyTable
import re  # 正则表达式模块
import urllib3, requests  # python 访问 HTTP 资源的必备库
import station
import xlsxwriter as xw


# 定义一个filtrate_train()函数，用来筛选查询到列车车次的数据
def filtrate_train(pt, data_list):
    temp_data = []
    station_train_code = data_list[3]  # 车次
    from_station_code = data_list[6]  # 起始站英文代号
    to_station_code = data_list[7]  # 终点站英文代号
    from_station_name = station.get_name(from_station_code)  # 起始站中文名称
    to_station_name = station.get_name(to_station_code)  # 终点站中文名称
    start_time = data_list[8]  # 出发时间
    arrive_time = data_list[9]  # 到达时间
    lishi = data_list[10]  # 历时
    # 通过对比12306代码和页面上座位显示结果分析出“商务座”和“特等座”对应的参数是不同的，cN[25]是特等座，cN[32]是商务座
    business_seat = data_list[25] or data_list[32] or "--"  # 商务座和特等座
    first_class_seat = data_list[31] or "--"  # 一等座
    second_class_seat = data_list[30] or "--"  # 二等座，查看12306页面时，二等座下方有个“二等包座”，对比代码应该是cN[27]，但是没有找到有对应数据暂时不写上去
    advanced_soft_sleeper = data_list[21] or "--"  # 高级软卧
    soft_sleeper = data_list[23] or "--"  # 软卧
    bullet_sleeper = data_list[33] or "--"  # 动卧
    hard_sleeper = data_list[28] or "--"  # 硬卧
    soft_seat = data_list[24] or "--"  # 软座，因为没有查询到有软座的信息，对比了代码参数，猜测cN[24]应该是软座
    hard_seat = data_list[29] or "--"  # 硬座
    not_seat = data_list[26] or "--"  # 无座

    temp_data.append(station_train_code)
    temp_data.append(from_station_name)
    temp_data.append(to_station_name)
    temp_data.append(start_time)
    temp_data.append(arrive_time)
    temp_data.append(lishi)

    temp_data.append(business_seat)
    temp_data.append(first_class_seat)
    temp_data.append(second_class_seat)
    temp_data.append(advanced_soft_sleeper)
    temp_data.append(soft_sleeper)
    temp_data.append(bullet_sleeper)
    temp_data.append(hard_sleeper)
    temp_data.append(soft_seat)
    temp_data.append(hard_seat)
    temp_data.append(not_seat)

    pt.add_row([
        station_train_code,  # 车次
        from_station_name,  # 起始站中文名称
        to_station_name,  # 终点站中文名称
        start_time,  # 出发时间
        arrive_time,  # 到达时间
        lishi,  # 历时
        business_seat,  # 商务座和特等座
        first_class_seat,  # 一等座
        second_class_seat,  # 二等座
        advanced_soft_sleeper,  # 高级软卧
        soft_sleeper,  # 软卧
        bullet_sleeper,  # 动卧
        hard_sleeper,  # 硬卧
        soft_seat,  # 软座
        hard_seat,  # 硬座
        not_seat  # 无座
    ])
    return pt, temp_data


# 得到爬虫后的数据
def cli(chushi, zhognzhi, date):
    from_stion = station.get_telecode(chushi)
    to_stion = station.get_telecode(zhognzhi)
    tempdatas = []
    # 构建 URL
    url = ("https://kyfw.12306.cn/otn/leftTicket/query?"
           "leftTicketDTO.train_date={}&"
           "leftTicketDTO.from_station={}&"
           "leftTicketDTO.to_station={}&"
           "purpose_codes=ADULT").format(date, from_stion, to_stion)
    headers = {
        # Cookie的值可以通过打开浏览器的开发者模式复制过来
        "Cookie": "_uab_collina=160395250285657341202147; JSESSIONID=7C56E896658518A4E5BF99889839D00C; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; BIGipServerotn=1725497610.50210.0000; RAIL_EXPIRATION=1604632917257; RAIL_DEVICEID=DeBrCMshZyD9JIK2yazJV4op0oxRXXKpeio_Y27U75ZkWKFwOd6Q_i2JRVBJeN3Q9qQ7ybyTw4Vv3ImAEwdTAAh8XLXL6WGn3irR65rZyYeWtvToLkq8oVAprmAw6OPgPnqI9a9ItALNr0kFjzDkncjjGPINbqfa; BIGipServerpassport=770179338.50215.0000; route=c5c62a339e7744272a54643b3be5bf64; _jc_save_fromDate=2020-11-02; _jc_save_toDate=2020-11-01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    }
    requests.packages.urllib3.disable_warnings()
    r = requests.get(url, headers=headers, verify=False)  # verify=False参数表示不进行证书验证
    raw_trains = r.json()['data']['result']
    # print(raw_trains)
    pt = PrettyTable()
    pt.field_names = '车次 起始站 终点站 出发时间 到达时间 历时 商务（特等）座 一等座 二等座 高级软卧 一等（软）卧 动卧 二等（硬）卧 软座 硬座 无座'.split()
    for raw_train in raw_trains:
        data_list = raw_train.split("|")

        if data_list[1] == "预订":  # 因为有停运列车，需判定该车次列车是否可以预约
            initial = data_list[3][0].lower()  # 获取车次代号，g:高铁，d:动车，t:特快，k:快速，z:直达
            pt, tempdata = filtrate_train(pt, data_list)
            tempdatas.append(tempdata)
    # print(pt)
    return tempdatas


# 时间判断
def JudegeTime(time1, time2):
    temp1 = time1.split(":")
    temp2 = time2.split(":")

    if int(temp2[0]) - int(temp1[0]) < 0:
        return False
    else:
        temp_time = int(temp2[0]) - int(temp1[0])
        if temp_time * 60 + int(temp2[1]) - int(temp1[1]) < 0:
            return False
    return True




if __name__ == "__main__":
    print(cli("厦门","上海","2022-12-20"))