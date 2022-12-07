# coding=utf-8
import requests
from fake_useragent import UserAgent
import json


city = {'深圳': 'SZX', '无锡': 'WUX','厦门':'XMN','上海':'SHA'}  ##定义一个存放城市和对应三字码的字典，这里就随便写两个城市
url = 'https://flights.ctrip.com/itinerary/api/12808/products'
headers = {
    'User-Agent': UserAgent().chrome,
    "Content-Type": "application/json"}


def pachong(dcity, acity, date):
    request_payload = {"flightWay": "Oneway",
                       "army": "false",
                       "classType": "ALL",
                       "hasChild": 'false',
                       "hasBaby": 'false',
                       "searchIndex": 1,
                       "portingToken": "3fec6a5a249a44faba1f245e61e2af88",
                       "airportParams": [
                           {"dcity": city.get(dcity),
                            "acity": city.get(acity),
                            "dcityname": dcity,
                            "acityname": acity,
                            "date": date}]}  ##这里是需要传入的参数
    response = requests.post(url, headers=headers, data=json.dumps(request_payload))  # 发送post请求
    data = json.loads(response.text)['data']
    datalist = data.get("routeList")  ##得到存放所有航班信息的列表

    save_datas=[]
    for num in range(len(datalist)):  ##遍历所有航班
        save_data=[]
        flight = datalist[num].get("legs")[0].get("flight")  ##找到航班信息

        airlineNames = flight.get("airlineName")  # 航空公司
        flight_no = flight.get("flightNumber")  ##航班号
        plane_type = flight.get("craftTypeName")  ##机型
        departuredate = flight.get("departureDate")  ##出发时间
        arrivalName = flight.get("departureAirportInfo").get("airportName")  ##出发机场

        arrivaldate = flight.get("arrivalDate")  ##到达时间
        departure=flight.get("arrivalAirportInfo").get("airportName")##到达机场

        price=datalist[num].get("legs")[0].get("characteristic")

        adultprice=price.get("lowestPrice") ##成人票
        adultcfprice=price.get('lowestCfPrice')#成人头等舱
        childprice=price.get('lowestChildPrice')#儿童票
        childcfprice=price.get('lowestChildCfPrice')

        save_data.append(airlineNames)
        save_data.append(flight_no)
        save_data.append(plane_type)
        save_data.append(departuredate)
        save_data.append(arrivalName)
        save_data.append(arrivaldate)
        save_data.append(departure)
        save_data.append(adultprice)
        save_data.append(adultcfprice)
        save_data.append(childprice)
        save_data.append(childcfprice)

        save_datas.append(save_data)

    return save_datas

if __name__ == '__main__':
    pachong('厦门', '上海', '2022-12-22')
