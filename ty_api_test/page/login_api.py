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
    data = {
        "username": f"{user}",
        "password": f"{password}",
        "grant_type": "password"
    }
    # print(data)
    # 发送POST请求
    # response = requests.post(url, headers=headers, data=data,verify=False)  #如果报错ssl证书异常，可以暂时设置verify=False来规避
    response = requests.post(url, headers=headers, data=data)

    # 打印响应状态码
    #print("Status Code:", response.status_code)
    # print(response.json())
    assert response.status_code == 200
    log.debug("登录成功")
    # 打印响应内容
    #print("Response Body:", response.json())
    data1 = response.json()
    authorization = data1.get("access_token")
    #log.debug("access_token为：%s"%(Authorization))
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
    return authorization,userid

#login("User2", "Password2")
#User3 = wangyong6
#User2 = kangle1
#User1 = caomeng
# login()
