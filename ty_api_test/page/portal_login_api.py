import hashlib
import requests
from ty_api_test.common.logger import *
from ty_api_test.common.readconfig import *
from ty_api_test.common.readapi import *

def login(u="User1", p="Password1"):
    """登录接口，账号、密码初始值是User1、Password1"""
    # 定义接口URL
    #url = "https://api-dev-uc.002302.com.cn/oauth/token"
    host = Readconfig('HOST').host
    api = Api('api')['登录']
    url = f"https://{host}{api}"
    # 定义请求头
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic dXNlcjokMmEkMTAkZ2xGVUF2WFRuU0tJNU81TUd0eFU5LmZwQnZQdmJxUS8uNEhBVlhvLk1nQlBXWW5LaUoxN3k="
    }

    # 定义请求参数
    user = Readconfig(u).host
    password = Readconfig(p).host
    password = hashlib.md5(password.encode()).hexdigest() #md5加密，hexdigest()方法返回一个字符串类型的哈希值摘要
    data = {
        "username": f"{user}",
        "password": f"{password}",
        "grant_type": "password"
    }
    # 发送POST请求
    response = requests.post(url, headers=headers, data=data)
    # 打印响应状态码
    assert response.status_code == 200
    log.debug("登录成功")
    # 打印响应内容
    data1 = response.json()
    authorization = data1.get("access_token")
    host1 = Readconfig('HOST').host
    api1 = Api('api')['用户信息']
    url1 = f"https://{host1}{api1}"
    headers1 = {
        "Authorization": f"Bearer {authorization}"
    }
    response1 = requests.get(url1, headers=headers1)
    # print(response1.json())
    data2 = response1.json()['data']
    userinfo = data2['userInfo']
    userid = userinfo['id']
    # print(userid)
    #需要获取用户角色信息
    authorities = userinfo['authorities']
    authority_list = []
    for authority in authorities:
        authority_list.append(authority['authority'])
        # log.debug("用户角色为：%s"%(authority['description']))
    # print(authority_list)
    companyid = authorities[0]['companyId']
    return authorization,userid,authority_list,companyid

# login()
