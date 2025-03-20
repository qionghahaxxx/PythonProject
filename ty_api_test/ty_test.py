# import urllib.parse
# file_str = urllib.parse.quote('Template (5)_20250307110538434.csv')
# file_str2 = urllib.parse.unquote('%E6%B5%8B%E8%AF%95')
# file3 = urllib.parse.quote(file_str2)
# print(file_str)
# print(file_str2)
# print(file3)
# import urllib.parse
import hashlib
# from datetime import timedelta

# time1 = '2025-03-07'
#新增time2,在time1基础上加一天
password = 'Aa123456@123456'
password = hashlib.md5(password.encode()).hexdigest() #md5加密
print(password)


