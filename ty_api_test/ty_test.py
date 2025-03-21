# import urllib.parse
# file_str = urllib.parse.quote('Template (5)_20250307110538434.csv')
# file_str2 = urllib.parse.unquote('%E6%B5%8B%E8%AF%95')
# file3 = urllib.parse.quote(file_str2)
# print(file_str)
# print(file_str2)
# print(file3)
import urllib.parse
import hashlib
# from datetime import timedelta
from datetime import datetime
import time
# time1 = '2025-03-07'
#新增time2,在time1基础上加一天

quote_data = 'CQMS%E7%B3%BB%E7%BB%9F%2F%E5%8E%9F%E6%9D%90%E6%96%99%E7%AE%A1%E7%90%86%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%2F%E5%8E%9F%E6%9D%90%E6%96%99%E6%A3%80%E6%B5%8B%E9%A2%91%E6%AC%A1%E5%8F%B0%E8%B4%A6.cpt'
quote_data = urllib.parse.unquote(quote_data)
# quote_data = urllib.parse.unquote(quote_data)
print(quote_data)
#url解码
quote_data = urllib.parse.quote(quote_data, safe='')
print(quote_data)

# time1 = datetime.now()
# print(time1)
# #当前时间转换成毫秒级时间戳
# time2 = int(time1.timestamp()*1000)
# print(time2)
# #当前时间转换成秒级时间戳
# time22 = int(time1.timestamp())
# print(time22)
# #时间戳转换成可读时间
# time3 = datetime.fromtimestamp(time2/1000)
# print(time3)
# time33 = datetime.fromtimestamp(time22)
# print(time33)
# #将毫秒级时间戳转换成秒级的可读时间
# time4 = datetime.fromtimestamp(int(time2/1000))
# print(time4)

# time4 = time.time()
# print(time4)
# #将时间转换成秒级时间戳
# time5 = int(time4)
# print(time5)

# json_data = {
#     "开始日期": "2025-02-18",
#     "截止日期": "2025-03-20",
#     "LABEL日期": "日期:",
#     "LABEL类别": "类别:",
#     "LABEL公司": "公司:",
#     "公司": "",
#     "类别": "",
#     "LABEL站点": "站点:",
#     "站点": ""
# }
# json_data = urllib.parse.quote(str(json_data))
# print(json_data)
