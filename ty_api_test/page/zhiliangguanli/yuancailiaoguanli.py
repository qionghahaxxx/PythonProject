import urllib.parse

from ty_api_test.common.logger import *
from ty_api_test.page.portal_login_api import login
from ty_api_test.common.readconfig import *
from ty_api_test.common.readapi import *
import requests
from datetime import datetime
from http.cookies import SimpleCookie

class YcLgLi:
    """原材料管理模块相关api方法封装"""
    def __init__(self):

        self.authorization, self.userid, self.company_id, self.fr_encrypted_username = login(u='User4', p='Password4')
        # 1.帆软单点认证，获取fine_auth_token相关认证凭证信息
        api_fr = Api('api')['帆软单点认证']
        api_fr = '?'.join([api_fr, f'username={self.fr_encrypted_username}&callback=ng_jsonp_callback_0'])
        host = Readconfig('HOST-FR').host
        url_fr = f"https://{host}{api_fr}"
        # 创建会话以自动管理Cookie
        session = requests.Session()
        url = url_fr
        response = session.get(url, allow_redirects=False)

        # 存储所有Set-Cookie头
        all_set_cookies = []

        # 跟踪重定向链
        while response.status_code in (301, 302, 303, 307, 308):
            # 获取当前响应的所有Set-Cookie头
            # set_cookies = response.raw.headers.get_all("Set-Cookie", [])
            set_cookies = response.raw.headers.get_all("Set-Cookie", [])
            all_set_cookies.extend(set_cookies)

            # 获取重定向目标
            redirect_url = response.headers["Location"]
            # 发送下一个请求（会话会自动携带已设置的Cookie）
            response = session.get(redirect_url, allow_redirects=False)

        # 处理最终响应（非重定向状态码）
        if response.ok:
            set_cookies = response.raw.headers.get_all("Set-Cookie", [])
            all_set_cookies.extend(set_cookies)

        # 解析所有Set-Cookie头
        parsed_cookies = []
        for cookie_header in all_set_cookies:
            cookie = SimpleCookie()
            cookie.load(cookie_header)
            # 提取键值对
            for key, morsel in cookie.items():
                parsed_cookies.append({key: morsel.value})

        # print("所有Set-Cookie头:", all_set_cookies)
        # print("解析后的Cookie键值对:", parsed_cookies)
        self.fine_auth_token = parsed_cookies[0]['fine_auth_token']
    def yc_tz_search(self,start_date='',end_date='',company='', category='', site=''):
        """原材料取样台账查询接口-可以按日期、公司、分类、站点查询"""

        # 1.访问帆软链接，获取sessionID
        api = Api('api')['帆软链接']
        host = Readconfig('HOST-FR').host
        # viewlet = urllib.parse.quote('CQMS系统/原材料管理/原材料取样/原材料检测频次台账.cpt', safe='') #safe='',强制编码所有非安全字符，即"/"也编码掉
        api = "?".join([api,
                        'viewlet=CQMS%E7%B3%BB%E7%BB%9F%2F%E5%8E%9F%E6%9D%90%E6%96%99%E7%AE%A1%E7%90%86%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%2F%E5%8E%9F%E6%9D%90%E6%96%99%E6%A3%80%E6%B5%8B%E9%A2%91%E6%AC%A1%E5%8F%B0%E8%B4%A6.cpt'])
        headers = {
            "Cookie": f"fineMarkId=38e5f95408bb300c88f21eead0aa1a0b; fine_auth_token={self.fine_auth_token}; fine_remember_login=-1"
        }
        url = f"https://{host}{api}"
        # print(url)
        response = requests.get(url, headers=headers)
        session_id_data = response.headers.get('Set-Cookie')
        session_id_list = session_id_data.split(';')
        # print(session_id_list)
        session_id = session_id_list[0].split('=')
        # print(session_id)
        #2.原材料取样台账查询
        api1 = Api('api')['原材料报表查询']
        time1 = datetime.now()
        timestamp1 = int(time1.timestamp() * 1000)
        api2 = '?'.join([api1, f'_={timestamp1}'])
        host = Readconfig('HOST-FR').host
        url1 = f"https://{host}{api2}"
        # print(url1)
        headers1 = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sessionID": f"{session_id[1]}",
            "Cookie": f'fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id[1]}'
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
        """原材料取样统计查询接口-按日期、站点、类别查询"""
        # 1.访问帆软链接，获取sessionID
        api = Api('api')['帆软链接']
        host = Readconfig('HOST-FR').host
        # viewlet = urllib.parse.quote('CQMS系统/原材料管理/原材料取样/原材料取样统计[ERP].cpt', safe='') #safe='',强制编码所有非安全字符，即"/"也编码掉
        api = "?".join([api,'viewlet=CQMS%E7%B3%BB%E7%BB%9F%2F%E5%8E%9F%E6%9D%90%E6%96%99%E7%AE%A1%E7%90%86%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%E7%BB%9F%E8%AE%A1%5BERP%5D.cpt'])
        headers = {
            "Cookie": f"fineMarkId=38e5f95408bb300c88f21eead0aa1a0b;fine_auth_token={self.fine_auth_token}; fine_remember_login=-1"
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
        api1 = Api('api')['原材料报表查询']
        time1 = datetime.now()
        timestamp1 = int(time1.timestamp() * 1000)
        api2 = '?'.join([api1, f'_={timestamp1}'])
        host = Readconfig('HOST-FR').host
        url1 = f"https://{host}{api2}"
        # print(url1)
        headers1 = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sessionID": session_id[1],
            "Cookie": f'fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id[1]}'
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
        host = Readconfig('HOST-FR').host
        # viewlet = urllib.parse.quote('CQMS系统/原材料管理/原材料取样/取样频次.frm', safe='') #safe='',强制编码所有非安全字符，即"/"也编码掉
        api = "?".join([api,
                        'viewlet=CQMS%E7%B3%BB%E7%BB%9F%2F%E5%8E%9F%E6%9D%90%E6%96%99%E7%AE%A1%E7%90%86%2F%E5%8E%9F%E6%9D%90%E6%96%99%E5%8F%96%E6%A0%B7%2F%E5%8F%96%E6%A0%B7%E9%A2%91%E6%AC%A1.frm'])
        headers = {
            "Cookie": f"fineMarkId=38e5f95408bb300c88f21eead0aa1a0b; fine_auth_token={self.fine_auth_token}; fine_remember_login=-1"
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
        api1 = Api('api')['原材料报表查询']
        time1 = datetime.now()
        timestamp1 = int(time1.timestamp() * 1000)
        api2 = '?'.join([api1, f'_={timestamp1}'])
        host = Readconfig('HOST-FR').host
        url1 = f"https://{host}{api2}"
        # print(url1)
        headers1 = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sessionID": f"{session_id[1]}",
            "Cookie": f'fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id[1]}'
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
    def yc_jc_sn(self,start_date='',end_date='', guige='', brand ='',supplier='',testno='',site=''):
        """原材料检测台账-水泥检测台账查询接口"""
        # 1.访问原材料检测台账帆软链接，获取sessionID
        api = Api('api')['帆软链接']
        host = Readconfig('HOST-FR').host
        viewlet = urllib.parse.quote('CQMS系统/原材料检测台账/原材料检测台账.frm', safe='') #safe='',强制编码所有非安全字符，即"/"也编码掉
        api = "?".join([api,f'viewlet={viewlet}'])
        headers = {
            "Cookie": f"fineMarkId=38e5f95408bb300c88f21eead0aa1a0b; fine_auth_token={self.fine_auth_token}; fine_remember_login=-1"
        }
        url = f"https://{host}{api}"
        # print(url)
        response = requests.get(url, headers=headers)
        session_id_data = response.headers.get('Set-Cookie')
        # print(session_id_data)
        session_id_list = session_id_data.split(';')
        # print(session_id_list)
        session_id = session_id_list[0].split('=')
        # print(session_id)
        # 2.访问原材料检测台账-水泥报表链接，获取sessionID
        api1 = Api('api')['原材料检测查询']
        viewlet_data = urllib.parse.quote(urllib.parse.quote('/CQMS系统/原材料检测台账/原材料检测台账-水泥.cpt', safe=''))
        ap2 = '?'.join([api1, f'viewlet={viewlet_data}&width=1667&height=491'])
        url1 = f"https://{host}{ap2}"
        headers1 = {
            "Cookie": f'fineMarkId=38e5f95408bb300c88f21eead0aa1a0b;fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id[1]}'
        }
        response1 = requests.get(url1, headers=headers1)
        session_id_data1 = response1.headers.get('Set-Cookie')
        session_id_list1 = session_id_data1.split(';')
        session_id1 = session_id_list1[0].split('=')
        #3.查询原材料检测台账-水泥报表
        api2 = Api('api')['原材料报表查询']
        time1 = datetime.now()
        timestamp1 = int(time1.timestamp() * 1000)
        api2 = '?'.join([api2, f'_={timestamp1}'])
        host = Readconfig('HOST-FR').host
        url2 = f"https://{host}{api2}"
        headers1 = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sessionID": f"{session_id1[1]}",
            "Cookie": f'fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id1[1]}'
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
            "规格": f"{guige}",
            "品牌": f"{brand}",
            "LABEL公司_C": "日期:",
            "供应商": f"{supplier}",
            "排序": "抽样日期",
            "检验编号": f"{testno}",
            "站点": f"{site}",
            "公司": "",
            "AA": "1"
        }
        json_data = urllib.parse.quote(str(json_data))
        json_data = urllib.parse.quote(json_data)
        data1 = f'__parameters__={json_data}'
        response1 = requests.post(url2, headers=headers1, data=data1)
        print(response1.json())
        assert response1.json()['status'] == 'success'
        log.debug('原材料检测台账-水泥报表查询成功')
    def yc_jc_fmh(self,start_date='',end_date='', guige='', brand ='',supplier='',testno='',site=''):
        """原材料检测台账-粉煤灰检测台账查询接口"""
        # 1.访问原材料检测台账帆软链接，获取sessionID
        api = Api('api')['帆软链接']
        host = Readconfig('HOST-FR').host
        viewlet = urllib.parse.quote('CQMS系统/原材料检测台账/原材料检测台账.frm',
                                     safe='')  # safe='',强制编码所有非安全字符，即"/"也编码掉
        api = "?".join([api, f'viewlet={viewlet}'])
        headers = {
            "Cookie": f"fineMarkId=38e5f95408bb300c88f21eead0aa1a0b; fine_auth_token={self.fine_auth_token}; fine_remember_login=-1"
        }
        url = f"https://{host}{api}"
        # print(url)
        response = requests.get(url, headers=headers)
        session_id_data = response.headers.get('Set-Cookie')
        # print(session_id_data)
        session_id_list = session_id_data.split(';')
        # print(session_id_list)
        session_id = session_id_list[0].split('=')
        # print(session_id)
        # 2.访问原材料检测台账-粉煤灰报表链接，获取sessionID
        api1 = Api('api')['原材料检测查询']
        viewlet_data = urllib.parse.quote(
            urllib.parse.quote('/CQMS系统/原材料检测台账/原材料检测台账-粉煤灰.cpt', safe=''))
        ap2 = '?'.join([api1, f'viewlet={viewlet_data}&width=1667&height=491'])
        url1 = f"https://{host}{ap2}"
        headers1 = {
            "Cookie": f'fineMarkId=38e5f95408bb300c88f21eead0aa1a0b;fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id[1]}'
        }
        response1 = requests.get(url1, headers=headers1)
        session_id_data1 = response1.headers.get('Set-Cookie')
        session_id_list1 = session_id_data1.split(';')
        session_id1 = session_id_list1[0].split('=')
        # 3.查询原材料检测台账-粉煤灰报表
        api2 = Api('api')['原材料报表查询']
        time1 = datetime.now()
        timestamp1 = int(time1.timestamp() * 1000)
        api2 = '?'.join([api2, f'_={timestamp1}'])
        host = Readconfig('HOST-FR').host
        url2 = f"https://{host}{api2}"
        headers1 = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sessionID": f"{session_id1[1]}",
            "Cookie": f'fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id1[1]}'
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
            "规格": f"{guige}",
            "品牌": f"{brand}",
            "LABEL公司_C": "日期:",
            "供应商": f"{supplier}",
            "排序": "抽样日期",
            "检验编号": f"{testno}",
            "站点": f"{site}",
            "公司": "",
            "AA": "1"
        }
        json_data = urllib.parse.quote(str(json_data))
        json_data = urllib.parse.quote(json_data)
        data1 = f'__parameters__={json_data}'
        response1 = requests.post(url2, headers=headers1, data=data1)
        print(response1.json())
        assert response1.json()['status'] == 'success'
        log.debug('原材料检测台账-粉煤灰报表查询成功')
    def yc_jc_kf(self,start_date='',end_date='', guige='', brand ='',supplier='',testno='',site=''):
        """原材料检测台账-矿粉检测台账查询接口"""
        # 1.访问原材料检测台账帆软链接，获取sessionID
        api = Api('api')['帆软链接']
        host = Readconfig('HOST-FR').host
        viewlet = urllib.parse.quote('CQMS系统/原材料检测台账/原材料检测台账.frm',
                                     safe='')  # safe='',强制编码所有非安全字符，即"/"也编码掉
        api = "?".join([api, f'viewlet={viewlet}'])
        headers = {
            "Cookie": f"fineMarkId=38e5f95408bb300c88f21eead0aa1a0b; fine_auth_token={self.fine_auth_token}; fine_remember_login=-1"
        }
        url = f"https://{host}{api}"
        # print(url)
        response = requests.get(url, headers=headers)
        session_id_data = response.headers.get('Set-Cookie')
        # print(session_id_data)
        session_id_list = session_id_data.split(';')
        # print(session_id_list)
        session_id = session_id_list[0].split('=')
        # print(session_id)
        # 2.访问原材料检测台账-矿粉报表链接，获取sessionID
        api1 = Api('api')['原材料检测查询']
        viewlet_data = urllib.parse.quote(
            urllib.parse.quote('/CQMS系统/原材料检测台账/原材料检测台账-矿粉.cpt', safe=''))
        ap2 = '?'.join([api1, f'viewlet={viewlet_data}&width=1667&height=491'])
        url1 = f"https://{host}{ap2}"
        headers1 = {
            "Cookie": f'fineMarkId=38e5f95408bb300c88f21eead0aa1a0b;fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id[1]}'
        }
        response1 = requests.get(url1, headers=headers1)
        session_id_data1 = response1.headers.get('Set-Cookie')
        session_id_list1 = session_id_data1.split(';')
        session_id1 = session_id_list1[0].split('=')
        # 3.查询原材料检测台账-矿粉报表
        api2 = Api('api')['原材料报表查询']
        time1 = datetime.now()
        timestamp1 = int(time1.timestamp() * 1000)
        api2 = '?'.join([api2, f'_={timestamp1}'])
        host = Readconfig('HOST-FR').host
        url2 = f"https://{host}{api2}"
        headers1 = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sessionID": f"{session_id1[1]}",
            "Cookie": f'fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id1[1]}'
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
            "规格": f"{guige}",
            "品牌": f"{brand}",
            "LABEL公司_C": "日期:",
            "供应商": f"{supplier}",
            "排序": "抽样日期",
            "检验编号": f"{testno}",
            "站点": f"{site}",
            "公司": "",
            "AA": "1"
        }
        json_data = urllib.parse.quote(str(json_data))
        json_data = urllib.parse.quote(json_data)
        data1 = f'__parameters__={json_data}'
        response1 = requests.post(url2, headers=headers1, data=data1)
        print(response1.json())
        assert response1.json()['status'] == 'success'
        log.debug('原材料检测台账-矿粉报表查询成功')
    def yc_jc_cgf(self,start_date='',end_date='', guige='', brand ='',supplier='',testno='',site=''):
        """原材料检测台账-粗骨料检测台账查询接口"""
        # 1.访问原材料检测台账帆软链接，获取sessionID
        api = Api('api')['帆软链接']
        host = Readconfig('HOST-FR').host
        viewlet = urllib.parse.quote('CQMS系统/原材料检测台账/原材料检测台账.frm',
                                     safe='')  # safe='',强制编码所有非安全字符，即"/"也编码掉
        api = "?".join([api, f'viewlet={viewlet}'])
        headers = {
            "Cookie": f"fineMarkId=38e5f95408bb300c88f21eead0aa1a0b; fine_auth_token={self.fine_auth_token}; fine_remember_login=-1"
        }
        url = f"https://{host}{api}"
        # print(url)
        response = requests.get(url, headers=headers)
        session_id_data = response.headers.get('Set-Cookie')
        # print(session_id_data)
        session_id_list = session_id_data.split(';')
        # print(session_id_list)
        session_id = session_id_list[0].split('=')
        # print(session_id)
        # 2.访问原材料检测台账-粗骨料报表链接，获取sessionID
        api1 = Api('api')['原材料检测查询']
        viewlet_data = urllib.parse.quote(
            urllib.parse.quote('/CQMS系统/原材料检测台账/原材料检测台账-粗骨料.cpt', safe=''))
        ap2 = '?'.join([api1, f'viewlet={viewlet_data}&width=1667&height=491'])
        url1 = f"https://{host}{ap2}"
        headers1 = {
            "Cookie": f'fineMarkId=38e5f95408bb300c88f21eead0aa1a0b;fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id[1]}'
        }
        response1 = requests.get(url1, headers=headers1)
        session_id_data1 = response1.headers.get('Set-Cookie')
        session_id_list1 = session_id_data1.split(';')
        session_id1 = session_id_list1[0].split('=')
        # 3.查询原材料检测台账-粗骨料报表
        api2 = Api('api')['原材料报表查询']
        time1 = datetime.now()
        timestamp1 = int(time1.timestamp() * 1000)
        api2 = '?'.join([api2, f'_={timestamp1}'])
        host = Readconfig('HOST-FR').host
        url2 = f"https://{host}{api2}"
        headers1 = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sessionID": f"{session_id1[1]}",
            "Cookie": f'fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id1[1]}'
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
            "规格": f"{guige}",
            "品牌": f"{brand}",
            "LABEL公司_C": "日期:",
            "供应商": f"{supplier}",
            "排序": "抽样日期",
            "检验编号": f"{testno}",
            "站点": f"{site}",
            "公司": "",
            "AA": "1"
        }
        json_data = urllib.parse.quote(str(json_data))
        json_data = urllib.parse.quote(json_data)
        data1 = f'__parameters__={json_data}'
        response1 = requests.post(url2, headers=headers1, data=data1)
        print(response1.json())
        assert response1.json()['status'] == 'success'
        log.debug('原材料检测台账-粗骨料报表查询成功')

    def yc_jc_xgf(self,start_date='',end_date='', guige='', brand ='',supplier='',testno='',site=''):
        """原材料检测台账-细骨料检测台账查询接口"""
        # 1.访问原材料检测台账帆软链接，获取sessionID
        api = Api('api')['帆软链接']
        host = Readconfig('HOST-FR').host
        viewlet = urllib.parse.quote('CQMS系统/原材料检测台账/原材料检测台账.frm',
                                     safe='')  # safe='',强制编码所有非安全字符，即"/"也编码掉
        api = "?".join([api, f'viewlet={viewlet}'])
        headers = {
            "Cookie": f"fineMarkId=38e5f95408bb300c88f21eead0aa1a0b; fine_auth_token={self.fine_auth_token}; fine_remember_login=-1"
        }
        url = f"https://{host}{api}"
        # print(url)
        response = requests.get(url, headers=headers)
        session_id_data = response.headers.get('Set-Cookie')
        # print(session_id_data)
        session_id_list = session_id_data.split(';')
        # print(session_id_list)
        session_id = session_id_list[0].split('=')
        # print(session_id)
        # 2.访问原材料检测台账-细骨料报表链接，获取sessionID
        api1 = Api('api')['原材料检测查询']
        viewlet_data = urllib.parse.quote(
            urllib.parse.quote('/CQMS系统/原材料检测台账/原材料检测台账-细骨料.cpt', safe=''))
        ap2 = '?'.join([api1, f'viewlet={viewlet_data}&width=1667&height=491'])
        url1 = f"https://{host}{ap2}"
        headers1 = {
            "Cookie": f'fineMarkId=38e5f95408bb300c88f21eead0aa1a0b;fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id[1]}'
        }
        response1 = requests.get(url1, headers=headers1)
        session_id_data1 = response1.headers.get('Set-Cookie')
        session_id_list1 = session_id_data1.split(';')
        session_id1 = session_id_list1[0].split('=')
        # 3.查询原材料检测台账-细骨料报表
        api2 = Api('api')['原材料报表查询']
        time1 = datetime.now()
        timestamp1 = int(time1.timestamp() * 1000)
        api2 = '?'.join([api2, f'_={timestamp1}'])
        host = Readconfig('HOST-FR').host
        url2 = f"https://{host}{api2}"
        headers1 = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sessionID": f"{session_id1[1]}",
            "Cookie": f'fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id1[1]}'
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
            "规格": f"{guige}",
            "品牌": f"{brand}",
            "LABEL公司_C": "日期:",
            "供应商": f"{supplier}",
            "排序": "抽样日期",
            "检验编号": f"{testno}",
            "站点": f"{site}",
            "公司": "",
            "AA": "1"
        }
        json_data = urllib.parse.quote(str(json_data))
        json_data = urllib.parse.quote(json_data)
        data1 = f'__parameters__={json_data}'
        response1 = requests.post(url2, headers=headers1, data=data1)
        print(response1.json())
        assert response1.json()['status'] == 'success'
        log.debug('原材料检测台账-细骨料报表查询成功')

    def yc_jc_wjj(self,start_date='',end_date='', guige='', brand ='',supplier='',testno='',site=''):
        """原材料检测台账-外加剂检测台账查询接口"""
        # 1.访问原材料检测台账帆软链接，获取sessionID
        api = Api('api')['帆软链接']
        host = Readconfig('HOST-FR').host
        viewlet = urllib.parse.quote('CQMS系统/原材料检测台账/原材料检测台账.frm',
                                     safe='')  # safe='',强制编码所有非安全字符，即"/"也编码掉
        api = "?".join([api, f'viewlet={viewlet}'])
        headers = {
            "Cookie": f"fineMarkId=38e5f95408bb300c88f21eead0aa1a0b; fine_auth_token={self.fine_auth_token}; fine_remember_login=-1"
        }
        url = f"https://{host}{api}"
        # print(url)
        response = requests.get(url, headers=headers)
        session_id_data = response.headers.get('Set-Cookie')
        # print(session_id_data)
        session_id_list = session_id_data.split(';')
        # print(session_id_list)
        session_id = session_id_list[0].split('=')
        # print(session_id)
        # 2.访问原材料检测台账-外加剂报表链接，获取sessionID
        api1 = Api('api')['原材料检测查询']
        viewlet_data = urllib.parse.quote(
            urllib.parse.quote('/CQMS系统/原材料检测台账/原材料检测台账-外加剂.cpt', safe=''))
        ap2 = '?'.join([api1, f'viewlet={viewlet_data}&width=1667&height=491'])
        url1 = f"https://{host}{ap2}"
        headers1 = {
            "Cookie": f'fineMarkId=38e5f95408bb300c88f21eead0aa1a0b;fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id[1]}'
        }
        response1 = requests.get(url1, headers=headers1)
        session_id_data1 = response1.headers.get('Set-Cookie')
        session_id_list1 = session_id_data1.split(';')
        session_id1 = session_id_list1[0].split('=')
        # 3.查询原材料检测台账-外加剂报表
        api2 = Api('api')['原材料报表查询']
        time1 = datetime.now()
        timestamp1 = int(time1.timestamp() * 1000)
        api2 = '?'.join([api2, f'_={timestamp1}'])
        host = Readconfig('HOST-FR').host
        url2 = f"https://{host}{api2}"
        headers1 = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sessionID": f"{session_id1[1]}",
            "Cookie": f'fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id1[1]}'
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
            "规格": f"{guige}",
            "品牌": f"{brand}",
            "LABEL公司_C": "日期:",
            "供应商": f"{supplier}",
            "排序": "抽样日期",
            "检验编号": f"{testno}",
            "站点": f"{site}",
            "公司": "",
            "AA": "1"
        }
        json_data = urllib.parse.quote(str(json_data))
        json_data = urllib.parse.quote(json_data)
        data1 = f'__parameters__={json_data}'
        response1 = requests.post(url2, headers=headers1, data=data1)
        print(response1.json())
        assert response1.json()['status'] == 'success'
        log.debug('原材料检测台账-外加剂报表查询成功')
    @staticmethod
    def str_to_unicode_hex(text):
        encoded = []
        for char in text:
            hex_value = format(ord(char), '04x')  # 转为4位十六进制，不足补零
            encoded.append(f'[{hex_value}]')
        return ''.join(encoded)
    def yc_zb_sn(self,start_date='',end_date='',guige='',brand='',supplier='',site=''):
        """原材料指标分析-水泥报表查询接口"""
        # 1.访问原材料检测台账帆软链接，获取sessionID
        api = Api('api')['帆软链接']
        host = Readconfig('HOST-FR').host
        viewlet = urllib.parse.quote('CQMS系统/原材料管理/原材料检测分析/原材料检测指标分析.frm',
                                     safe='')  # safe='',强制编码所有非安全字符，即"/"也编码掉
        api = "?".join([api, f'viewlet={viewlet}'])
        headers = {
            "Cookie": f"fineMarkId=38e5f95408bb300c88f21eead0aa1a0b; fine_auth_token={self.fine_auth_token}; fine_remember_login=-1"
        }
        url = f"https://{host}{api}"
        # print(url)
        response = requests.get(url, headers=headers)
        session_id_data = response.headers.get('Set-Cookie')
        # print(session_id_data)
        session_id_list = session_id_data.split(';')
        # print(session_id_list)
        session_id = session_id_list[0].split('=')
        # print(session_id)
        # 2.访问原材料检测分析-水泥检测报表链接，获取sessionID
        api1 = Api('api')['原材料检测查询']
        viewlet_data = urllib.parse.quote(
            urllib.parse.quote('/CQMS系统/原材料管理/原材料检测分析/水泥检测结果分析.frm', safe=''))
        ap2 = '?'.join([api1, f'viewlet={viewlet_data}&width=1549&height=449'])
        url1 = f"https://{host}{ap2}"
        headers1 = {
            "Cookie": f'fineMarkId=38e5f95408bb300c88f21eead0aa1a0b;fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id[1]}'
        }
        response1 = requests.get(url1, headers=headers1)
        session_id_data1 = response1.headers.get('Set-Cookie')
        session_id_list1 = session_id_data1.split(';')
        session_id1 = session_id_list1[0].split('=')
        # 3.查询原材料检测分析-水泥结果分析报表
        api2 = Api('api')['原材料指标分析结果查询']
        time1 = datetime.now()
        timestamp1 = int(time1.timestamp() * 1000)
        host = Readconfig('HOST-FR').host
        url2 = f"https://{host}{api2}"
        headers1 = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sessionID": f"{session_id1[1]}",
            "Cookie": f'fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id1[1]}'
        }
        now = datetime.now()
        if start_date == '':
            start_date = now - timedelta(days=30)
            start_date = start_date.strftime('%Y-%m-%d')
        if end_date == '':
            end_date = now.strftime('%Y-%m-%d')

        para1 = self.str_to_unicode_hex('起始日期')
        para2 = self.str_to_unicode_hex('截止日期')
        para3 = self.str_to_unicode_hex('供应商')
        para4 = self.str_to_unicode_hex('站点')
        para5 = self.str_to_unicode_hex('规格')
        para6 = self.str_to_unicode_hex('品牌')
        supplier = self.str_to_unicode_hex(supplier)
        brand = self.str_to_unicode_hex(brand)
        if site == '':
            site = '00902'
        if guige == '':
            guige = 'P.O42.5R'
        json_data = {
            f"{para1}": f"{start_date}",
            f"{para2}": f"{end_date}",
            f"{para3}": f"{supplier}",
            f"{para4}": f"{site}",
            f"{para5}": f"{guige}",
            f"{para6}": f"{brand}"
        }
        # print(json_data)
        json_data = urllib.parse.quote(str(json_data))
        query_data = f'__parameters__={json_data}&_={timestamp1}'

        response1 = requests.post(url2, headers=headers1, data=query_data)
        print(response1.json())
        assert response1.json()['status'] == 'success'
        log.debug('原材料检测分析-水泥结果分析报表查询成功')

    def yc_zb_fmh(self,start_date='',end_date='',guige='',brand='',supplier='',site=''):
        """原材料指标分析-粉煤灰报表查询接口"""
        # 1.访问原材料检测台账帆软链接，获取sessionID
        api = Api('api')['帆软链接']
        host = Readconfig('HOST-FR').host
        viewlet = urllib.parse.quote('CQMS系统/原材料管理/原材料检测分析/原材料检测指标分析.frm',
                                     safe='')  # safe='',强制编码所有非安全字符，即"/"也编码掉
        api = "?".join([api, f'viewlet={viewlet}'])
        headers = {
            "Cookie": f"fineMarkId=38e5f95408bb300c88f21eead0aa1a0b; fine_auth_token={self.fine_auth_token}; fine_remember_login=-1"
        }
        url = f"https://{host}{api}"
        # print(url)
        response = requests.get(url, headers=headers)
        session_id_data = response.headers.get('Set-Cookie')
        # print(session_id_data)
        session_id_list = session_id_data.split(';')
        # print(session_id_list)
        session_id = session_id_list[0].split('=')
        # print(session_id)
        # 2.访问原材料检测分析-粉煤灰检测报表链接，获取sessionID
        api1 = Api('api')['原材料检测查询']
        viewlet_data = urllib.parse.quote(
            urllib.parse.quote('/CQMS系统/原材料管理/原材料检测分析/粉煤灰检测结果分析新.frm', safe=''))
        ap2 = '?'.join([api1, f'viewlet={viewlet_data}&width=1549&height=449'])
        url1 = f"https://{host}{ap2}"
        headers1 = {
            "Cookie": f'fineMarkId=38e5f95408bb300c88f21eead0aa1a0b;fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id[1]}'
        }
        response1 = requests.get(url1, headers=headers1)
        session_id_data1 = response1.headers.get('Set-Cookie')
        session_id_list1 = session_id_data1.split(';')
        session_id1 = session_id_list1[0].split('=')
        # 3.查询原材料检测分析-粉煤灰结果分析报表
        api2 = Api('api')['原材料指标分析结果查询']
        time1 = datetime.now()
        timestamp1 = int(time1.timestamp() * 1000)
        host = Readconfig('HOST-FR').host
        url2 = f"https://{host}{api2}"
        headers1 = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sessionID": f"{session_id1[1]}",
            "Cookie": f'fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id1[1]}'
        }
        now = datetime.now()
        if start_date == '':
            start_date = now - timedelta(days=30)
            start_date = start_date.strftime('%Y-%m-%d')
        if end_date == '':
            end_date = now.strftime('%Y-%m-%d')

        para1 = self.str_to_unicode_hex('起始日期')
        para2 = self.str_to_unicode_hex('截止日期')
        para3 = self.str_to_unicode_hex('供应商')
        para4 = self.str_to_unicode_hex('站点')
        para5 = self.str_to_unicode_hex('规格')
        para6 = self.str_to_unicode_hex('品牌')
        supplier = self.str_to_unicode_hex(supplier)
        brand = self.str_to_unicode_hex(brand)
        if guige == '':
            guige = 'F[7c7b][4e8c][7ea7]'
        if site == '':
            site = '03701'
        json_data = {
            f"{para1}": f"{start_date}",
            f"{para2}": f"{end_date}",
            f"{para3}": f"{supplier}",
            f"{para4}": f"{site}",
            f"{para5}": f"{guige}",
            f"{para6}": f"{brand}"
        }
        # print(json_data)
        json_data = urllib.parse.quote(str(json_data))
        query_data = f'__parameters__={json_data}&_={timestamp1}'
        response1 = requests.post(url2, headers=headers1, data=query_data)
        print(response1.json())
        assert response1.json()['status'] == 'success'
        log.debug('原材料检测分析-粉煤灰结果分析报表查询成功')
    def yc_zb_kf(self,start_date='',end_date='',guige='',brand='',supplier='',site=''):
        """原材料指标分析-矿粉报表查询接口"""
        # 1.访问原材料检测台账帆软链接，获取sessionID
        api = Api('api')['帆软链接']
        host = Readconfig('HOST-FR').host
        viewlet = urllib.parse.quote('CQMS系统/原材料管理/原材料检测分析/原材料检测指标分析.frm',
                                     safe='')  # safe='',强制编码所有非安全字符，即"/"也编码掉
        api = "?".join([api, f'viewlet={viewlet}'])
        headers = {
            "Cookie": f"fineMarkId=38e5f95408bb300c88f21eead0aa1a0b; fine_auth_token={self.fine_auth_token}; fine_remember_login=-1"
        }
        url = f"https://{host}{api}"
        # print(url)
        response = requests.get(url, headers=headers)
        session_id_data = response.headers.get('Set-Cookie')
        # print(session_id_data)
        session_id_list = session_id_data.split(';')
        # print(session_id_list)
        session_id = session_id_list[0].split('=')
        # print(session_id)
        # 2.访问原材料检测分析-矿粉检测报表链接，获取sessionID
        api1 = Api('api')['原材料检测查询']
        viewlet_data = urllib.parse.quote(
            urllib.parse.quote('/CQMS系统/原材料管理/原材料检测分析/矿粉检测结果分析新.frm', safe=''))
        ap2 = '?'.join([api1, f'viewlet={viewlet_data}&width=1549&height=449'])
        url1 = f"https://{host}{ap2}"
        headers1 = {
            "Cookie": f'fineMarkId=38e5f95408bb300c88f21eead0aa1a0b;fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id[1]}'
        }
        response1 = requests.get(url1, headers=headers1)
        session_id_data1 = response1.headers.get('Set-Cookie')
        session_id_list1 = session_id_data1.split(';')
        session_id1 = session_id_list1[0].split('=')
        # 3.查询原材料检测分析-矿粉结果分析报表
        api2 = Api('api')['原材料指标分析结果查询']
        time1 = datetime.now()
        timestamp1 = int(time1.timestamp() * 1000)
        host = Readconfig('HOST-FR').host
        url2 = f"https://{host}{api2}"
        headers1 = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sessionID": f"{session_id1[1]}",
            "Cookie": f'fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id1[1]}'
        }
        now = datetime.now()
        if start_date == '':
            start_date = now - timedelta(days=30)
            start_date = start_date.strftime('%Y-%m-%d')
        if end_date == '':
            end_date = now.strftime('%Y-%m-%d')

        para1 = self.str_to_unicode_hex('起始日期')
        para2 = self.str_to_unicode_hex('截止日期')
        para3 = self.str_to_unicode_hex('供应商')
        para4 = self.str_to_unicode_hex('站点')
        para5 = self.str_to_unicode_hex('规格')
        para6 = self.str_to_unicode_hex('品牌')
        supplier = self.str_to_unicode_hex(supplier)
        brand = self.str_to_unicode_hex(brand)
        if guige == '':
            guige = 'S95'
        if site == '':
            site = '09104'
        json_data = {
            f"{para1}": f"{start_date}",
            f"{para2}": f"{end_date}",
            f"{para3}": f"{supplier}",
            f"{para4}": f"{site}",
            f"{para5}": f"{guige}",
            f"{para6}": f"{brand}"
        }
        # print(json_data)
        json_data = urllib.parse.quote(str(json_data))
        query_data = f'__parameters__={json_data}&_={timestamp1}'
        response1 = requests.post(url2, headers=headers1, data=query_data)
        print(response1.json())
        assert response1.json()['status'] == 'success'
        log.debug('原材料检测分析-矿粉结果分析报表查询成功')
    def yc_zb_cgf(self,start_date='',end_date='',guige='',brand='',supplier='',site=''):
        """原材料指标分析-粗骨粉报表查询接口"""
        # 1.访问原材料检测台账帆软链接，获取sessionID
        api = Api('api')['帆软链接']
        host = Readconfig('HOST-FR').host
        viewlet = urllib.parse.quote('CQMS系统/原材料管理/原材料检测分析/原材料检测指标分析.frm',
                                     safe='')  # safe='',强制编码所有非安全字符，即"/"也编码掉
        api = "?".join([api, f'viewlet={viewlet}'])
        headers = {
            "Cookie": f"fineMarkId=38e5f95408bb300c88f21eead0aa1a0b; fine_auth_token={self.fine_auth_token}; fine_remember_login=-1"
        }
        url = f"https://{host}{api}"
        # print(url)
        response = requests.get(url, headers=headers)
        session_id_data = response.headers.get('Set-Cookie')
        # print(session_id_data)
        session_id_list = session_id_data.split(';')
        # print(session_id_list)
        session_id = session_id_list[0].split('=')
        # print(session_id)
        # 2.访问原材料检测分析-粗骨粉检测报表链接，获取sessionID
        api1 = Api('api')['原材料检测查询']
        viewlet_data = urllib.parse.quote(
            urllib.parse.quote('/CQMS系统/原材料管理/原材料检测分析/粗骨料检测结果分析新.frm', safe=''))
        ap2 = '?'.join([api1, f'viewlet={viewlet_data}&width=1549&height=449'])
        url1 = f"https://{host}{ap2}"
        headers1 = {
            "Cookie": f'fineMarkId=38e5f95408bb300c88f21eead0aa1a0b;fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id[1]}'
        }
        response1 = requests.get(url1, headers=headers1)
        session_id_data1 = response1.headers.get('Set-Cookie')
        session_id_list1 = session_id_data1.split(';')
        session_id1 = session_id_list1[0].split('=')
        # 3.查询原材料检测分析-粗骨粉结果分析报表
        api2 = Api('api')['原材料指标分析结果查询']
        time1 = datetime.now()
        timestamp1 = int(time1.timestamp() * 1000)
        host = Readconfig('HOST-FR').host
        url2 = f"https://{host}{api2}"
        headers1 = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sessionID": f"{session_id1[1]}",
            "Cookie": f'fine_auth_token={self.fine_auth_token}; fine_remember_login=-1; sessionID={session_id1[1]}'
        }
        now = datetime.now()
        if start_date == '':
            start_date = now - timedelta(days=30)
            start_date = start_date.strftime('%Y-%m-%d')
        if end_date == '':
            end_date = now.strftime('%Y-%m-%d')

        para1 = self.str_to_unicode_hex('起始日期')
        para2 = self.str_to_unicode_hex('截止日期')
        para3 = self.str_to_unicode_hex('供应商')
        para4 = self.str_to_unicode_hex('站点')
        para5 = self.str_to_unicode_hex('规格')
        para6 = self.str_to_unicode_hex('品牌')
        supplier = self.str_to_unicode_hex(supplier)
        brand = self.str_to_unicode_hex(brand)
        if guige == '':
            guige = '20-40mm'
        if site == '':
            site = '03701'
        json_data = {
            f"{para1}": f"{start_date}",
            f"{para2}": f"{end_date}",
            f"{para3}": f"{supplier}",
            f"{para4}": f"{site}",
            f"{para5}": f"{guige}",
            f"{para6}": f"{brand}"
        }
        # print(json_data)
        json_data = urllib.parse.quote(str(json_data))
        query_data = f'__parameters__={json_data}&_={timestamp1}'
        response1 = requests.post(url2, headers=headers1, data=query_data)
        print(response1.json())
        assert response1.json()['status'] == 'success'
        log.debug('原材料检测分析-粗骨粉结果分析报表查询成功')



if __name__ == '__main__':
    lg = YcLgLi()
    # lg.yc_tz_search(site='08805',company='2')
    # lg.yc_tj_search(site='08805')
    # lg.yc_pc_search()
    # lg.yc_jc_sn()
    # lg.yc_jc_fmh()
    # lg.yc_jc_kf()
    # lg.yc_jc_cgf()
    # lg.yc_jc_xgf()
    # lg.yc_jc_wjj()
    lg.yc_zb_sn()
    lg.yc_zb_fmh()
    lg.yc_zb_kf()


