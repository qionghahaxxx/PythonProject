import pytest

from ty_api_test.page.lixiangtaizhang import *
from ty_api_test.page.daibanjihe import *
from ty_api_test.page.keyantaizhang import *


class Test_tzb:

#1.立项管理
    def test_lx1(self):
        """验证查看详情"""
        lx = Lxtz()
        lx.lx_info()
    def test_lx2(self):
        """验证查询功能"""
        lx = Lxtz()
        lx.lx_search()
    def test_lx3(self):
        """验证创建立项项目成功/暂存立项资料"""
        lx = Lxtz()
        id, project_name = l1.lx_create_project()
        try:
            lx.lx_save1(id)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
        finally:
            lx.lx_remove_project(1)
    def test_lx3(self):
        """验证项目评审和决策情况保存成功"""
        lx = Lxtz()
        id, project_name = l1.lx_create_project()
        try:
            lx.lx_save1(id)
            lx.lx_save2(id)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_lx4(self):
        """验证立项项目提交稽核成功"""
        lx = Lxtz()
        id,project_name = lx.lx_create_project()
        try:
            lx.lx_save1(id)
            lx.lx_save2(id)
            lx.lx_submit(id,project_name)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_lx5(self):
        """立项待办任务-二级单位稽核人稽核通过"""
        db1 = Dbjh('User3','Password3')
        try:
            db1.lx_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_lx6(self):
        """立项待办任务-二级单位稽核人稽核驳回"""
        db1 = Dbjh('User3','Password3')
        try:
            db1.lx_jude_reject(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_lx7(self):
        """立项待办任务-总部审定人稽核通过"""
        db1 = Dbjh('User2','Password2')
        try:
            db1.lx_jude_pass(1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_lx8(self):
        """立项待办任务-总部审定人稽核驳回"""
        db1 = Dbjh('User3','Password3')
        try:
            db1.jude_reject(1,'1')
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")

#可研管理
    def test_ky1(self):
        """验证添加可研项目/保存可研基础信息"""

        try:
            result = ky.ky_add_project()
            id1, createtime = result
            ky.ky_save1(id1, createtime)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky2(self):
        """验证创建可研项目，保存可研资料成功"""
        try:
            result = ky.ky_add_project()
            id1, createtime = result
            ky.ky_save1(id1, createtime)
            ky.ky_save2(id1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky3(self):
        """验证创建可研项目，保存实施计划成功"""
        try:
            result = ky.ky_add_project()
            id1, createtime = result
            ky.ky_save1(id1, createtime)
            ky.ky_save2(id1)
            ky.ky_save3(id1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky4(self):
        """验证创建可研项目，保存手续办理计划成功"""
        try:
            result = ky.ky_add_project()
            id1, createtime = result
            ky.ky_save1(id1, createtime)
            ky.ky_save2(id1)
            ky.ky_save3(id1)
            ky.ky_save4(id1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")


    def test_ky5(self):
        """验证创建可研项目，保存经济测算表成功"""
        try:
            result = ky.ky_add_project()
            id1, createtime = result
            ky.ky_save1(id1, createtime)
            ky.ky_save2(id1)
            ky.ky_save3(id1)
            ky.ky_save4(id1)
            ky.ky_save5(id1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky6(self):
        """验证创建可研项目，保存可研项目评审和决策情况成功"""
        try:
            result = ky.ky_add_project()
            id1, createtime = result
            ky.ky_save1(id1, createtime)
            ky.ky_save2(id1)
            ky.ky_save3(id1)
            ky.ky_save4(id1)
            ky.ky_save5(id1)
            ky.ky_save6(id1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky7(self):
        """验证创建可研项目，提交稽核成功"""
        try:
            result = ky.ky_add_project()
            id1, createtime = result
            ky.ky_save1(id1, createtime)
            ky.ky_save2(id1)
            ky.ky_save3(id1)
            ky.ky_save4(id1)
            ky.ky_save5(id1)
            ky.ky_save6(id1)
            ky.ky_save7(id1)
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky8(self):
        """可研待办任务-二级单位稽核人稽核通过"""
        db1 = Dbjh('User3','Password3')
        try:
            db1.jude_pass(1,'2')
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky9(self):
        """可研待办任务-二级单位稽核人稽核驳回"""
        db1 = Dbjh('User3','Password3')
        try:
            db1.jude_reject(1,'2')
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky10(self):
        """可研待办任务-总部审定人稽核通过"""
        db1 = Dbjh('User2','Password2')
        try:
            db1.jude_pass(1,'2')
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")
    def test_ky11(self):
        """可研待办任务-总部审定人稽核驳回"""
        db1 = Dbjh('User3','Password3')
        try:
            db1.jude_reject(1,'2')
        except Exception as e:
            log.error(f"测试过程中出现异常，异常信息为：{e}")


#实施许可令管理


if __name__ == '__main__':
    pytest.main(['-s','test_tzb.py'])
    #-s参数是一个命令行选项，它的作用是禁止捕获标准输出（stdout）和标准错误（stderr）。通常，pytest会捕获这些输出，并在测试完成后显示。如果你使用-s选项，那么测试过程中产生的输出会立即显示到控制台，而不是被捕获和延迟显示。
    #如果想要指定运行某个测试用例，可以在测试文件后面加"::类名::函数名",如:
    # pytest.main(['-s','test_tzb.py::Test_tzb::test_ky1'])
