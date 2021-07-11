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


def excel_assert(ret, tableName):
    """
    用于处理检查配置表返回的错误
    :param ret:
    :return: None
    """
    if ret:
        if not isinstance(EXCEL_ERROR.get(tableName), list):
            EXCEL_ERROR[tableName] = []
        EXCEL_ERROR[tableName].append(ret)
        error_message = '\n'.join([f"第{value['row']}行,列名:{value['column_name']},值:{value['value']},{value['message']}"
                                  for value in ret])
        assert not ret, f'{tableName}\n{error_message}'

