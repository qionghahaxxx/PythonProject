import pytest

from ty_api_test.page.lixiangtaizhang import *
from ty_api_test.page.daibanjihe import *
from ty_api_test.page.keyantaizhang import *
from ty_api_test.page.shishiguanli import *


class TestTzb:

#1.立项管理
    def test_lx1(self):
        """验证按立项状态查询"""
        lx = LxGl()
        lx.lx_search2('lxtb')
    def test_lx2(self):
        """验证按项目名称查询"""
        lx = LxGl()
        lx.lx_search1('测试')
    def test_lx3(self):
        """验证创建立项项目成功/暂存立项资料"""
        lx = LxGl()
        lx_id, project_name = lx.lx_create_project()
        try:
            lx.lx_save1(lx_id)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
        finally:
            lx.lx_remove_project(1)
    def test_lx4(self):
        """验证项目评审和决策情况保存成功"""
        lx = LxGl()
        lx_id, project_name = lx.lx_create_project()
        try:
            lx.lx_save1(lx_id)
            lx.lx_save2(lx_id)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_lx5(self):
        """验证立项项目提交稽核成功"""
        lx = LxGl()
        lx_id,project_name = lx.lx_create_project()
        try:
            lx.lx_save1(lx_id)
            lx.lx_save2(lx_id)
            lx.lx_submit(lx_id, project_name)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_lx6(self):
        """立项待办任务-二级单位稽核人稽核通过"""
        db = DbJh('User3', 'Password3')
        try:
            db.lx_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_lx7(self):
        """立项待办任务-二级单位稽核人稽核驳回"""
        db = DbJh('User3', 'Password3')
        try:
            db.lx_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_lx8(self):
        """立项待办任务-总部审定人稽核通过"""
        db = DbJh('User2', 'Password2')
        try:
            db.lx_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_lx9(self):
        """立项待办任务-总部审定人稽核驳回"""
        db = DbJh('User3', 'Password3')
        try:
            db.lx_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")

#可研管理
    def test_ky1(self):
        """验证添加可研项目/保存可研基础信息"""
        try:
            ky_result = ky.ky_add_project('测试')
            ky_id, create_time = ky_result
            ky.ky_save1(ky_id, create_time)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky2(self):
        """验证创建可研项目，保存可研资料成功"""
        try:
            ky_result = ky.ky_add_project('测试')
            ky_id, create_time = ky_result
            ky.ky_save1(ky_id, create_time)
            ky.ky_save2(ky_id)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky3(self):
        """验证创建可研项目，保存实施计划成功"""
        try:
            ky_result = ky.ky_add_project('测试')
            ky_id, create_time = ky_result
            ky.ky_save1(ky_id, create_time)
            ky.ky_save2(ky_id)
            ky.ky_save3(ky_id)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky4(self):
        """验证创建可研项目，保存手续办理计划成功"""
        try:
            ky_result = ky.ky_add_project('测试')
            ky_id, create_time = ky_result
            ky.ky_save1(ky_id, create_time)
            ky.ky_save2(ky_id)
            ky.ky_save3(ky_id)
            ky.ky_save4(ky_id)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")


    def test_ky5(self):
        """验证创建可研项目，保存经济测算表成功"""
        try:
            ky_result = ky.ky_add_project('测试')
            ky_id, create_time = ky_result
            ky.ky_save1(ky_id, create_time)
            ky.ky_save2(ky_id)
            ky.ky_save3(ky_id)
            ky.ky_save4(ky_id)
            ky.ky_save5(ky_id)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky6(self):
        """验证创建可研项目，保存可研项目评审和决策情况成功"""
        try:
            ky_result = ky.ky_add_project('测试')
            ky_id, create_time = ky_result
            ky.ky_save1(ky_id, create_time)
            ky.ky_save2(ky_id)
            ky.ky_save3(ky_id)
            ky.ky_save4(ky_id)
            ky.ky_save5(ky_id)
            ky.ky_save6(ky_id)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky7(self):
        """验证创建可研项目，提交稽核成功"""
        try:
            ky_result = ky.ky_add_project('测试')
            ky_id, create_time = ky_result
            ky.ky_save1(ky_id, create_time)
            ky.ky_save2(ky_id)
            ky.ky_save3(ky_id)
            ky.ky_save4(ky_id)
            ky.ky_save5(ky_id)
            ky.ky_save6(ky_id)
            ky.ky_save7(ky_id)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky8(self):
        """可研待办任务-二级单位稽核人稽核通过"""
        db = DbJh('User3', 'Password3')
        try:
            db.ky_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky9(self):
        """可研待办任务-二级单位稽核人稽核驳回"""
        db = DbJh('User3', 'Password3')
        try:
            db.ky_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky10(self):
        """可研待办任务-总部审定人稽核通过"""
        db = DbJh('User2', 'Password2')
        try:
            db.ky_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky11(self):
        """可研待办任务-总部审定人稽核驳回"""
        db = DbJh('User3', 'Password3')
        try:
            db.ky_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")


#实施许可令管理
    def test_ss1(self):
        """验证添加实施许可令，提交稽核成功"""
        try:
            Ss.ss_add_permit('测试')
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss2(self):
        """验证添加项目公司，提交稽核成功"""
        try:
            Ss.ss_project_company('测试')
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss3(self):
        """验证添加项目招投标及合同文件，提交稽核成功"""
        try:
            Ss.ss_project_contract('测试')
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss4(self):
        """验证添加建设实施进度，提交稽核成功"""
        try:
            Ss.ss_project_built('测试')
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss5(self):
        """验证添加合规性手续，提交稽核成功"""
        try:
            Ss.ss_project_procedure('测试')
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss6(self):
        """验证添加投资预算实施进度，提交稽核成功"""
        try:
            Ss.ss_project_investment('测试')
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss7(self):
        """验证实施许可令待办任务，二级单位稽核人稽核通过"""
        db = DbJh('User3', 'Password3')
        try:
            db.ss_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss8(self):
        """验证实施许可令待办任务，二级单位稽核人稽核驳回"""
        db = DbJh('User3', 'Password3')
        try:
            db.ss_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss9(self):
        """验证实施许可令待办任务，总部审定人稽核通过"""
        db = DbJh('User2', 'Password2')
        try:
            db.ss_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss10(self):
        """验证实施许可令待办任务，总部审定人稽核驳回"""
        db = DbJh('User2', 'Password2')
        try:
            db.ss_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss11(self):
        """验证项目公司待办任务，二级单位稽核人稽核通过"""
        db = DbJh('User3', 'Password3')
        try:
            db.company_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss12(self):
        """验证项目公司待办任务，二级单位稽核人稽核驳回"""
        db = DbJh('User3', 'Password3')
        try:
            db.company_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss13(self):
        """验证项目公司待办任务，总部审定人稽核通过"""
        db = DbJh('User2', 'Password2')
        try:
            db.company_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss14(self):
        """验证项目公司待办任务，总部审定人稽核驳回"""
        db = DbJh('User2', 'Password2')
        try:
            db.company_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss15(self):
        """验证项目招投标及合同文件待办任务，二级单位稽核人稽核通过"""
        db = DbJh('User3', 'Password3')
        try:
            db.contract_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss16(self):
        """验证项目招投标及合同文件待办任务，二级单位稽核人稽核驳回"""
        db = DbJh('User3', 'Password3')
        try:
            db.contract_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss17(self):
        """验证项目招投标及合同文件待办任务，总部审定人稽核通过"""
        db = DbJh('User2', 'Password2')
        try:
            db.contract_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss18(self):
        """验证项目招投标及合同文件待办任务，总部审定人稽核驳回"""
        db = DbJh('User2', 'Password2')
        try:
            db.contract_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss19(self):
        """验证建设实施进度待办任务，二级单位稽核人稽核通过"""
        db = DbJh('User3', 'Password3')
        try:
            db.progress_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss20(self):
        """验证建设实施进度待办任务，二级单位稽核人稽核驳回"""
        db = DbJh('User3', 'Password3')
        try:
            db.progress_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss21(self):
        """验证建设实施进度待办任务，总部审定人稽核通过"""
        db = DbJh('User2', 'Password2')
        try:
            db.progress_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss22(self):
        """验证建设实施进度待办任务，总部审定人稽核驳回"""
        db = DbJh('User2', 'Password2')
        try:
            db.progress_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss23(self):
        """验证合规性手续待办任务，二级单位稽核人稽核通过"""
        db = DbJh('User3', 'Password3')
        try:
            db.compliance_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss24(self):
        """验证合规性手续待办任务，二级单位稽核人稽核驳回"""
        db = DbJh('User3', 'Password3')
        try:
            db.compliance_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss25(self):
        """验证合规性手续待办任务，总部审定人稽核通过"""
        db = DbJh('User2', 'Password2')
        try:
            db.compliance_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss26(self):
        """验证合规性手续待办任务，总部审定人稽核驳回"""
        db = DbJh('User2', 'Password2')
        try:
            db.compliance_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss27(self):
        """验证预算实施进度待办任务，二级单位稽核人稽核通过"""
        db = DbJh('User3', 'Password3')
        try:
            db.asset_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss28(self):
        """验证预算实施进度待办任务，二级单位稽核人稽核驳回"""
        db = DbJh('User3', 'Password3')
        try:
            db.asset_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss29(self):
        """验证预算实施进度待办任务，总部审定人稽核通过"""
        db = DbJh('User2', 'Password2')
        try:
            db.asset_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ss30(self):
        """验证预算实施进度待办任务，总部审定人稽核驳回"""
        db = DbJh('User2', 'Password2')
        try:
            db.asset_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")



if __name__ == '__main__':
    pytest.main(['-s','test_tzb.py'])
    #-s参数是一个命令行选项，它的作用是禁止捕获标准输出（stdout）和标准错误（stderr）。通常，pytest会捕获这些输出，并在测试完成后显示。如果你使用-s选项，那么测试过程中产生的输出会立即显示到控制台，而不是被捕获和延迟显示。
    #如果想要指定运行某个测试用例，可以在测试文件后面加"::类名::函数名",如:
    # pytest.main(['-s','test_tzb.py::TestTzb::test_ky1'])
