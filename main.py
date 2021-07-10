import os
import re
import pytest
from tools.XlsReader import XlsReader
from tools.ConfigCheckerXlsx import check_reference, CheckReference
from tools.pyxl import Pyxl
from tools.style import xlStyle
from utils import pprint
from test.conftest import EXCEL_ERROR
from setting import REPORT_PATH, REPORT_NAME
"""  本框架里所有表格相关的索引数值均从1开始计算 """
""" 
pytest {test目录} --alluredir {导出的目录}
allure generate {pytest生成的alluredir} -o {导出的目录}
allure open {导出的目录} 
"""

a = [
    {'row': 0, 'value': 1, 'message': '哈哈哈'},
    {'value': 2, 'row': 1, 'message': '哔哔哔'},
]
print(list(a[0].values()))


if __name__ == '11__main__':
    report_path = os.path.realpath('report')
    allure_path = os.path.realpath('allure-report')

    pytest.main(['-s', '--alluredir', report_path])
    allure_cmd = f'allure generate {report_path} -o {allure_path} --clean'
    p = os.popen(allure_cmd, mode='r')
    print(p.read())

    a = Pyxl(file_name=REPORT_NAME, path=REPORT_PATH, init=True)
    a.ignore_lines = 1
    a.write_value_to_row(['table_name', 'column_name', 'row', 'value', 'message'], 1, style=xlStyle)
    """
    dict {
        table1_name = [
            [
                {value,row,message,column_name},
                {value,row,message,column_name},
                ...
            ],
            [
                ...
            ],
            [
                ...
            ],
            ...
        ],
        table2_name = [
            [],
            [],
            []
        ],
    }
    """
    for table_name, table in EXCEL_ERROR.items():
        for table_error_list in table:
            for error in table_error_list:
                a.write_dict_to_row(_value=dict(
                    table_name=table_name, column_name=error['column_name'], row=error['row'], value=error['value'],
                    message=error['message']), style=xlStyle)
    a.save()
