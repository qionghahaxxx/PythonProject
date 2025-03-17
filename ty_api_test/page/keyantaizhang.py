import json
# import sys
import urllib.parse
import requests
# from datetime import datetime,timedelta
from ty_api_test.common.logger import *
from ty_api_test.page.login_api import login
from ty_api_test.common.readconfig import *
from ty_api_test.common.readapi import *
# import time

class KyGl:
    """可研模块用例，封装相关api方法"""
    def __init__(self):
        self.authorization,self.userid = login()
    def ky_add_project(self,queryname):
        """添加可研项目"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        #查询项目名称，模糊查询
        api1 = Api('api')['立项完成的项目']
        url1 = f"https://{host}{api1}"
        projectname = urllib.parse.quote(queryname)  #对字符串进行url编码，解码用unquote()函数
        projectname1 = f"projectName={projectname}"
        url2 = '&'.join([url1,projectname1])
        #print(url2)
        response1 = requests.get(url2, headers=headers)
        #print(response1.json())
        data = response1.json()['data']
        datalist = data['list']
        num = data['endRow']
        if num>0:
            """立项完成的项目可能有多个，有些可能已经是可研填报状态，用for循环来遍历尝试，直到添加成功break"""
            for i in range(num):
                list_info = datalist[i]
                project_code = list_info['projectCode']
                id1 = list_info['id']
                projectname2 = list_info['projectName']
                #print(project_code)
                #print(id1)
                api2 = Api('api')['创建可研项目']
                url3 = f"https://{host}{api2}"
                headers1 = {
                    "Authorization": f"Bearer {authorization}",
                    "Content-Type": "application/json"
                }
                data1 = json.dumps({f"projectCode":f"{project_code}", "id": f"{id1}"})
                #print(data1)
                response2 = requests.post(url3, headers=headers1, data=data1)
                response_json = response2.json()
               # print(response_json)
               #  assert response_json['code'] == 200
                if response_json['code'] ==200:
                    data2 = response_json['data']
                    id2 = data2['id']
                    create_time1 = data2['createdTime']
                    project_id = data2['projectId']
                    # print(id2)
                    # print(create_time1)
                    print(projectname2)
                    log.debug('添加可研项目成功')
                    return id2, create_time1,projectname2,project_code,project_id
                else:
                    continue
            else: #注意这个else是和for循环相关联的,只有在循环没有被break打断时才会执行
                log.debug('暂时没有未填报的立项完成的测试项目')
                return None
        else:
            log.debug('暂时没有立项完成的测试项目')
            return None

    def ky_save1(self,id,createtime,projectname,projectcode,projectid):
        """保存可研基础信息"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        headers = {
            "Authorization": f"Bearer {authorization}",
            "Content-Type": "application/json"
        }

        # id,createtime = self.ky_add_project()
        # 获取当前时间
        now = datetime.datetime.now()

        # 将当前时间格式化为字符串
        updatedtime = now.strftime("%Y-%m-%d %H:%M:%S")
        api = Api('api')['保存可研基础信息']
        data = json.dumps({
            "addDetail": "四川省成都市龙泉驿区",
            "areaQuare": 10,
            "areaTypeCharacter": "17",
            "areaTypeId": "13",
            "businessTypeId": "6",
            "companyId": "0",
            "companyName": "总部",
            "countryId": "1",
            "createdBy": "曹孟",
            "createdTime": f"{createtime}",
            "currencyTypeId": "10",
            "designCapacity": 100,
            "feasibleStatus": "kytb",
            "id": f"{id}",
            "investContent": "投资内容测试",
            "investFixedAssets": 100,
            "latitude": "30.697316212381597",
            "lineConfig": "生产线配置测试",
            "longitude": "104.36250469936057",
            "projectCode": f"{projectcode}",
            "projectId": f"{projectid}",
            "projectName": f"{projectname}",
            "registeredCapital": 10000000,
            "updatedBy": "曹孟",
            "updatedTime": f"{updatedtime}",
            "provinceId": "",
            "cityId": "",
            "feasibleShareholders": [
                {
                    "shareholdersName": "测试股东",
                    "shareholdersAmount": "10000",
                    "shareholdersProportion": "100"
                }
            ],
            "dictMarketType": "",
            "projectType": "93",
            "feasibleAsset": {
                "id": "",
                "feasibleId": 0,
                "totalFlatProAmount": 10,
                "synthFlatProAmount": 10,
                "warapFlatProAmount": 10,
                "otherFlatProAmount": 0,
                "flatProAmount": 30,
                "produceEquipmentAmount": 10,
                "environmentEquipmentAmount": 0,
                "experimentEquipmentAmount": 10,
                "rearEquipmentAmount": 0,
                "otherEquipmentAmount": 10,
                "equipmentAmount": 30,
                "proServerAmount": 10,
                "landPurAmount": 10,
                "basicPreparAmount": 10,
                "increasePreparAmount": 10,
                "preparAmount": 20,
                "totalAmount": 100
            }
        }
        )
        url = f"https://{host}{api}"
        response = requests.post(url, headers=headers, data=data)
        # print(response.json())
        assert response.json()['code'] == 200
        log.debug('可研填报-基础信息保存成功')
        # return id
    def ky_upload(self):
        """上传文件"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['上传文件']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        # 要上传的文件路径
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(BASE_DIR, 'Template.csv')
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
    def ky_save2(self,id):
        """保存可研资料"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['保存可研资料']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}",
            "Content-Type": "application/json"
        }
        #id = self.ky_save1() #先保存基础信息
        fileurl1,filename1 = self.ky_upload()
        data = json.dumps({
            "feasibleId": f"{id}",
            "fileList": [
                {
                    "dictId": "37",
                    "remake": "可研资料备注测试",
                    "fileName": f"{filename1}",
                    "fileUrl": f"{fileurl1}"
                }
            ]
        })
        response = requests.post(url, headers=headers, data=data)
        # print(response.json())
        assert response.json()['code'] == 200
        log.debug('可研填报-可研资料保存成功')
        #return id
    def ky_save3(self,id):
        """保存实施计划"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['保存实施计划']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}",
            "Content-Type": "application/json"
        }
        #id = self.ky_save2()  # 先保存基础信息,保存可研资料
        now = datetime.datetime.now()
        date1 = now + timedelta(weeks=1)
        plandate = date1.strftime("%Y-%m-%d")
        data = json.dumps([
            {
                "dictId": "63",
                "planDate": f"{plandate}",
                "feasibleId": f"{id}"
            },
            {
                "dictId": "70",
                "planDate": f"{plandate}",
                "feasibleId": f"{id}"
            }
        ])
        response = requests.post(url, data, headers=headers)
        # print(response.json())
        assert response.json()['code'] == 200
        logging.debug('可研填报-实施计划保存成功')
        #return id
    def ky_save4(self,id):
        """保存手续办理计划"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['保存手续办理计划']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}",
            "Content-Type": "application/json"
        }
        #id1 = self.ky_save3()
        now = datetime.datetime.now()
        date1 = now + timedelta(weeks=1)
        plandate = date1.strftime("%Y-%m-%d")
        data = json.dumps([
            {
                "dictId": "76",
                "planDate": f"{plandate}",
                "remake": "手续备注测试1",
                "feasibleId": f"{id}"
            },
            {
                "dictId": "88",
                "planDate": f"{plandate}",
                "remake": "手续备注测试2",
                "feasibleId": f"{id}"
            }
        ])
        response = requests.post(url, data, headers=headers)
        # print(response.json())
        assert response.json()['code'] == 200
        log.debug('可研填报-手续办理计划保存成功')
        #return id1

    def ky_save5(self,id):
        """保存经济测算表"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['保存财务评价指标']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}",
            "Content-Type": "application/json"
        }
        #id1 = self.ky_save4()
        data = json.dumps({
            "economic": {
                "id": 0,
                "feasibleId": f"{id}",
                "nePresentValue": "100",
                "internalRate": "20",
                "investRate": "20",
                "investCycle": "3",
                "totalProfitAmount": "200",
                "profitAmount": "100",
                "profitAmountRate": "15",
                "economicCycle": "5",
                "createdBy": 0,
                "createdById": 0,
                "createdTime": 0,
                "updateById": 0,
                "updatedBy": 0,
                "updatedTime": 0
            },
            "profitList": [
            ],
            "netValueList": [
            ],
            "capitalList": [
            ]
        })
        response1 = requests.post(url, data, headers=headers)
        # print(response1.json())
        assert response1.json()['code'] == 200
        log.debug('财务评价指标保存成功')
        api1 = Api('api')['保存经济测算表']
        url1 = f"https://{host}{api1}"
        data1 = json.dumps({"feasibleId":f"{id}","decisionList":[]})
        response2 = requests.post(url1, data1, headers=headers)
        # print(response2.json())
        assert response2.json()['code'] == 200
        log.debug('可研填报-经济测算表保存成功')
        #return id1

    def ky_save6(self,id):
        """保存可研项目评审和决策情况"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['保存可研项目评审和决策情况']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}",
            "Content-Type": "application/json"
        }
        #id1 = self.ky_save5()
        now = datetime.datetime.now()
        date1 = now + timedelta(weeks=1)
        date2 = date1.strftime("%Y-%m-%d")

        data = json.dumps({
            "feasibleId": f"{id}",
            "decisionList": [
                {
                    "decisionDate": f"{date2}",
                    "businessName": "项目批复情况",
                    "file": [
                    ],
                    "fileName": "",
                    "fileUrl": ""
                },
                {
                    "businessLink": "20",
                    "businessName": "20",
                    "decisionDate": f"{date2}",
                    "decisionUnit": "中建西部建设",
                    "decisionBody": "24",
                    "fileName": "",
                    "fileUrl": ""
                }
            ]
        })
        response = requests.post(url, data, headers=headers)
        # print(response.json())
        assert response.json()['code'] == 200
        log.debug('可研填报-可研项目评审和决策情况保存成功')
        #return id1

    def ky_save7(self,id,projectname):
        """可研提交稽核"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['可研提交稽核']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}",
            "Content-Type": "application/json"
        }

        data = json.dumps({
            "processId": "1860967594641265369",
            "businessId": f"{id}",
            "nodeUserList": [
                {
                    "nodeId": "1860968026910912252",
                    "userId": 70557
                },
                {
                    "nodeId": "1860968026910912253",
                    "userId": 71048
                }
            ],
            "businessType": 2,
            "instanceStatus": "PENDING",
            "businessData": {"data": {"projectName": f"{projectname}"}}
        })
        response = requests.post(url, data=data, headers=headers)
        assert response.json()['code'] == 200
        log.debug("可研提交稽核成功")

ky = Kytz()
if __name__ == '__main__':
    for i in range(6):           #批量造数据
        result = ky.ky_add_project('测试')
        if result is not None:
            id1, createtime, projectname, projectcode, projectid= result
            ky.ky_save1(id1, createtime,projectname,projectcode,projectid)
            ky.ky_save2(id1)
            ky.ky_save3(id1)
            ky.ky_save4(id1)
            ky.ky_save5(id1)
            ky.ky_save6(id1)
            ky.ky_save7(id1, projectname)
        i+=1
    #ky.ky_add_project()
