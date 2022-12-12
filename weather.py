import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import re
import json
import pymongo

connetion = pymongo.MongoClient("mongodb://mongodbforserver:E9wBw9l9BTU1z82GLI26FJLVJK2VQTWs5C7QttBMQMPApALEZnY1q4kOwjf2U3ENs1X1JAbOiru0ACDbbcIdUg==@mongodbforserver.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@mongodbforserver@")#private connetion String
db = connetion["webdb"] #cosmos mongo db DB명
col = db["webdb_id"]    #collention명


location = input("지역을 입력하세요\n>>> ")
Finallocation = location + '날씨'

url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + Finallocation
hdr = {'User-Agent': ('mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.70 safari/537.36')}
req = requests.get(url, headers=hdr)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

print("[[[오늘의 날씨]]]")
temperature_text = soup.find("div", attrs={"class":"temperature_text"}).get_text().replace("현재 온도","").strip()
print(temperature_text)
summary = soup.find("p", attrs={"class":"summary"}).get_text()
print(summary)
summary_list = soup.find("dl", attrs={"class":"summary_list"})
desc1 = summary_list.find_all("dd")[0].get_text()
desc2 = summary_list.find_all("dd")[1].get_text()
desc3 = summary_list.find_all("dd")[2].get_text()
print("체감 온도: ",desc1)
print("습도: ",desc2)
print("바람(북풍): ",desc3)
today_chart_list = soup.find("ul", attrs={"class":"today_chart_list"})
dust1 = today_chart_list.find_all("li")[0].get_text().strip()
dust2 = today_chart_list.find_all("li")[1].get_text().strip()
sun1 = today_chart_list.find_all("li")[2].get_text().strip()
sun2 = today_chart_list.find_all("li")[3].get_text().strip()
print("미세먼지: ",dust1)
print("초미세먼지: ",dust2)
print("자외선: ",sun1)
print("일몰: ",sun2)
print("--------------------")
print("[[[주간예보(---%는 강수량---)]]]")
list_box_weekly_weather = soup.find("div", attrs={"class":"list_box _weekly_weather"})
date1 = list_box_weekly_weather.find_all("li")[0].get_text().strip()
date2 = list_box_weekly_weather.find_all("li")[1].get_text().strip()
date3 = list_box_weekly_weather.find_all("li")[2].get_text().strip()
date4 = list_box_weekly_weather.find_all("li")[3].get_text().strip()
date5 = list_box_weekly_weather.find_all("li")[4].get_text().strip()
date6 = list_box_weekly_weather.find_all("li")[5].get_text().strip()
date7 = list_box_weekly_weather.find_all("li")[6].get_text().strip()


week = {}
listdate = [date1, date2, date3, date4, date5, date6, date7]

for i in range(0, 6):
    print(listdate[i])
    i = listdate[i].split
date1 = date1.split()
date2 = date2.split()
date3 = date3.split()
date4 = date4.split()
date5 = date5.split()
date6 = date6.split()
date7 = date7.split()

lenlist = []
#길이 반환

lenlist.append(len(date1)), lenlist.append(len(date2)), lenlist.append(len(date3))
lenlist.append(len(date4)), lenlist.append(len(date5)), lenlist.append(len(date6))
lenlist.append(len(date7))

listdata = [1, 6, 8]
listre = []
LEN = 9

for i in listdata:
    if (i > 1):
        listre.append(re.findall("-?\d+", date1[i + (lenlist[0] - LEN)])) #숫자만 추출
        listre.append(re.findall("-?\d+", date2[i + (lenlist[1] - LEN)]))
        listre.append(re.findall("-?\d+", date3[i + (lenlist[2] - LEN)]))
        listre.append(re.findall("-?\d+", date4[i + (lenlist[3] - LEN)]))
        listre.append(re.findall("-?\d+", date5[i + (lenlist[4] - LEN)]))
        listre.append(re.findall("-?\d+", date6[i + (lenlist[5] - LEN)]))
        listre.append(re.findall("-?\d+", date7[i + (lenlist[6] - LEN)]))
        listre.append(re.findall("-?\d+", date1[i+4])) #숫자만 추출
        listre.append(re.findall("-?\d+", date2[i]))
        listre.append(re.findall("-?\d+", date3[i]))
        listre.append(re.findall("-?\d+", date4[i]))
        listre.append(re.findall("-?\d+", date5[i]))
        listre.append(re.findall("-?\d+", date6[i]))
        listre.append(re.findall("-?\d+", date7[i]))
        listre = sum(listre,[]) #1차원 변환
        listre = list(map(int, listre)) #int형 변환
    else :
        listre.append(date1[i])
        listre.append(date2[i])
        listre.append(date3[i])
        listre.append(date4[i])
        listre.append(date5[i])
        listre.append(date6[i])
        listre.append(date7[i])
    if (i == 1):    #dict형 변환
         week['date'] = listre
    elif (i == 6):
        week['mintemp'] = listre
    else :
        week['maxtemp'] = listre
    listre = []

print(week)
plt.plot('date', 'mintemp', data=week)   #그래프 그리기(날짜, 최저기온, 최고기온)
plt.plot('date', 'maxtemp', data=week)
plt.show()

with open('week.json', 'w') as f :  #json 변환
	json.dump(week, f, indent=3)

data = col.insert_one(week) #cosmos db에 파일 저장