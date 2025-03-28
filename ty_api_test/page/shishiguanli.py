from ty_api_test.common.logger import *
from ty_api_test.page.login_api import login
from ty_api_test.common.readconfig import *
from ty_api_test.common.readapi import *
import urllib.parse
import requests
import json
from datetime import datetime, timedelta

# 类名使用大驼峰命名法，每个单词首字母大写；函数、变量名使用使用小写字母+下划线
class SsGl:
    """实施许可令管理模块用例，相关api方法封装"""
    def __init__(self):
        self.authorization,self.userid = login()
    def ss_upload(self):
        """上传文件"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['上传文件']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        # 要上传的文件路径
        BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(BASEDIR, 'Template.csv')
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
            assert response.status_code == 200
        log.debug("上传文件成功")
        # print(uri)
        # print(filename)
        return uri,filename
    def ss_add_permit(self, query_name):
        """新增实施许可令，提交稽核"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        # 1.查询项目名称，模糊查询
        api1 = Api('api')['可研完成的项目']
        url1 = f"https://{host}{api1}"
        projectname = urllib.parse.quote(query_name)  # 对字符串进行url编码，解码用unquote()函数
        projectname1 = f"projectName={projectname}"
        url2 = '&'.join([url1, projectname1])
        # print(url2)
        response1 = requests.get(url2, headers=headers)
        print(response1.json())
        data = response1.json()['data']
        data_list = data['list']
        num = data['endRow']
        if num > 0:
            """可研完成的项目可能有多个，有些可能已经是提交稽核，用for循环来遍历尝试，直到添加成功break"""
            for i in range(num):
                # 2.查询实施许可令详情
                list_info = data_list[i]
                project_id = list_info['projectId']
                api2 = Api('api')['实施许可令详情']
                url3 = f"https://{host}{api2}"
                url_ss = '?'.join([url3, f'projectId={project_id}'])
                # print(url_ss)
                response2 = requests.get(url_ss, headers=headers)
                response_json = response2.json()
                list_info1 = response_json['data']
                # print(list_info1)
                if "implStatus" not in list_info1:
                    """3.1从无到有新增实施许可令"""
                    api3 = Api('api')['添加实施许可令']
                    url4 = f"https://{host}{api3}"
                    uri, filename = self.ss_upload()
                    data1 = json.dumps({
                        "id": "",
                        "projectId": f"{project_id}",
                        "implStatus": "tb",
                        "files": [
                            {
                                "dictId": "100",
                                "fileUrl": f"{uri}",
                                "fileName": f"{filename}"
                            }
                        ]
                    })
                    headers1 = {
                        "Authorization": f"Bearer {authorization}",
                        "Content-Type": "application/json"
                    }
                    response3 = requests.post(url4, data=data1, headers=headers1)
                    print(response3.json())
                    data2 = response3.json()['data']
                    #4.1提交稽核
                    api4 = Api('api')['实施提交稽核']
                    url5 = f"https://{host}{api4}"
                    data3 = json.dumps({
                        "processId": "1871457740242022401",
                        "businessId": f"{data2['implLicenseId']}",
                        "nodeUserList": [
                            {
                                "nodeId": "1871458261166170114",
                                "userId": 70557
                            },
                            {
                                "nodeId": "1871458457493053441",
                                "userId": 71048
                            }
                        ],
                        "businessType": 3,
                        "businessData": {
                            "data": {
                                "projectName": f"{data2['projectName']}",
                                "projectId": f"{project_id}"
                            }
                        }
                    })
                    response4 = requests.post(url5, data=data3, headers=headers1)
                    print(response4.json())
                    assert response4.json()['code'] == 200
                    log.debug("实施许可令稽核提交成功")
                    break
                elif list_info1['implStatus'] == 'tb':
                    """3.2编辑填报状态的实施许可令"""
                    api4 = Api('api')['更新实施许可令']
                    url6 = f"https://{host}{api4}"
                    uri, filename = self.ss_upload()
                    id1 = list_info1['licenseFilesList'][0]['id']
                    data4 = json.dumps({
                        "implLicenseId": f"{project_id}",
                        "addFilesList": [
                        ],
                        "updateFileList": [
                            {
                                "createdBy": "caomeng",
                                "createdById": 68506,
                                "dictId": "100",
                                "fileName": f"{filename}",
                                "fileUrl": f"{uri}",
                                "id": f"{id1}",
                                "implLicenseId": f"{list_info1['licenseFilesList'][0]['implLicenseId']}"
                            }
                        ],
                        "deleteFilesIds": [
                        ]
                    })
                    headers2 = {
                        "Authorization": f"Bearer {authorization}",
                        "Content-Type": "application/json"
                    }
                    response5 = requests.post(url6, data=data4, headers=headers2)
                    print(response5.json())
                    projectname2 = response5.json()['data']['projectName']
                    #保存成功后，需要删除先前的文件，当前只允许保留1份附件文件
                    api_del = Api('api')['删除文件']
                    filename1 = list_info1['licenseFilesList'][0]['fileName']
                    filename2 = urllib.parse.quote(filename1)  # 对中文进行url编码
                    api_del1 = '?'.join([api_del, f'fileName={filename2}'])
                    url_del = f"https://{host}{api_del1}"
                    print(url_del)
                    response6 = requests.post(url_del, headers=headers2)
                    print(response6.json())
                    #4.2 提交稽核
                    api5 = Api('api')['实施提交稽核']
                    url7 = f"https://{host}{api5}"
                    data5 = json.dumps({
                        "processId": "1871457740242022401",
                        "businessId": f"{list_info1['licenseFilesList'][0]['implLicenseId']}",
                        "nodeUserList": [
                            {
                                "nodeId": "1871458261166170114",
                                "userId": 70557
                            },
                            {
                                "nodeId": "1871458457493053441",
                                "userId": 71048
                            }
                        ],
                        "businessType": 3,
                        "businessData": {
                            "data": {
                                "projectName": f"{projectname2}",
                                "projectId": f"{project_id}"
                            }
                        }
                    })
                    response6 = requests.post(url7, data=data5, headers=headers2)
                    print(response6.json())
                    assert response6.json()['code'] == 200
                    log.debug("实施许可令稽核提交成功")
                    break
                else:
                    # log.debug(f"第{i+1}个项目已处于实施稽核流程中，跳过")
                    continue
            else:
                # 如果循环没有通过break退出，则执行else子句
                log.debug("没有可研完成且尚未提交实施稽核的项目")
        else:
            log.debug("没有可研完成的项目")
    def ss_project_company(self, query_name):
            """更新项目公司，提交稽核"""
            # 1.查询项目名称，模糊查询
            authorization = self.authorization
            host = Readconfig('HOST-TZB').host
            headers = {
                "Authorization": f"Bearer {authorization}"
            }
            api1 = Api('api')['可研完成的项目']
            url1 = f"https://{host}{api1}"
            projectname = urllib.parse.quote(query_name)
            projectname1 = f"projectName={projectname}"
            url2 = '&'.join([url1, projectname1])
            response1 = requests.get(url2, headers=headers)
            # print(response1.json())
            response_data1 = response1.json()['data']
            data_list1 = response_data1['list']
            num = response_data1['endRow']
            if num > 0:
                """可研完成的项目可能有多个，有些可能已经是提交稽核，用for循环来遍历尝试，直到添加成功break"""
                for i in range(num):
                    # 2.查询项目详情
                    list_info = data_list1[i]
                    project_id = list_info['projectId']
                    api2 = Api('api')['项目公司详情']
                    url3 = f"https://{host}{api2}"
                    url_ss = '?'.join([url3, f'projectId={project_id}'])
                    response2 = requests.get(url_ss, headers=headers)
                    response_json = response2.json()
                    # print(response_json)
                    response_data2 = response_json['data']
                    # 3.添加项目公司/暂存
                    if 'implCompanyStatus' not in response_data2 :
                        """3.1 新项目，不处于填报状态"""
                        api3 = Api('api')['添加项目公司']
                        url4 = f"https://{host}{api3}"
                        uri, filename = self.ss_upload()
                        data1 = json.dumps({
                            "projectCompanyName": "测试项目公司",
                            "projectId": f"{project_id}",
                            "implCompanyStatus": "tb",
                            "companyFiles": [
                                {
                                    "dictId": "105",
                                    "file": [
                                    ],
                                    "fileName": f"{filename}",
                                    "fileUrl": f"{uri}"
                                }
                            ]
                        })
                        headers1 = {
                            "Authorization": f"Bearer {authorization}",
                            "Content-Type": "application/json"
                        }
                        response3 = requests.post(url4, data=data1, headers=headers1)
                        # print(response3.json())
                        response_data3 = response3.json()['data']
                        projectname2 = response_data3['projectName']

                        # 4.1提交稽核
                        api4 = Api('api')['项目公司提交稽核']
                        url5 = f"https://{host}{api4}"
                        data2 = json.dumps({
                            "processId": "1889227480372482048",
                            "businessId": f"{response_data3['id']}",
                            "nodeUserList": [
                                {
                                    "nodeId": "1889118550821777409",
                                    "userId": 70557
                                },
                                {
                                    "nodeId": "1889228550821777409",
                                    "userId": 71048
                                }
                            ],
                            "businessType": 4,
                            "businessData": {
                                "data": {
                                    "projectName": f"{projectname2}",
                                    "projectId": f"{project_id}"
                                }
                            }
                        })
                        response4 = requests.post(url5, data=data2, headers=headers1)
                        # print(response4.json())
                        assert response4.json()['code'] == 200
                        log.debug("项目公司稽核提交成功")
                        break
                    elif response_data2['implCompanyStatus'] == 'tb':
                        """3.2 项目当前已处于填报状态，走编辑逻辑"""
                        api5 = Api('api')['更新项目公司']
                        url6 = f"https://{host}{api5}"
                        uri, filename = self.ss_upload()
                        filelist = response_data2['filesList']
                        # create_time = filelist[0]['createdTime']  #有些数据没有createdTime
                        id1 = response_data2['id']
                        id2 = filelist[0]['id']
                        if 'createdTime' in filelist[0]:
                            create_time = filelist[0]['createdTime']
                            data3 = json.dumps({
                                "id": f"{id1}",
                                "projectCompanyName": f"{response_data2['projectCompanyName']}",
                                "addFilesList": [
                                ],
                                "updateFilesList": [
                                    {
                                        "createdBy": "曹孟",
                                        "createdById": 68506,
                                        "createdTime": f"{create_time}",
                                        "dictId": "105",
                                        "fileName": f"{filename}",
                                        "fileUrl": f"{uri}",
                                        "id": f"{id2}",
                                        "implCompanyId": f"{filelist[0]['implCompanyId']}",
                                        "updateById": 68506,
                                        "updatedBy": "曹孟"
                                    }
                                ],
                                "deleteFilesIds": [
                                ]
                            })
                        else:
                            data3 = json.dumps({
                                "id": f"{id1}",
                                "projectCompanyName": f"{response_data2['projectCompanyName']}",
                                "addFilesList": [
                                ],
                                "updateFilesList": [
                                    {
                                        "createdBy": "曹孟",
                                        "createdById": 68506,
                                        "dictId": "105",
                                        "fileName": f"{filename}",
                                        "fileUrl": f"{uri}",
                                        "id": f"{id2}",
                                        "implCompanyId": f"{filelist[0]['implCompanyId']}",
                                        "updateById": 68506,
                                        "updatedBy": "曹孟"
                                    }
                                ],
                                "deleteFilesIds": [
                                ]
                            })

                        headers2 = {
                            "Authorization": f"Bearer {authorization}",
                            "Content-Type": "application/json"
                        }
                        response5 = requests.post(url6, data=data3, headers=headers2)
                        # print(response5.json())
                        projectname3 = response5.json()['data']['projectName']
                        # 保存成功后，需要删除先前的文件，当前只允许保留1份附件文件
                        api_del = Api('api')['删除文件']
                        filename1 = response_data2['filesList'][0]['fileName']
                        filename2 = urllib.parse.quote(filename1)  # 对中文进行url编码
                        api_del1 = '?'.join([api_del, f'fileName={filename2}'])
                        url_del = f"https://{host}{api_del1}"
                        # print(url_del)
                        response6 = requests.post(url_del, headers=headers2)
                        print(response6.json())
                        #4.2 提交稽核
                        api6 = Api('api')['项目公司提交稽核']
                        url7 = f"https://{host}{api6}"
                        data3 = json.dumps({
                            "processId": "1889227480372482048",
                            "businessId": f"{id1}",
                            "nodeUserList": [
                                {
                                    "nodeId": "1889118550821777409",
                                    "userId": 70557
                                },
                                {
                                    "nodeId": "1889228550821777409",
                                    "userId": 71048
                                }
                            ],
                            "businessType": 4,
                            "businessData": {
                                "data": {
                                    "projectName": f"{projectname3}",
                                    "projectId": f"{project_id}"
                                }
                            }
                        })
                        response7 = requests.post(url7, data=data3, headers=headers2)
                        # print(response7.json())
                        assert response7.json()['code'] == 200
                        log.debug("项目公司稽核提交成功")
                        break
                    else:
                        # log.debug(f"第{i+1}个项目已处于项目公司稽核流程中，跳过")
                        continue
                else:
                    # 如果循环没有通过break退出，则执行else子句
                    log.debug("没有可研完成的项目")
    def ss_project_contract(self, query_name):
            """更新项目招投标及合同文件，提交稽核"""
            # 1.查询项目名称，模糊查询
            authorization = self.authorization
            host = Readconfig('HOST-TZB').host
            headers = {
                "Authorization": f"Bearer {authorization}"
            }
            api1 = Api('api')['可研完成的项目']
            url1 = f"https://{host}{api1}"
            projectname = urllib.parse.quote(query_name)
            projectname1 = f"projectName={projectname}"
            url2 = '&'.join([url1, projectname1])
            response1 = requests.get(url2, headers=headers)
            print(response1.json())
            response_data1 = response1.json()['data']
            data_list1 = response_data1['list']
            num = response_data1['endRow']
            if num > 0:
                """可研完成的项目可能有多个，有些可能已经是提交稽核，用for循环来遍历尝试，直到添加成功break"""
                for i in range(num):
                    # 2.查询项目招投标及合同文件详情
                    list_info = data_list1[i]
                    project_id = list_info['projectId']
                    api2 = Api('api')['项目招投标及合同文件详情']
                    url3 = f"https://{host}{api2}"
                    url_ss = '?'.join([url3, f'projectId={project_id}'])
                    response2 = requests.get(url_ss, headers=headers)
                    response_json = response2.json()
                    # print(response_json)
                    response_data2 = response_json['data']
                    if "implContractStatus" not in response_data2[0] :
                        # 3.1添加项目招投标及合同文件，走新增逻辑
                        api3 = Api('api')['添加项目招投标及合同文件']
                        url4 = f"https://{host}{api3}"
                        uri, filename = self.ss_upload()
                        data1 = json.dumps({
                            "projectId": f"{project_id}",
                            "contractInfos": [
                                {
                                    "businessType": "121",
                                    "budgetAmount": "100",
                                    "actualAmount": "100",
                                    "fileUrl": f"{uri}",
                                    "fileName": f"{filename}",
                                    "implContractStatus": "tb"
                                }
                            ]
                        })
                        headers1 = {
                            "Authorization": f"Bearer {authorization}",
                            "Content-Type": "application/json"
                        }
                        response3 = requests.post(url4, data=data1, headers=headers1)
                        print(response3.json())
                        response_data3 = response3.json()['data']
                        projectname2 = response_data3['projectName']
                        # 4.1提交稽核
                        api4 = Api('api')['项目招投标及合同文件提交稽核']
                        url5 = f"https://{host}{api4}"
                        data2 = json.dumps({
                            "processId": "1889488130877296640",
                            "businessId": f"{project_id}",
                            "nodeUserList": [
                                {
                                    "nodeId": "1889488577105104896",
                                    "userId": 70557
                                },
                                {
                                    "nodeId": "1889488577105104897",
                                    "userId": 71048
                                }
                            ],
                            "businessType": 5,
                            "businessData": {
                                "data": {
                                    "projectName": f"{projectname2}",
                                    "projectId": f"{project_id}"
                                }
                            }
                        })
                        response4 = requests.post(url5, data=data2, headers=headers1)
                        print(response4.json())
                        assert response4.json()['code'] == 200
                        log.debug(f"{projectname2}项目招投标及合同文件提交稽核成功")
                        break
                    elif response_data2[0]['implContractStatus'] == 'tb':
                        """如果是填报状态，走编辑逻辑"""
                        api5 = Api('api')['添加项目招投标及合同文件']
                        url6 = f"https://{host}{api5}"
                        uri, filename = self.ss_upload()
                        create_time = response_data2[0]['createdTime']
                        update_time = response_data2[0]['updatedTime']

                        id1 = response_data2[0]['id']
                        data2 = json.dumps({
                            "projectId": f"{project_id}",
                            "contractInfos": [
                                {
                                    "actualAmount": 1000,
                                    "budgetAmount": 1000,
                                    "businessType": "121",
                                    "createdBy": "曹孟",
                                    "createdById": 68506,
                                    "createdTime": f"{create_time}",
                                    "fileName": f"{filename}",
                                    "fileUrl": f"{uri}",
                                    "id": f"{id1}",
                                    "implContractStatus": "tb",
                                    "projectId": f"{project_id}",
                                    "updateById": 68506,
                                    "updatedBy": "曹孟",
                                    "updatedTime": f"{update_time}"
                                }
                            ]
                        },ensure_ascii=False)
                        headers2 = {
                            "Authorization": f"Bearer {authorization}",
                            "Content-Type": "application/json"
                        }
                        response5 = requests.post(url6, data=data2, headers=headers2)
                        # print('走编辑逻辑')
                        print(response5.json())
                        response_data4 = response5.json()['data']
                        projectname3 = response_data4['projectName']
                        # 保存成功后，需要删除先前的文件，当前只允许保留1份附件文件
                        api_del = Api('api')['删除文件']
                        filename1 = response_data2[0]['fileName']
                        filename2 = urllib.parse.quote(filename1)  # 对中文进行url编码
                        api_del1 = '?'.join([api_del, f'fileName={filename2}'])
                        url_del = f"https://{host}{api_del1}"
                        response6 = requests.post(url_del, headers=headers2)
                        print(response6.json())
                        #4.2 提交稽核
                        api6 = Api('api')['项目招投标及合同文件提交稽核']
                        url7 = f"https://{host}{api6}"
                        data3 = json.dumps({
                            "processId": "1889488130877296640",
                            "businessId": f"{project_id}",
                            "nodeUserList": [
                                {
                                    "nodeId": "1889488577105104896",
                                    "userId": 70557
                                },
                                {
                                    "nodeId": "1889488577105104897",
                                    "userId": 71048
                                }
                            ],
                            "businessType": 5,
                            "businessData": {
                                "data": {
                                    "projectName": f"{projectname3}",
                                    "projectId": f"{project_id}"
                                }
                            }
                        })
                        response6 = requests.post(url7, data=data3, headers=headers2)
                        assert response6.json()['code'] == 200
                        log.debug(f"{projectname3}项目招投标及合同文件提交稽核成功")
                        break
                    else:
                        # log.debug(f"第{i+1}个项目已处于项目招投标及合同文件流程中，跳过")
                        continue
                else:
                    # 如果循环没有通过break退出，则执行else子句
                    log.debug("没有可研完成且尚未提交稽核的项目")
            else:
                log.debug("没有可研完成的项目")

    def ss_project_built(self, query_name):
        """更新项目建设（实施）进度，提交稽核"""
        # 1.查询项目名称，模糊查询
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        api1 = Api('api')['可研完成的项目']
        url1 = f"https://{host}{api1}"
        projectname = urllib.parse.quote(query_name)
        projectname1 = f"projectName={projectname}"
        url2 = '&'.join([url1, projectname1])
        response1 = requests.get(url2, headers=headers)
        # print(response1.json())
        response_data1 = response1.json()['data']
        data_list1 = response_data1['list']
        num = response_data1['endRow']
        if num > 0:
            """可研完成的项目可能有多个，有些可能已经是提交稽核，用for循环来遍历尝试，直到添加成功break"""
            for i in range(num):
                # 2.查询项目建设实施进度详情
                list_info = data_list1[i]
                project_id = list_info['projectId']
                api2 = Api('api')['项目建设实施进度详情']
                url3 = f"https://{host}{api2}"
                url_ss = '?'.join([url3, f'projectId={project_id}'])
                response2 = requests.get(url_ss, headers=headers)
                response_json = response2.json()
                response_data2 = response_json['data']
                plan_date = response_data2[0]['planDate']
                # 转换为datetime对象
                original_date = datetime.strptime(plan_date, '%Y-%m-%d')
                actual_date = original_date + timedelta(days=7)
                # 将actual_date转换为字符串
                actual_date = actual_date.strftime("%Y-%m-%d")

                feasible_plan_id1 = response_data2[0]['feasiblePlanId']
                feasible_plan_id2 = response_data2[1]['feasiblePlanId']
                if 'implProgressStatus' not in response_data2[0] :
                    """3.1无更新状态，保存项目建设实施进度"""
                    api3 = Api('api')['保存项目建设实施进度']
                    url4 = f"https://{host}{api3}"
                    data1 = json.dumps({
                        "projectId": f"{project_id}",
                        "detailList": [
                            {
                                "dictId": 63,
                                "dictName": "施工许可",
                                "feasiblePlanId": f"{feasible_plan_id1}",
                                "planDate": f"{plan_date}",
                                "implProgressStatus": "tb",
                                "actualProgressDate": f"{actual_date}",
                                "actualProgressDesc": "测试建设实施进度节点1"
                            },
                            {
                                "dictId": 70,
                                "dictName": "正式投产",
                                "feasiblePlanId": f"{feasible_plan_id2}",
                                "planDate": f"{plan_date}",
                                "actualProgressDate": f"{actual_date}",
                                "actualProgressDesc": "测试建设实施进度节点2"
                            }
                        ]
                    })
                    header2 = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {authorization}"
                    }
                    response3 = requests.post(url4, data=data1, headers=header2)
                    print(response3.json())
                    projectname2 = response3.json()['data']['projectName']
                    # 4.1 提交稽核
                    api4 = Api('api')['项目建设实施进度提交稽核']
                    url5 = f"https://{host}{api4}"
                    data2 = json.dumps({
                        "processId": "1889599825780019200",
                        "businessId": f"{project_id}",
                        "nodeUserList": [
                            {
                                "nodeId": "1889599825780019201",
                                "userId": 70557
                            },
                            {
                                "nodeId": "1889599825780019202",
                                "userId": 71048
                            }
                        ],
                        "businessType": 6,
                        "businessData": {
                            "data": {
                                "projectName": f"{projectname2}",
                                "projectId": f"{project_id}"
                            }
                        }
                    })
                    headers2 = {
                        "Authorization": f"Bearer {authorization}",
                        "Content-Type": "application/json"
                    }
                    response4 = requests.post(url5, data=data2, headers=headers2)
                    print(response4.json())
                    assert response4.json()['code'] == 200
                    log.debug(f'{projectname2}项目建设实施进度提交稽核成功')
                    break
                elif response_data2[0]['implProgressStatus'] == 'tb':
                    """3.2 更新状态为填报状态，已保存有数据"""
                    api3 = Api('api')['保存项目建设实施进度']
                    url4 = f"https://{host}{api3}"
                    create_time = response_data2[0]['createdTime']
                    update_time = response_data2[0]['updatedTime']
                    id1 = response_data2[0]['id']
                    id2 = response_data2[1]['id']
                    data2 = json.dumps({
                        "projectId": f"{project_id}",
                        "detailList": [
                            {
                                "actualProgressDate": f"{actual_date}",
                                "actualProgressDesc": "测试建设实施进度节点1",
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "dictId": 63,
                                "dictName": "施工许可",
                                "feasiblePlanId": f"{feasible_plan_id1}",
                                "id": f"{id1}",
                                "implProgressStatus": "tb",
                                "planDate": f"{plan_date}",
                                "projectId": f"{project_id}",
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}"
                            },
                            {
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "dictId": 70,
                                "dictName": "正式投产",
                                "feasiblePlanId": f"{feasible_plan_id2}",
                                "id": f"{id2}",
                                "implProgressStatus": "tb",
                                "planDate": f"{plan_date}",
                                "projectId": f"{project_id}",
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "actualProgressDate": f"{actual_date}",
                                "actualProgressDesc": "测试建设实施进度节点2"
                            }
                        ]
                    })
                    header2 = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {authorization}"
                    }
                    response3 = requests.post(url4, data=data2, headers=header2)
                    print(response3.json())
                    projectname2 = response3.json()['data']['projectName']
                    #4.2 提交稽核
                    api4 = Api('api')['项目建设实施进度提交稽核']
                    url5 = f"https://{host}{api4}"
                    data3 = json.dumps({
                        "processId": "1889599825780019200",
                        "businessId": f"{project_id}",
                        "nodeUserList": [
                            {
                                "nodeId": "1889599825780019201",
                                "userId": 70557
                            },
                            {
                                "nodeId": "1889599825780019202",
                                "userId": 71048
                            }
                        ],
                        "businessType": 6,
                        "businessData": {
                            "data": {
                                "projectName": f"{projectname2}",
                                "projectId": f"{project_id}"
                            }
                        }
                    })
                    response4 = requests.post(url5, data=data3, headers=header2)
                    print(response4.json())
                    assert response4.json()['code'] == 200
                    log.debug(f'{projectname2}项目建设实施进度提交稽核成功')
                    break
                else:
                    log.debug(f"第{i + 1}个项目已处于项目建设实施进度流程中，跳过")
                    continue
            else:
                log.debug("没有可研完成且尚未提交稽核的项目")
        else:
            log.debug("没有可研完成的项目")
    def ss_project_procedure(self, query_name):
        """更新项目合规性手续办理，提交稽核"""
        # 1.查询项目名称，模糊查询
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        api1 = Api('api')['可研完成的项目']
        url1 = f"https://{host}{api1}"
        projectname = urllib.parse.quote(query_name)
        projectname1 = f"projectName={projectname}"
        url2 = '&'.join([url1, projectname1])
        response1 = requests.get(url2, headers=headers)
        print(response1.json())
        response_data1 = response1.json()['data']
        data_list1 = response_data1['list']
        num = response_data1['endRow']
        if num > 0:
            """可研完成的项目可能有多个，有些可能已经是提交稽核，用for循环来遍历尝试，直到添加成功break"""
            for i in range(num):
                # 2.查询项目合规性手续详情详情
                list_info = data_list1[i]
                project_id = list_info['projectId']
                api2 = Api('api')['项目合规性手续详情']
                url3 = f"https://{host}{api2}"
                url_ss = '?'.join([url3, f'projectId={project_id}'])
                response2 = requests.get(url_ss, headers=headers)
                response_json = response2.json()
                # print(response_json)
                response_data2 = response_json['data']
                plan_date = response_data2[0]['planDate']
                original_date = datetime.strptime(plan_date, '%Y-%m-%d')  # 将字符串转换为日期对象
                actual_date = original_date + timedelta(days=7)
                actual_date = actual_date.strftime('%Y-%m-%d')  # 将日期对象转换为字符串
                feasible_compliance_id1 = response_data2[0]['feasibleComplianceId']
                feasible_compliance_id2 = response_data2[1]['feasibleComplianceId']
                if 'implComplianceStatus' not in response_data2[0] :
                    # 3.1 无更新状态，保存项目合规性手续

                    api3 = Api('api')['保存项目合规性手续']
                    url4 = f"https://{host}{api3}"
                    uri, filename = self.ss_upload()
                    data1 = json.dumps({
                        "projectId": f"{project_id}",
                        "detailList": [
                            {
                                "dictId": 76,
                                "dictName": "立项备案登记",
                                "feasibleComplianceId": f"{feasible_compliance_id1}",
                                "planDate": f"{plan_date}",
                                "remake": "手续备注测试1",
                                "implComplianceStatus": "tb",
                                "actualProgressDate": f"{actual_date}",
                                "fileName": f"{filename}",
                                "fileUrl": f"{uri}"
                            },
                            {
                                "dictId": 88,
                                "dictName": "生产资质",
                                "feasibleComplianceId": f"{feasible_compliance_id2}",
                                "planDate": f"{plan_date}",
                                "remake": "手续备注测试2",
                                "implComplianceStatus": "tb",
                                "actualProgressDate": f"{actual_date}"
                            }
                        ]
                    })
                    headers1 = {
                        "Authorization": f"Bearer {authorization}",
                        "Content-Type": "application/json"
                    }
                    response3 = requests.post(url4, data=data1, headers=headers1)
                    # print(response3.json())
                    response_data2 = response3.json()['data']
                    projectname2 = response_data2['projectName']
                    # 4.1 项目合规性手续提交稽核
                    api4 = Api('api')['项目合规性手续提交稽核']
                    url5 = f"https://{host}{api4}"
                    data2 = json.dumps({
                        "processId": "1889950321795534848",
                        "businessId": f"{project_id}",
                        "nodeUserList": [
                            {
                                "nodeId": "1889950321795534849",
                                "userId": 70557
                            },
                            {
                                "nodeId": "1889950321795534850",
                                "userId": 71048
                            }
                        ],
                        "businessType": 7,
                        "businessData": {
                            "data": {
                                "projectName": f"{projectname2}",
                                "projectId": f"{project_id}"
                            }
                        }
                    })
                    headers2 = {
                        "Authorization": f"Bearer {authorization}",
                        "Content-Type": "application/json"
                    }
                    response4 = requests.post(url5, data=data2, headers=headers2)
                    response_data3 = response4.json()
                    assert response_data3['code'] == 200
                    log.debug(f"{projectname2}项目合规性手续提交稽核成功")
                    break
                elif response_data2[0]['implComplianceStatus'] == 'tb':
                    """3.2 更新状态为填报状态，走编辑逻辑"""
                    api3 = Api('api')['保存项目合规性手续']
                    url4 = f"https://{host}{api3}"
                    uri, filename = self.ss_upload()
                    #上传文件成功后，删除原文件
                    api_del = Api('api')['删除文件']
                    filename1 = response_data2[0]['fileName']
                    filename2 = urllib.parse.quote(filename1)  # 对中文进行url编码
                    api_del1 = '?'.join([api_del, f'fileName={filename2}'])
                    url_del = f"https://{host}{api_del1}"
                    headers1 = {
                        "Authorization": f"Bearer {authorization}",
                        "Content-Type": "application/json"
                    }
                    response6 = requests.post(url_del, headers=headers1)
                    print(response6.json())

                    create_time = response_data2[0]['createdTime']
                    update_time = response_data2[0]['updatedTime']
                    id1 = response_data2[0]['id']
                    id2 = response_data2[1]['id']

                    data1 = json.dumps({
                        "projectId": f"{project_id}",
                        "detailList": [
                            {
                                "actualProgressDate": f"{actual_date}",
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "dictId": 76,
                                "dictName": "立项备案登记",
                                "feasibleComplianceId": f"{feasible_compliance_id1}",
                                "fileName": f"{filename}",
                                "fileUrl": f"{uri}",
                                "id": f"{id1}",
                                "implComplianceStatus": "tb",
                                "planDate": f"{plan_date}",
                                "projectId": f"{project_id}",
                                "remake": "手续备注测试1",
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}"
                            },
                            {
                                "actualProgressDate": f"{actual_date}",
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "dictId": 88,
                                "dictName": "生产资质",
                                "feasibleComplianceId": f"{feasible_compliance_id2}",
                                "id": f"{id2}",
                                "implComplianceStatus": "tb",
                                "planDate": f"{plan_date}",
                                "projectId": f"{project_id}",
                                "remake": "手续备注测试2",
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}"
                            }
                        ]
                    })
                    response3 = requests.post(url4, data=data1, headers=headers1)
                    response_data3 = response3.json()
                    projectname2 = response_data3['data']['projectName']
                    # 4.2 项目合规性手续提交稽核
                    api4 = Api('api')['项目合规性手续提交稽核']
                    url5 = f"https://{host}{api4}"
                    data2 = json.dumps({
                        "processId": "1889950321795534848",
                        "businessId": f"{project_id}",
                        "nodeUserList": [
                            {
                                "nodeId": "1889950321795534849",
                                "userId": 70557
                            },
                            {
                                "nodeId": "1889950321795534850",
                                "userId": 71048
                            }
                        ],
                        "businessType": 7,
                        "businessData": {
                            "data": {
                                "projectName": f"{projectname2}",
                                "projectId": f"{project_id}"
                            }
                        }
                    })
                    headers2 = {
                        "Authorization": f"Bearer {authorization}",
                        "Content-Type": "application/json"
                    }
                    response4 = requests.post(url5, data=data2, headers=headers2)
                    response_data3 = response4.json()
                    assert response_data3['code'] == 200
                    log.debug(f"{projectname2}项目合规性手续提交稽核成功")
                    break
                else:
                    log.debug(f"第{i + 1}个项目已处于合规性手续办理流程中，跳过")
                    continue
            else:
                log.debug("没有可研完成且尚未提交合规性手续稽核的项目")
        else:
            log.debug("没有可研完成的项目")

    def ss_project_investment(self, query_name):
        """更新项目投资预算实施进度，提交稽核"""
        # 1.查询项目名称，模糊查询
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        api1 = Api('api')['可研完成的项目']
        url1 = f"https://{host}{api1}"
        projectname = urllib.parse.quote(query_name)
        projectname1 = f"projectName={projectname}"
        url2 = '&'.join([url1, projectname1])
        response1 = requests.get(url2, headers=headers)
        response_data1 = response1.json()['data']
        # print(response_data1)
        data_list1 = response_data1['list']
        num = response_data1['endRow']
        if num > 0:
            """可研完成的项目可能有多个，有些可能已经是提交稽核，用for循环来遍历尝试，直到添加成功break"""
            for i in range(num):
                # 2.查询项目投资预算实施进度详情
                list_info = data_list1[i]
                project_id = list_info['projectId']
                api2 = Api('api')['项目投资预算实施进度详情']
                url3 = f"https://{host}{api2}"
                url_ss = '?'.join([url3, f'projectId={project_id}'])
                response2 = requests.get(url_ss, headers=headers)
                response_json = response2.json()
                # print(response_json)
                response_data2 = response_json['data']
                if 'implAssetStatus' not in response_data2[0] :
                    # 3.1 无更新状态，保存项目投资预算实施进度
                    api3 = Api('api')['保存项目投资预算实施进度']
                    url4 = f"https://{host}{api3}"
                    data1 = json.dumps({
                        "projectId": f"{project_id}",
                        "detailList": [
                            {
                                "budgetAmount": 30,
                                "fieldCname": "1.基建概算",
                                "fieldName": "flatProAmount",
                                "projectId": f"{project_id}",
                                "sorted": 10,
                                "type": "count",
                                "implAssetStatus": "tb",
                                "actualAmount": 30
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "1.1 总平工程",
                                "fieldName": "totalFlatProAmount",
                                "projectId": f"{project_id}",
                                "sorted": 11,
                                "type": "edit",
                                "actualAmount": "10"
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "1.2 单体工程",
                                "fieldName": "synthFlatProAmount",
                                "projectId": f"{project_id}",
                                "sorted": 12,
                                "type": "edit",
                                "actualAmount": "10"
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "1.3 封装工程",
                                "fieldName": "warapFlatProAmount",
                                "projectId": f"{project_id}",
                                "sorted": 13,
                                "type": "edit",
                                "actualAmount": "10"
                            },
                            {
                                "budgetAmount": 0,
                                "fieldCname": "1.4 其他基建工程",
                                "fieldName": "otherFlatProAmount",
                                "projectId": f"{project_id}",
                                "sorted": 14,
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 30,
                                "fieldCname": "2.设备概算",
                                "fieldName": "equipmentAmount",
                                "projectId": f"{project_id}",
                                "sorted": 20,
                                "type": "count",
                                "actualAmount": 10
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "2.1 生产设备",
                                "fieldName": "produceEquipmentAmount",
                                "projectId": f"{project_id}",
                                "sorted": 21,
                                "type": "edit",
                                "actualAmount": "10"
                            },
                            {
                                "budgetAmount": 0,
                                "fieldCname": "2.2 环保设备",
                                "fieldName": "environmentEquipmentAmount",
                                "projectId": f"{project_id}",
                                "sorted": 22,
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "2.3 实验设备",
                                "fieldName": "experimentEquipmentAmount",
                                "projectId": f"{project_id}",
                                "sorted": 23,
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 0,
                                "fieldCname": "2.4 办公及后勤设备",
                                "fieldName": "rearEquipmentAmount",
                                "projectId": f"{project_id}",
                                "sorted": 24,
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "2.5 其他设备",
                                "fieldName": "otherEquipmentAmount",
                                "projectId": f"{project_id}",
                                "sorted": 25,
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "3.工程建设服务费",
                                "fieldName": "proServerAmount",
                                "projectId": f"{project_id}",
                                "sorted": 30,
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "4.土地购置费",
                                "fieldName": "landPurAmount",
                                "projectId": f"{project_id}",
                                "sorted": 40,
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 20,
                                "fieldCname": "5.不可预见费",
                                "fieldName": "preparAmount",
                                "projectId": f"{project_id}",
                                "sorted": 50,
                                "type": "count",
                                "actualAmount": 0
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "5.1 基本预备费",
                                "fieldName": "basicPreparAmount",
                                "projectId": f"{project_id}",
                                "sorted": 51,
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "5.2 涨价预备费",
                                "fieldName": "increasePreparAmount",
                                "projectId": f"{project_id}",
                                "sorted": 52,
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 100,
                                "fieldCname": "6.总投资额",
                                "fieldName": "totalAmount",
                                "projectId": f"{project_id}",
                                "sorted": 60,
                                "type": "count",
                                "actualAmount": 40
                            }
                        ]
                    }
                    )
                    headers1 = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {authorization}"
                    }
                    response3 = requests.post(url4, headers=headers1, data=data1)
                    print(response3.json())
                    response_data3 = response3.json()['data']
                    projectname2 = response_data3['projectName']
                    # 4.1 项目投资预算实施进度提交稽核
                    api4 = Api('api')['项目投资预算实施进度提交稽核']
                    url5 = f"https://{host}{api4}"
                    data2 = json.dumps({
                        "processId": "1889935646890528768",
                        "businessId": f"{project_id}",
                        "nodeUserList": [
                            {
                                "nodeId": "1889935646890528769",
                                "userId": 70557
                            },
                            {
                                "nodeId": "1889935646890528770",
                                "userId": 71048
                            }
                        ],
                        "businessType": 8,
                        "businessData": {
                            "data": {
                                "projectName": f"{projectname2}",
                                "projectId": f"{project_id}"
                            }
                        }
                    })
                    headers2 = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {authorization}"
                    }
                    response4 = requests.post(url5, headers=headers2, data=data2)
                    print(response4.json())
                    assert response4.json()['code'] == 200
                    log.debug(f'{projectname2}项目投资预算实施进度提交稽核成功')
                    break
                elif response_data2[0] ['implAssetStatus'] == 'tb':
                    # 3.2 更新状态为填报，走编辑逻辑
                    api3 = Api('api')['保存项目投资预算实施进度']
                    url4 = f"https://{host}{api3}"
                    create_time = response_data2[0] ['createdTime']
                    update_time = response_data2[0] ['updatedTime']
                    headers1 = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {authorization}"
                    }
                    id_list = []
                    for j in range(len(response_data2)):
                        id_list.append(response_data2[j]['id'])
                        j += 1
                    data1 = json.dumps({
                        "projectId": f"{project_id}",
                        "detailList": [
                            {
                                "actualAmount": 30,
                                "budgetAmount": 30,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "1.基建概算",
                                "fieldName": "flatProAmount",
                                "id": f"{id_list[0]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 10,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "count"
                            },
                            {
                                "actualAmount": 10,
                                "budgetAmount": 10,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "1.1 总平工程",
                                "fieldName": "totalFlatProAmount",
                                "id": f"{id_list[1]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 11,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "edit"
                            },
                            {
                                "actualAmount": 10,
                                "budgetAmount": 10,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "1.2 单体工程",
                                "fieldName": "synthFlatProAmount",
                                "id": f"{id_list[2]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 12,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 10,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "1.3 封装工程",
                                "fieldName": "warapFlatProAmount",
                                "id": f"{id_list[3]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 13,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "edit",
                                "actualAmount": "10"
                            },
                            {
                                "budgetAmount": 0,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "1.4 其他基建工程",
                                "fieldName": "otherFlatProAmount",
                                "id": f"{id_list[4]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 14,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "edit"
                            },
                            {
                                "actualAmount": 29,
                                "budgetAmount": 30,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "2.设备概算",
                                "fieldName": "equipmentAmount",
                                "id": f"{id_list[5]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 20,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "count"
                            },
                            {
                                "budgetAmount": 10,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "2.1 生产设备",
                                "fieldName": "produceEquipmentAmount",
                                "id": f"{id_list[6]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 21,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "edit",
                                "actualAmount": "10"
                            },
                            {
                                "budgetAmount": 0,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "2.2 环保设备",
                                "fieldName": "environmentEquipmentAmount",
                                "id": f"{id_list[7]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 22,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 10,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "2.3 实验设备",
                                "fieldName": "experimentEquipmentAmount",
                                "id": f"{id_list[8]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 23,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "edit",
                                "actualAmount": "10"
                            },
                            {
                                "budgetAmount": 0,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "2.4 办公及后勤设备",
                                "fieldName": "rearEquipmentAmount",
                                "id": f"{id_list[9]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 24,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 10,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "2.5 其他设备",
                                "fieldName": "otherEquipmentAmount",
                                "id": f"{id_list[10]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 25,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "edit",
                                "actualAmount": "9"
                            },
                            {
                                "budgetAmount": 10,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "3.工程建设服务费",
                                "fieldName": "proServerAmount",
                                "id": f"{id_list[11]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 30,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "edit",
                                "actualAmount": "10"
                            },
                            {
                                "budgetAmount": 10,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "4.土地购置费",
                                "fieldName": "landPurAmount",
                                "id": f"{id_list[12]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 40,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "edit",
                                "actualAmount": "10"
                            },
                            {
                                "actualAmount": 20,
                                "budgetAmount": 20,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "5.不可预见费",
                                "fieldName": "preparAmount",
                                "id": f"{id_list[13]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 50,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "count"
                            },
                            {
                                "budgetAmount": 10,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "5.1 基本预备费",
                                "fieldName": "basicPreparAmount",
                                "id": f"{id_list[14]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 51,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "edit",
                                "actualAmount": "10"
                            },
                            {
                                "budgetAmount": 10,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "5.2 涨价预备费",
                                "fieldName": "increasePreparAmount",
                                "id": f"{id_list[15]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 52,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "edit",
                                "actualAmount": "10"
                            },
                            {
                                "actualAmount": 99,
                                "budgetAmount": 100,
                                "createdBy": "曹孟",
                                "createdById": 68506,
                                "createdTime": f"{create_time}",
                                "fieldCname": "6.总投资额",
                                "fieldName": "totalAmount",
                                "id": f"{id_list[16]}",
                                "implAssetStatus": "tb",
                                "projectId": f"{project_id}",
                                "sorted": 60,
                                "updateById": 68506,
                                "updatedBy": "曹孟",
                                "updatedTime": f"{update_time}",
                                "type": "count"
                            }
                        ]
                    })
                    response3 = requests.post(url4, headers=headers1, data=data1)
                    print(response3.json())
                    #4.2 提交稽核
                    projectname2 = response3.json()["data"]["projectName"]
                    api4 = Api('api')['项目投资预算实施进度提交稽核']
                    url5 = f"https://{host}{api4}"
                    data2 = json.dumps({
                        "processId": "1889935646890528768",
                        "businessId": f"{project_id}",
                        "nodeUserList": [
                            {
                                "nodeId": "1889935646890528769",
                                "userId": 70557
                            },
                            {
                                "nodeId": "1889935646890528770",
                                "userId": 71048
                            }
                        ],
                        "businessType": 8,
                        "businessData": {
                            "data": {
                                "projectName": f"{projectname2}",
                                "projectId": f"{project_id}"
                            }
                        }
                    })
                    headers2 = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {authorization}"
                    }
                    response4 = requests.post(url5, headers=headers2, data=data2)
                    # print(response4.json())
                    assert response4.json()['code'] == 200
                    log.debug(f'{projectname2}项目投资预算实施进度提交稽核成功')
                    break
                else:
                    log.debug(f"第{i + 1}个项目已处于投资预算实施进度办理流程中，跳过")
                    continue
            else:
                log.debug("没有可研完成且尚未提交投资预算实施进度稽核的项目")
        else:
            log.debug("没有可研完成的项目")


Ss = SsGl()
if __name__ == '__main__':
    #1.添加实施许可令，提交稽核
    # Ss.ss_add_permit('测试')
    #2.添加项目公司，提交稽核
    # Ss.ss_project_company('测试')
    #3.添加项目招投标及合同文件，提交稽核
    # Ss.ss_project_contract('测试')
    #4.添加建设实施进度，提交稽核
    # Ss.ss_project_built('测试')
    #5.添加合规性手续，提交稽核
    # Ss.ss_project_procedure('测试')
    #6.添加投资预算实施进度，提交稽核
    Ss.ss_project_investment('测试')