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
# quote_data = '/CQMS系统/原材料检测台账/原材料检测台账-水泥.cpt'
# quote_data = 'CQMS%E7%B3%BB%E7%BB%9F%2F%E5%8E%9F%E6%9D%90%E6%96%99%E7%AE%A1%E7%90%86%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%E7%BB%9F%E8%AE%A1%5BERP%5D.cpt'
# quote_data = 'CQMS%E7%B3%BB%E7%BB%9F%2F%E5%8E%9F%E6%9D%90%E6%96%99%E7%AE%A1%E7%90%86%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%2F%E5%8E%9F%E6%9D%90%E6%96%99%E6%A3%80%E6%B5%8B%E9%A2%91%E6%AC%A1%E5%8F%B0%E8%B4%A6.cpt'
# quote_data = 'CQMS%E7%B3%BB%E7%BB%9F%2F%E5%8E%9F%E6%9D%90%E6%96%99%E7%AE%A1%E7%90%86%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%2F%E5%8F%96%E6%A0%B7%E9%A2%91%E6%AC%A1.frm'
# quote_data = "%257B%2522%25E5%25BC%2580%25E5%25A7%258B%25E6%2597%25A5%25E6%259C%259F%2522%253A%25222025-02-19%2522%252C%2522%25E6%2588%25AA%25E6%25AD%25A2%25E6%2597%25A5%25E6%259C%259F%2522%253A%25222025-03-21%2522%252C%2522LABEL%25E5%2585%25AC%25E5%258F%25B8_C%2522%253A%2522%25E6%2597%25A5%25E6%259C%259F%253A%2522%252C%2522LABEL%25E7%25AB%2599%25E7%2582%25B9%2522%253A%2522%25E7%25AB%2599%25E7%2582%25B9%253A%2522%252C%2522%25E7%25AB%2599%25E7%2582%25B9%2522%253A%255B%252217505%2522%252C%252219701%2522%252C%2522653380340%2522%252C%252200902%2522%252C%252200904%2522%252C%252201001%2522%252C%252201601%2522%252C%252202101%2522%252C%252202301%2522%252C%252202102%2522%252C%252202701%2522%252C%252201701%2522%252C%252201901%2522%252C%252201801%2522%252C%252202601%2522%252C%2522837700993%2522%252C%2522903536295%2522%252C%2522928096160%2522%252C%2522936572029%2522%252C%2522981359013%2522%252C%252203701%2522%252C%252204101%2522%252C%252204401%2522%252C%252204104%2522%252C%25222043068%2522%255D%252C%2522LABEL%25E6%259D%2590%25E6%2596%2599%25E7%25B1%25BB%25E5%2588%25AB%2522%253A%2522%25E7%25B1%25BB%25E5%2588%25AB%253A%2522%252C%2522%25E6%259D%2590%25E6%2596%2599%25E7%25B1%25BB%25E5%2588%25AB%2522%253A%2522%25E6%25B0%25B4%25E6%25B3%25A5'%252C'%25E7%25A0%2582%2522%257D"
# quote_data = '%252FCQMS%25E7%25B3%25BB%25E7%25BB%259F%252F%25E5%258E%259F%25E6%259D%2590%25E6%2596%2599%25E6%25A3%2580%25E6%25B5%258B%25E5%258F%25B0%25E8%25B4%25A6%252F%25E5%258E%259F%25E6%259D%2590%25E6%2596%2599%25E6%25A3%2580%25E6%25B5%258B%25E5%258F%25B0%25E8%25B4%25A6-%25E7%25B2%2589%25E7%2585%25A4%25E7%2581%25B0.cpt'
# quote_data = '%252FCQMS%25E7%25B3%25BB%25E7%25BB%259F%252F%25E5%258E%259F%25E6%259D%2590%25E6%2596%2599%25E6%25A3%2580%25E6%25B5%258B%25E5%258F%25B0%25E8%25B4%25A6%252F%25E5%258E%259F%25E6%259D%2590%25E6%2596%2599%25E6%25A3%2580%25E6%25B5%258B%25E5%258F%25B0%25E8%25B4%25A6-%25E6%25B0%25B4%25E6%25B3%25A5.cpt'
# quote_data = 'CQMS%E7%B3%BB%E7%BB%9F%2F%E5%8E%9F%E6%9D%90%E6%96%99%E6%A3%80%E6%B5%8B%E5%8F%B0%E8%B4%A6%2F%E5%8E%9F%E6%9D%90%E6%96%99%E6%A3%80%E6%B5%8B%E5%8F%B0%E8%B4%A6.frm'
# quote_data = '%257B%2522%25E5%25BC%2580%25E5%25A7%258B%25E6%2597%25A5%25E6%259C%259F%2522%253A%25222025-02-23%2522%252C%2522%25E6%2588%25AA%25E6%25AD%25A2%25E6%2597%25A5%25E6%259C%259F%2522%253A%25222025-03-25%2522%252C%2522%25E8%25A7%2584%25E6%25A0%25BC%2522%253A%252252.5%2522%252C%2522%25E5%2593%2581%25E7%2589%258C%2522%253A%2522%2520%25E4%25B8%25AD%25E8%2581%2594%2522%252C%2522LABEL%25E5%2585%25AC%25E5%258F%25B8_C%2522%253A%2522%25E6%2597%25A5%25E6%259C%259F%253A%2522%252C%2522%25E4%25BE%259B%25E5%25BA%2594%25E5%2595%2586%2522%253A%2522%25E4%25B8%25AD%25E5%25BB%25BA%25E8%25A5%25BF%25E9%2583%25A8%25E5%25BB%25BA%25E8%25AE%25BE%25E8%2582%25A1%25E4%25BB%25BD%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8%25E9%259B%2586%25E9%2587%2587%25E5%2588%2586%25E5%2585%25AC%25E5%258F%25B8%2522%252C%2522%25E6%258E%2592%25E5%25BA%258F%2522%253A%2522%25E6%258A%25BD%25E6%25A0%25B7%25E6%2597%25A5%25E6%259C%259F%2522%252C%2522%25E6%25A3%2580%25E9%25AA%258C%25E7%25BC%2596%25E5%258F%25B7%2522%253A%2522%2520%2520SN20230188%2522%252C%2522%25E7%25AB%2599%25E7%2582%25B9%2522%253A%255B%252217505%2522%252C%252219701%2522%252C%2522653380340%2522%252C%252200902%2522%252C%252200904%2522%252C%252201001%2522%252C%252201601%2522%252C%252202101%2522%252C%252202301%2522%252C%252202102%2522%252C%252202701%2522%252C%252201701%2522%252C%252201901%2522%252C%252201801%2522%252C%252202601%2522%252C%2522837700993%2522%252C%2522903536295%2522%252C%2522928096160%2522%252C%2522936572029%2522%252C%2522981359013%2522%252C%252203701%2522%252C%252204101%2522%252C%252204401%2522%252C%252204104%2522%252C%25222043068%2522%255D%252C%2522%25E5%2585%25AC%25E5%258F%25B8%2522%253A%2522%2522%252C%2522AA%2522%253A%25221%2522%257D'
# quote_data = '%7B%22%5B8d77%5D%5B59cb%5D%5B65e5%5D%5B671f%5D%22%3A%222020-01-01%22%2C%22%5B622a%5D%5B6b62%5D%5B65e5%5D%5B671f%5D%22%3A%222025-03-26%22%2C%22%5B4f9b%5D%5B5e94%5D%5B5546%5D%22%3A%22%5B5723%5D%5B96c4%5D%5B6c34%5D%5B6ce5%5D%5B5382%5D%22%2C%22%5B7ad9%5D%5B70b9%5D%22%3A%2200902%22%2C%22%5B89c4%5D%5B683c%5D%22%3A%22P.O42.5R%22%2C%22%5B54c1%5D%5B724c%5D%22%3A%22%5B5723%5D%5B96c4%5D%22%7D'


# quote_data = 'CQMS%E7%B3%BB%E7%BB%9F%2F%E9%85%8D%E5%90%88%E6%AF%94%E7%AE%A1%E7%90%86%2F%E9%85%8D%E5%90%88%E6%AF%94%E4%BD%BF%E7%94%A8%E5%8F%B0%E8%B4%A6%5B%E6%96%B0%E7%96%86%5D.cpt'
# quote_data = urllib.parse.unquote(quote_data)
# print(quote_data)
# quote_data = urllib.parse.unquote(quote_data)
# # quote_data = urllib.parse.quote('CQMS系统/原材料管理/原材料检测分析/原材料检测指标分析.frm', safe='')
# print(quote_data)

# quote_data = urllib.parse.quote(quote_data)
# print(quote_data)
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
#对json数据进行两次编码
# json_data = urllib.parse.quote(str(json_data))
# json_data = urllib.parse.quote(json_data)
# print(json_data)

#获取返回头set-cookie信息
# import requests
# from http.cookies import SimpleCookie
#
#
# # 创建会话以自动管理Cookie
# session = requests.Session()
# url = "https://fr.002302.com.cn/decision?username=TMR29YtnGPI=&callback=ng_jsonp_callback_0"
# response = session.get(url, allow_redirects=False)
#
# # 存储所有Set-Cookie头
# all_set_cookies = []
#
# # 跟踪重定向链
# while response.status_code in (301, 302, 303, 307, 308):
#     # 获取当前响应的所有Set-Cookie头
#     # set_cookies = response.raw.headers.getall("Set-Cookie", [])
#     set_cookies = response.raw.headers.get_all("Set-Cookie", [])
#     all_set_cookies.extend(set_cookies)
#
#     # 获取重定向目标
#     redirect_url = response.headers["Location"]
#     # 发送下一个请求（会话会自动携带已设置的Cookie）
#     response = session.get(redirect_url, allow_redirects=False)
#
# # 处理最终响应（非重定向状态码）
# if response.ok:
#     set_cookies = response.raw.headers.get_all("Set-Cookie", [])
#     all_set_cookies.extend(set_cookies)
#
# # 解析所有Set-Cookie头
# parsed_cookies = []
# for cookie_header in all_set_cookies:
#     cookie = SimpleCookie()
#     cookie.load(cookie_header)
#     # 提取键值对
#     for key, morsel in cookie.items():
#         parsed_cookies.append({key: morsel.value})
#
# print("所有Set-Cookie头:", all_set_cookies)
# print("解析后的Cookie键值对:", parsed_cookies)

# 将字符串转换为Unicode十六进制编码
# def str_to_unicode_hex(text):
#     encoded = []
#     for char in text:
#         hex_value = format(ord(char), '04x')  # 转为4位十六进制，不足补零
#         encoded.append(f'[{hex_value}]')
#     return ''.join(encoded)
#
# # 示例
# original_str = "F类二级"
# result = str_to_unicode_hex(original_str)
# print(result)  # 输出: [8d77][59cb][65e5][671f]

# now = datetime.now()
# print(int(now.timestamp()*1000))

# Python 解码示例
# key = "[914d][6bd4][7f16][53f7]"
# decoded_key = "".join([chr(int(code, 16)) for code in key.strip("[]").split("][")])
# print(decoded_key)  # 输出
print(datetime.now())
#输出当前日期
print(datetime.now().strftime("%Y-%m-%d"))
