# -*- coding: utf-8 -*-
import pytest
from loguru import logger
from py.xml import html


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """ 获取到每个用例的执行结果 """
    outcome = yield
    report = outcome.get_result()

    if call.when == "teardown":
        report.description = str(item.function.__doc__)
        print(report.description)


def pytest_configure(config):
    config._metadata = None


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("")])


def pytest_html_results_table_header(cells: list):
    cells[0] = html.th('测试结果')
    cells[1] = html.th('测试描述')
    cells[2] = html.th('消耗时长')
    cells[3] = html.th('链接')


def pytest_html_results_table_row(report, cells):
    if report.when == 'call':
        cells[1] = html.td(str(report.description))
