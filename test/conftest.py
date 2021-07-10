# -*- coding: utf-8 -*-
import allure
import pytest
from loguru import logger
from utils import pprint


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """ 获取到每个用例的执行结果 """
    outcome = yield
    report = outcome.get_result()

    if call.when == "teardown":
        report.description = str(item.function.__doc__)

    if call.when == 'call' and report.failed:
        """ 用例cell阶段,且用例执行失败 """
        # pass
        # allure.attach(, '失败截图', allure.attachment_type.PNG)


EXCEL_ERROR = {}


def print_excel_assert_error(ret):
    """ 用于将配置表返回的错误, 格式化输出 """
    table = []


def excel_assert(ret, table_name):
    """
    用于处理检查配置表返回的错误
    :param ret:
    :return: None
    """
    if ret:
        if not isinstance(EXCEL_ERROR.get(table_name), list):
            EXCEL_ERROR[table_name] = []
        EXCEL_ERROR[table_name].append(ret)
        pprint(ret)
        assert not ret

