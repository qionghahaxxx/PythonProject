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
# quote_data = 'CQMS%E7%B3%BB%E7%BB%9F%2F%E5%8E%9F%E6%9D%90%E6%96%99%E7%AE%A1%E7%90%86%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%E7%BB%9F%E8%AE%A1%5BERP%5D.cpt'
# quote_data = 'CQMS%E7%B3%BB%E7%BB%9F%2F%E5%8E%9F%E6%9D%90%E6%96%99%E7%AE%A1%E7%90%86%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%2F%E5%8E%9F%E6%9D%90%E6%96%99%E6%A3%80%E6%B5%8B%E9%A2%91%E6%AC%A1%E5%8F%B0%E8%B4%A6.cpt'
quote_data = "%257B%2522%25E5%25BC%2580%25E5%25A7%258B%25E6%2597%25A5%25E6%259C%259F%2522%253A%25222025-02-19%2522%252C%2522%25E6%2588%25AA%25E6%25AD%25A2%25E6%2597%25A5%25E6%259C%259F%2522%253A%25222025-03-21%2522%252C%2522LABEL%25E5%2585%25AC%25E5%258F%25B8_C%2522%253A%2522%25E6%2597%25A5%25E6%259C%259F%253A%2522%252C%2522LABEL%25E7%25AB%2599%25E7%2582%25B9%2522%253A%2522%25E7%25AB%2599%25E7%2582%25B9%253A%2522%252C%2522%25E7%25AB%2599%25E7%2582%25B9%2522%253A%255B%252217505%2522%252C%252219701%2522%252C%2522653380340%2522%252C%252200902%2522%252C%252200904%2522%252C%252201001%2522%252C%252201601%2522%252C%252202101%2522%252C%252202301%2522%252C%252202102%2522%252C%252202701%2522%252C%252201701%2522%252C%252201901%2522%252C%252201801%2522%252C%252202601%2522%252C%2522837700993%2522%252C%2522903536295%2522%252C%2522928096160%2522%252C%2522936572029%2522%252C%2522981359013%2522%252C%252203701%2522%252C%252204101%2522%252C%252204401%2522%252C%252204104%2522%252C%25222043068%2522%255D%252C%2522LABEL%25E6%259D%2590%25E6%2596%2599%25E7%25B1%25BB%25E5%2588%25AB%2522%253A%2522%25E7%25B1%25BB%25E5%2588%25AB%253A%2522%252C%2522%25E6%259D%2590%25E6%2596%2599%25E7%25B1%25BB%25E5%2588%25AB%2522%253A%2522%25E6%25B0%25B4%25E6%25B3%25A5'%252C'%25E7%25A0%2582%2522%257D"
quote_data = urllib.parse.unquote(quote_data)
quote_data = urllib.parse.unquote(quote_data)
print(quote_data)
#url解码
# quote_data = urllib.parse.quote(quote_data, safe='')
# print(quote_data)

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
