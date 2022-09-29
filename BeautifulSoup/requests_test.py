import requests

res=requests.get("http://www.chinaunicom.com.cn/api/article/NewsByIndex/2/2022/08/news")
print(res)
print(requests.json())