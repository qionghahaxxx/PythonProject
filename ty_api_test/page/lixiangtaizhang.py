import json
import urllib.parse


import requests
from ty_api_test.common.logger import *
from ty_api_test.page.login_api import login
from ty_api_test.common.readconfig import *
from ty_api_test.common.readapi import *
from datetime import datetime


class LxGl:
    """立项台账模块用例"""
    #authorization = login()
    def __init__(self):
        self.authorization,self.userid = login()
    def lx_search1(self,query_name):
        """立项查询-按项目名称查询"""
        # 定义接口URL
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['立项查询']
        query_name_quote = urllib.parse.quote(query_name) # 对中文进行编码
        api1 = "&".join([api,f'projectName={query_name_quote}','projectStatus='])
        url = f"https://{host}{api1}"
        # 定义请求头
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        # 发送GET请求
        response = requests.get(url, headers=headers)
        response_data = response.json()['data']
        if response_data['endRow'] == 0:
            log.debug("没有查询到数据，请重新输入")
        else:
            project_name = response_data['list'][0]['projectName']
            # print(project_name)
            assert query_name in project_name
            log.debug("查询成功")
        # print(response.json())
        # assert response.json()['code'] == 200
        # log.debug("查询成功")

    def lx_search2(self,query_status):
        """立项查询-按立项状态查询,lxtb,lxjh,lxsd,lxwc"""
        authorization = self.authorization
        # 定义接口URL
        host = Readconfig('HOST-TZB').host
        api = Api('api')['立项查询']
        url = f"https://{host}{api}"
        url1 = "&".join([url,f'projectStatus={query_status}','projectName='])
        # 定义请求头
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        # 发送GET请求
        response = requests.get(url1, headers=headers)
        # 打印响应状态码
        # print(response.json())
        response_data = response.json()['data']
        if response_data['endRow'] == 0:
            log.debug("没有查询到数据，请重新输入")
            return None
        else:
            project_status = response_data['list'][0]['projectStatus']
            # print(project_name)
            assert query_status == project_status
            log.debug("查询成功")
            project_id_list = []
            for i in range(len(response_data['list'])):
                project_id_list.append(response_data['list'][i]['projectId'])
                i += 1
            return project_id_list


    def lx_procode(self):
        """立项新增-项目编号"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['立项新增-项目编号']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        response = requests.get(url, headers=headers)
        assert response.json()['code'] == 200
        log.debug("成功返回项目编号")
    def lx_detail(self):
        """查看立项详情"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['立项详情']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        response = requests.get(url, headers=headers)
        assert response.json()['code'] == 200
        log.debug("查看立项详情成功")
    def lx_create_project(self):
        """创建立项项目"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        #获取项目编号
        api1 = Api('api')['项目编号']
        url1 = f"https://{host}{api1}"
        response1 = requests.get(url1, headers=headers)
        json1 = response1.json()
        project_code = json1.get('data')
        # print(project_code)
        #定义项目名称
        time1 = datetime.now().strftime("%Y%m%d%H%M%S")
        project_name = f"测试项目{time1}"
        # print(project_name)
        # 定义请求参数
        api = Api('api')['创建立项项目']
        url = f"https://{host}{api}"
        data = json.dumps({
	        "projectCode": f"{project_code}",
	        "projectName": f"{project_name}",
	        "companyId": 0,
	        "companyName": "总部",
	        "businessTypeId": "6",
	        "registeredCapital": 10000000,
	        "currencyTypeId": "10",
	        "investFixedAssets": 100,
	        "lineConfig": "生产线配置测试",
	        "designCapacity": 100,
	        "investContent": "投资内容测试",
	        "countryId": "1",
	        "provinceId": "",
	        "cityId": "",
	        "addDetail": "四川省成都市龙泉驿区",
	        "longitude": 104.36250469936057,
	        "latitude": 30.697316212381597,
	        "areaTypeId": "13",
	        "areaTypeCharacter": "17",
	        "areaQuare": 10,
	        "createdBy": "曹孟",
	        "dictMarketType": "",
	        "cityMarketType": "",
	        "id": "",
	        "province": "",
	        "city": "",
	        "district": "龙泉驿区"
        })
        header1 = {
            'Authorization': f'Bearer {authorization}',
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=89B7FDD075B82EA1DDED185F762A8C4E'
        }
        response = requests.post(url, headers=header1, data=data)
        # print(response.json())
        assert response.json()['code'] == 200
        log.debug("创建立项项目成功")
        data = response.json()['data']
        lx_id = data['id']

        # print(id)
        return lx_id, project_name
    def lx_remove_project(self, delete_num=1):
        """删除立项项目"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['删除立项项目']
        url = f"https://{host}{api}"

        if self.lx_search2('lxtb') :
            project_id_list = self.lx_search2('lxtb')
            for i in range(delete_num):
                lx_id = project_id_list[i]
                # print(id)
                url1 = "?".join([url, f'id={lx_id}'])
                # print(url1)
                headers = {
                    "Authorization": f"Bearer {authorization}"
                }

                payload = f'id={lx_id}'
                # print(payload)
                response = requests.post(url1, headers=headers, data=payload)
                # print(response.json())
                assert response.json()['code'] == 200
                log.debug("删除立项项目成功")
        else:
            log.debug("没有可删除的立项项目")

    def lx_upload(self):
        """上传文件"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['上传文件']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        # 要上传的文件路径
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, 'Template.csv')
        if not os.path.exists(file_path):
            raise FileNotFoundError("测试文件%s不存在！" % file_path)

        # 打开文件，以二进制模式读取
        with open(file_path, 'rb') as f:
            files = {'file': f}  # 创建一个包含文件数据的字典
        # 发送POST请求，带上文件数据
            response = requests.post(url, files=files, headers=headers)
            #print(response.json())
            data = response.json()['data']
            uri = data['uri']
            filename = data['relativePathAndFileName']
            # print(uri)
            # print(filename)
            assert response.json()['code'] == 200
        log.debug("上传文件成功")
        # print(uri)
        # print(filename)
        return uri,filename
    def lx_save1(self, lx_id):
        """上传立项资料后，保存"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['保存文件']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}",
            'Content-Type': 'application/json'
        }
        #id = self.lx_create_project()  #项目id
        uri1,filename1 = self.lx_upload()  #上传文件名及存放路径
        uri2,filename2 = self.lx_upload()
        data = json.dumps({
	        "establishId": f"{lx_id}",
	        "filesList": [
		    {
			    "establishInfo": "立项建议书",
			    "fileName": f"{filename1}",
			    "fileUrl": f"{uri1}"
		    },
		    {
			    "establishInfo": "初步法律意见书",
			    "fileName": f"{filename2}",
			    "fileUrl": f"{uri2}"
		    }
	        ]
        })
        # print(data)
        # print(headers)
        response1 = requests.post(url, headers=headers, data=data)
        # print(response1.json())
        assert response1.json()['code'] == 200
        log.debug("立项资料保存成功")

    def lx_save2(self, lx_id):
        """保存项目评审和决策情况"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['保存立项项目评审和决策情况']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}",
            'Content-Type': 'application/json'
        }
        # 决策文件
        uri1, filename1 = self.lx_upload()  # 上传文件名及存放路径
        data = json.dumps({
            "establishId": f"{lx_id}",
            "decisionList": [
                {
                    "businessLink": "20",
                    "decisionDate": "2025-02-11",
                    "decisionUnit": "总部",
                    "decisionBody": "25",
                    "fileName": f"{filename1}",
                    "fileUrl": f"{uri1}"
                }
            ]
        })
        response = requests.post(url, data=data, headers=headers)
        assert response.json()['code'] == 200
        log.debug("项目评审和决策情况保存成功")
    def lx_submit(self, lx_id, project_name):
        """项目立项提交稽核"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['立项提交稽核']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}",
            'Content-Type': 'application/json'
        }
        data = json.dumps({
	        "processId": "1860967594442764290", #二级单位投资部项目立项审批流程
	        "businessId": f"{lx_id}",
	        "nodeUserList": [
		    {
			    "nodeId": "1860968025910816770",
			    "userId": 70557
		    },
		    {
			    "nodeId": "1860968025910816771",
			    "userId": 71048
		    }
	        ],
	    "businessType": 1,
        "businessData": {"data": {"projectName": f"{project_name}"}}
        })
        response = requests.post(url, data=data, headers=headers)
        assert response.json()['code'] == 200
        log.debug("立项提交稽核成功")


if __name__ == '__main__':
    l1 = LxGl() #实例方法需要通过类的实例来调用，而不是直接通过类。
    # id = l1.lx_create_project()
    l1.lx_search1('啦啦啦啦')
    l1.lx_search2('lxtb')
    # l1.lx_remove_project(1)
    # l1.lx_search()
    # l1.lx_info()
    # l1.lx_procode()
    #id = l1.lx_create_project()
    # l1.lx_save1(id)
    # l1.lx_save2(id)
    # l1.lx_submit(id)
    #l1.lx_jhlc()
    #批量造数据
    # for i in range(10):
    #     l1 = LxGl()
    #     lx_id, project_name = l1.lx_create_project()
    #     l1.lx_save1(lx_id)
    #     sleep(1)
    #     l1.lx_save2(lx_id)
    #     l1.lx_submit(lx_id, project_name)
    #     i+=1
