import urllib.parse

from ty_api_test.common.logger import *
from ty_api_test.page.portal_login_api import login
from ty_api_test.common.readconfig import *
from ty_api_test.common.readapi import *
import requests
from datetime import datetime

class YcLgLi:
    """原材料管理模块相关api方法封装"""
    # def __init__(self):
    #     self.authorization, self.userid, self.company_id = login()
    def yc_tz_search(self):
        """原材料取样台账-按当前时间查询"""
        #1.访问帆软链接，获取sessionID
        api = Api('api')['帆软链接']
        host = Readconfig('HOST-FR').host
        # viewlet = urllib.parse.quote('dw/优化/首页.frm', safe='') #safe='',强制编码所有非安全字符，即"/"也编码掉
        # api = '?'.join([api, f'{viewlet}&ref_t=design&op=form_adaptive&ref_c=c35dfbfd-52ab-4fd0-ad74-2a99618d9d58&token=L7sP9Ummj3hM4IQJnOBX8x0gbLU%253D'])
        api = "?".join([api,'viewlet=CQMS%E7%B3%BB%E7%BB%9F%2F%E5%8E%9F%E6%9D%90%E6%96%99%E7%AE%A1%E7%90%86%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%2F%E5%8E%9F%E6%9D%90%E6%96%99%E6%A3%80%E6%B5%8B%E9%A2%91%E6%AC%A1%E5%8F%B0%E8%B4%A6.cpt'])
        headers = {
            "Cookie": "fineMarkId=38e5f95408bb300c88f21eead0aa1a0b; fine_auth_token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjYW9tZW5nIiwidGVuYW50SWQiOiJkZWZhdWx0IiwiaXNzIjoiZmFucnVhbiIsImRlc2NyaXB0aW9uIjoiWzY2ZjldWzViNWZdKGNhb21lbmcpIiwiZXhwIjoxNzQzMzIyMDc2LCJpYXQiOjE3NDI0NTgwNzYsImp0aSI6ImFHRlVmdFduQVdpbHhPWDFnUUJXYmtIdVdVVkZaQTZPSXVtN0pnblNDQUFDMk5WRCJ9.ZZh5Cs5nRzWHss_1D1BmAJsEqI5k11qXvnW9E6JZOgI; fine_remember_login=-1"
        }
        url = f"https://{host}{api}"
        # print(url)
        response = requests.get(url, headers=headers)
        session_id_data = response.headers.get('Set-Cookie')
        session_id_list = session_id_data.split(';')
        print(session_id_list)
        session_id = session_id_list[0].split('=')
        # print(response.headers)
        # print(session_id)
        #2.原材料取样台账查询
        api1 = Api('api')['原材料取样台账查询']
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
        start_date = now - timedelta(days=30)
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = now.strftime('%Y-%m-%d')

        json_data = {
            "开始日期": f"{start_date}",
            "截止日期": f"{end_date}",
            "LABEL日期": "日期:",
            "LABEL类别": "类别:",
            "LABEL公司": "公司:",
            "公司": "",
            "类别": "",
            "LABEL站点": "站点:",
            "站点": ""
        }
        json_data = urllib.parse.quote(str(json_data))
        # print(json_data)
        data1 = f'__parameters__={json_data}'
        response1 = requests.post(url1, headers=headers1, data=data1)
        print(response1.json())

if __name__ == '__main__':
    lg = YcLgLi()
    lg.yc_tz_search()


