from ty_api_test.common.logger import *
from ty_api_test.page.portal_login_api import login
from ty_api_test.common.readconfig import *
from ty_api_test.common.readapi import *
import requests

class CqMsSy:
    """CQMS首页"""
    def __init__(self):
        self.authorization, self.userid, self.authority_list, self.company_id = login()
    def cqms_sy(self):
        api = Api('api')['用户信息']
        host = Readconfig('HOST').host
        if 'CQMS_2_USER' in self.authority_list:
            api ='?'.join([api,f'companyId=0&userId={self.userid}'])
            headers = {
                "Authorization": f"Bearer {self.authorization}"
            }
            url = f"https://{host}{api}"
            response = requests.get(url, headers=headers)
            # print(response.json())
            user_menu = response.json()['data']['userMenu']
            assert user_menu[0]['title'] == '返回砼翼首页'
            log.debug("成功进入砼翼首页")
        else:
            log.debug("用户权限不足，没有CQMS访问权限")



if __name__ == '__main__':
    cq = CqMsSy()
    cq.cqms_sy()