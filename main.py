import os
import sys
import pytest
from tools.pyxl import Pyxl
from tools.style import xlStyle
from utils import pprint
from test.conftest import EXCEL_ERROR
from setting import REPORT_PATH, REPORT_NAME, CHECKLIST_PATH, CHECKLIST_NAME
"""  本框架里所有表格相关的索引数值均从1开始计算 """
""" 
pytest {test目录} --alluredir {导出的目录}
allure generate {pytest生成的alluredir} -o {导出的目录}
allure open {导出的目录} 
"""


if __name__ == '11__main__':
    report_path = os.path.realpath('report')
    allure_path = os.path.realpath('allure-report')
    checklist_path = os.path.join(CHECKLIST_PATH, CHECKLIST_NAME)
    result_xlsx = Pyxl(file_name=REPORT_NAME, path=REPORT_PATH, init=True)

    if not os.path.exists(checklist_path):
        print(f'没有检测到"{checklist_path}"配置文件')
        sys.exit(0)

    if not result_xlsx.if_condition():
        print('保存结果的excel在打开状态,请关闭后再运行')
        sys.exit()

    pytest.main(['-s', '--alluredir', report_path])
    os.popen(f'allure generate {report_path} -o {allure_path} --clean', mode='r')

    result_xlsx.ignore_lines = 1
    result_xlsx.write_value_to_row(['table_name', 'column_name', 'row', 'value', 'message'], 1, style=xlStyle)
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
                result_xlsx.write_dict_to_row(_value=dict(
                    table_name=table_name, column_name=error['column_name'], row=error['row'], value=error['value'],
                    message=error['message']), style=xlStyle)
    result_xlsx.save()
