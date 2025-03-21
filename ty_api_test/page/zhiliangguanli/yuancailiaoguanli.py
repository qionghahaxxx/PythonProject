
import urllib.parse

from ty_api_test.common.logger import *
# from ty_api_test.page.portal_login_api import login
from ty_api_test.common.readconfig import *
from ty_api_test.common.readapi import *
import requests
from datetime import datetime

class YcLgLi:
    """原材料管理模块相关api方法封装"""
    def __init__(self):
        self.host = Readconfig('HOST-FR').host
    def yc_tz_search(self,start_date='',end_date='',company='', category='', site=''):
        """原材料取样台账-可以按日期、公司、分类、站点查询"""
        # 1.访问帆软链接，获取sessionID
        api = Api('api')['帆软链接']
        host = self.host
        # viewlet = urllib.parse.quote('CQMS系统/原材料管理/原材料取样/原材料检测频次台账.cpt', safe='') #safe='',强制编码所有非安全字符，即"/"也编码掉
        api = "?".join([api,
                        'viewlet=CQMS%E7%B3%BB%E7%BB%9F%2F%E5%8E%9F%E6%9D%90%E6%96%99%E7%AE%A1%E7%90%86%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%2F%E5%8E%9F%E6%9D%90%E6%96%99%E6%A3%80%E6%B5%8B%E9%A2%91%E6%AC%A1%E5%8F%B0%E8%B4%A6.cpt'])
        headers = {
            "Cookie": "fineMarkId=38e5f95408bb300c88f21eead0aa1a0b; fine_auth_token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjYW9tZW5nIiwidGVuYW50SWQiOiJkZWZhdWx0IiwiaXNzIjoiZmFucnVhbiIsImRlc2NyaXB0aW9uIjoiWzY2ZjldWzViNWZdKGNhb21lbmcpIiwiZXhwIjoxNzQzMzIyMDc2LCJpYXQiOjE3NDI0NTgwNzYsImp0aSI6ImFHRlVmdFduQVdpbHhPWDFnUUJXYmtIdVdVVkZaQTZPSXVtN0pnblNDQUFDMk5WRCJ9.ZZh5Cs5nRzWHss_1D1BmAJsEqI5k11qXvnW9E6JZOgI; fine_remember_login=-1"
        }
        url = f"https://{host}{api}"
        # print(url)
        response = requests.get(url, headers=headers)
        session_id_data = response.headers.get('Set-Cookie')
        session_id_list = session_id_data.split(';')
        # print(session_id_list)
        session_id = session_id_list[0].split('=')
        # print(response.headers)
        # print(session_id)
        #2.原材料取样台账查询
        api1 = Api('api')['原材料取样查询']
        time1 = datetime.now()
        timestamp1 = int(time1.timestamp() * 1000)
        api2 = '?'.join([api1, f'_={timestamp1}'])
        host = Readconfig('HOST-FR').host
        url1 = f"https://{host}{api2}"
        # print(url1)
        headers1 = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sessionID": session_id[1],
            "Cookie": f'fine_auth_token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjYW9tZW5nIiwidGVuYW50SWQiOiJkZWZhdWx0IiwiaXNzIjoiZmFucnVhbiIsImRlc2NyaXB0aW9uIjoiWzY2ZjldWzViNWZdKGNhb21lbmcpIiwiZXhwIjoxNzQzMzIyMDc2LCJpYXQiOjE3NDI0NTgwNzYsImp0aSI6ImFHRlVmdFduQVdpbHhPWDFnUUJXYmtIdVdVVkZaQTZPSXVtN0pnblNDQUFDMk5WRCJ9.ZZh5Cs5nRzWHss_1D1BmAJsEqI5k11qXvnW9E6JZOgI; fine_remember_login=-1; sessionID={session_id[1]}'
        }
        now = datetime.now()
        if start_date == '':
            start_date = now - timedelta(days=30)
            start_date = start_date.strftime('%Y-%m-%d')
        if end_date == '':
            end_date = now.strftime('%Y-%m-%d')
        json_data = {
            "开始日期": f"{start_date}",
            "截止日期": f"{end_date}",
            "LABEL日期": "日期:",
            "LABEL类别": "类别:",
            "LABEL公司": "公司:",
            "公司": f"{company}",
            "类别": f"{category}",
            "LABEL站点": "站点:",
            "站点": f"{site}"
        }
        #连续2次编码
        json_data = urllib.parse.quote(str(json_data))
        json_data = urllib.parse.quote(json_data)
        # print(json_data)
        data1 = f'__parameters__={json_data}'
        response1 = requests.post(url1, headers=headers1, data=data1)
        # print(response1.json())
        assert response1.json()['status'] == 'success'
        log.debug('原材料取样台账报表查询成功')
    def yc_tj_search(self,start_date='',end_date='', category='', site=''):
        """原材料取样统计-按日期、站点、类别查询"""
        # 1.访问帆软链接，获取sessionID
        api = Api('api')['帆软链接']
        host = self.host
        # viewlet = urllib.parse.quote('CQMS系统/原材料管理/原材料取样/原材料取样统计[ERP].cpt', safe='') #safe='',强制编码所有非安全字符，即"/"也编码掉
        api = "?".join([api,'viewlet=CQMS%E7%B3%BB%E7%BB%9F%2F%E5%8E%9F%E6%9D%90%E6%96%99%E7%AE%A1%E7%90%86%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%E7%BB%9F%E8%AE%A1%5BERP%5D.cpt'])
        headers = {
            "Cookie": "fineMarkId=38e5f95408bb300c88f21eead0aa1a0b; fine_auth_token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjYW9tZW5nIiwidGVuYW50SWQiOiJkZWZhdWx0IiwiaXNzIjoiZmFucnVhbiIsImRlc2NyaXB0aW9uIjoiWzY2ZjldWzViNWZdKGNhb21lbmcpIiwiZXhwIjoxNzQzMzIyMDc2LCJpYXQiOjE3NDI0NTgwNzYsImp0aSI6ImFHRlVmdFduQVdpbHhPWDFnUUJXYmtIdVdVVkZaQTZPSXVtN0pnblNDQUFDMk5WRCJ9.ZZh5Cs5nRzWHss_1D1BmAJsEqI5k11qXvnW9E6JZOgI; fine_remember_login=-1"
        }
        url = f"https://{host}{api}"
        # print(url)
        response = requests.get(url, headers=headers)
        session_id_data = response.headers.get('Set-Cookie')
        # print(session_id_data)
        session_id_list = session_id_data.split(';')
        # print(session_id_list)
        session_id = session_id_list[0].split('=')
        # print(response.headers)
        # print(session_id)
        # 2.原材料取样统计查询
        api1 = Api('api')['原材料取样查询']
        time1 = datetime.now()
        timestamp1 = int(time1.timestamp() * 1000)
        api2 = '?'.join([api1, f'_={timestamp1}'])
        host = Readconfig('HOST-FR').host
        url1 = f"https://{host}{api2}"
        # print(url1)
        headers1 = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sessionID": session_id[1],
            "Cookie": f'fine_auth_token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjYW9tZW5nIiwidGVuYW50SWQiOiJkZWZhdWx0IiwiaXNzIjoiZmFucnVhbiIsImRlc2NyaXB0aW9uIjoiWzY2ZjldWzViNWZdKGNhb21lbmcpIiwiZXhwIjoxNzQzMzIyMDc2LCJpYXQiOjE3NDI0NTgwNzYsImp0aSI6ImFHRlVmdFduQVdpbHhPWDFnUUJXYmtIdVdVVkZaQTZPSXVtN0pnblNDQUFDMk5WRCJ9.ZZh5Cs5nRzWHss_1D1BmAJsEqI5k11qXvnW9E6JZOgI; fine_remember_login=-1; sessionID={session_id[1]}'
        }
        now = datetime.now()
        if start_date == '':
            start_date = now - timedelta(days=30)
            start_date = start_date.strftime('%Y-%m-%d')
        if end_date == '':
            end_date = now.strftime('%Y-%m-%d')
        json_data = {
            "开始日期": f"{start_date}",
            "截止日期": f"{end_date}",
            "LABEL公司_C": "日期:",
            "LABEL站点": "站点:",
            "站点": [f'{site}'],
            "LABEL材料类别": "类别:",
            "材料类别": f"{category}"
        }
        json_data = urllib.parse.quote(str(json_data))
        json_data = urllib.parse.quote(json_data)
        # print(json_data)
        data1 = f'__parameters__={json_data}'
        response1 = requests.post(url1, headers=headers1, data=data1)
        # print(response1.json())
        assert response1.json()['status'] == 'success'
        log.debug('原材料取样统计报表查询成功')
    def yc_pc_search(self,start_date='',end_date=''):
        """原材料频次分析-查询接口，按日期查询"""
        # 1.访问帆软链接，获取sessionID
        api = Api('api')['帆软链接']
        host = self.host
        # viewlet = urllib.parse.quote('CQMS系统/原材料管理/原材料取样/取样频次.frm', safe='') #safe='',强制编码所有非安全字符，即"/"也编码掉
        api = "?".join([api,
                        'viewlet=CQMS%E7%B3%BB%E7%BB%9F%2F%E5%8E%9F%E6%9D%90%E6%96%99%E7%AE%A1%E7%90%86%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%2F%E5%8F%96%E6%A0%B7%E9%A2%91%E6%AC%A1.frm'])
        headers = {
            "Cookie": "fineMarkId=38e5f95408bb300c88f21eead0aa1a0b; fine_auth_token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjYW9tZW5nIiwidGVuYW50SWQiOiJkZWZhdWx0IiwiaXNzIjoiZmFucnVhbiIsImRlc2NyaXB0aW9uIjoiWzY2ZjldWzViNWZdKGNhb21lbmcpIiwiZXhwIjoxNzQzMzIyMDc2LCJpYXQiOjE3NDI0NTgwNzYsImp0aSI6ImFHRlVmdFduQVdpbHhPWDFnUUJXYmtIdVdVVkZaQTZPSXVtN0pnblNDQUFDMk5WRCJ9.ZZh5Cs5nRzWHss_1D1BmAJsEqI5k11qXvnW9E6JZOgI; fine_remember_login=-1"
        }
        url = f"https://{host}{api}"
        # print(url)
        response = requests.get(url, headers=headers)
        session_id_data = response.headers.get('Set-Cookie')
        # print(session_id_data)
        session_id_list = session_id_data.split(';')
        # print(session_id_list)
        session_id = session_id_list[0].split('=')
        # print(response.headers)
        # print(session_id)
        # 2.原材料频次分析查询
        api1 = Api('api')['原材料取样查询']
        time1 = datetime.now()
        timestamp1 = int(time1.timestamp() * 1000)
        api2 = '?'.join([api1, f'_={timestamp1}'])
        host = Readconfig('HOST-FR').host
        url1 = f"https://{host}{api2}"
        # print(url1)
        headers1 = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sessionID": session_id[1],
            "Cookie": f'fine_auth_token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjYW9tZW5nIiwidGVuYW50SWQiOiJkZWZhdWx0IiwiaXNzIjoiZmFucnVhbiIsImRlc2NyaXB0aW9uIjoiWzY2ZjldWzViNWZdKGNhb21lbmcpIiwiZXhwIjoxNzQzMzIyMDc2LCJpYXQiOjE3NDI0NTgwNzYsImp0aSI6ImFHRlVmdFduQVdpbHhPWDFnUUJXYmtIdVdVVkZaQTZPSXVtN0pnblNDQUFDMk5WRCJ9.ZZh5Cs5nRzWHss_1D1BmAJsEqI5k11qXvnW9E6JZOgI; fine_remember_login=-1; sessionID={session_id[1]}'
        }
        now = datetime.now()
        if start_date == '':
            start_date = now - timedelta(days=30)
            start_date = start_date.strftime('%Y-%m-%d')
        if end_date == '':
            end_date = now.strftime('%Y-%m-%d')
        json_data = {
            "LABEL0_C": "日期选择范围：",
            "开始日期": f"{start_date}",
            "LABEL1_C": "-",
            "截止日期": f"{end_date}",
            "AA": "1",
            "公司": ""
        }
        json_data = urllib.parse.quote(str(json_data))
        # print(json_data)
        json_data = urllib.parse.quote(json_data)
        # print(json_data)
        data1 = f'__parameters__={json_data}'
        response1 = requests.post(url1, headers=headers1, data=data1)
        # print(response1.json())
        assert response1.json()['status'] == 'success'
        log.debug('原材料频次分析报表查询成功')

if __name__ == '__main__':
    lg = YcLgLi()
    lg.yc_tz_search(site='08805',company='2')
    lg.yc_tj_search(site='08805')
    lg.yc_pc_search()


