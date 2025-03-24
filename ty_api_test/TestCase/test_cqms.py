#生产环境CQMS质量管理模块测试用例
import pytest

from ty_api_test.page.zhiliangguanli.yuancailiaoguanli import *

class TestCqms:
    def test1(self):
        yc = YcLgLi()