import os
import re
import pytest
from tools.XlsReader import XlsReader
from tools.ConfigCheckerXlsx import check_reference, CheckReference
from utils import pprint
"""  本框架里所有表格相关的索引数值均从1开始计算 """
""" 
pytest {test目录} --alluredir {导出的目录}
allure generate {pytest生成的alluredir} -o {导出的目录}
allure open {导出的目录} 
"""
if __name__ == '__main__':
    # report_path = os.path.realpath('report')
    # allure_path = os.path.realpath('allure-report')
    #
    # pytest.main(['-s', '--alluredir', report_path])
    # allure_cmd = f'allure generate {report_path} -o {allure_path} --clean'
    # p = os.popen(allure_cmd, mode='r')
    # print(p.read())

    # xl =
    # patter = re.compile(r'(-?\d+){1},(-?\d+)+\|?')
    # col_list = xl.get_col_list_by_name('rangePassengerList')
    # for key, value in enumerate(col_list):
    #     table = {'id': [], 'probability': []}
    #     for s in patter.findall(value):
    #         table['id'].append(s[0])
    #         table['probability'].append(value[1])
    a = CheckReference(XlsReader(xls_name='B_班次类型表(已确认).xls'), r'(-?\d+){1},(-?\d+)+\|?', ['id', 'probability'])
    a.handle_list('rangePassengerList')