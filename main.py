from tools.ConfigCheckDriver import CheckList
from tools.style import xlStyle
from tools.pyxl import Pyxl
from setting import REPORT_PATH, REPORT_NAME
"""  本框架里所有表格相关的索引数值均从1开始计算 """
""" 
pytest {test目录} --alluredir {导出的目录}
allure generate {pytest生成的alluredir} -o {导出的目录}
allure open {导出的目录}
"""
#
a = CheckList()
ret = a.run()


a = Pyxl(file_name=REPORT_NAME, path=REPORT_PATH, init=True)
a.ignore_lines = 1
a.write_value_to_row(['table_name', 'column_name', 'row', 'value', 'message'], 1, style=xlStyle)

for _ in ret:
    table_name = _[0]
    for ret_dict in _[1]:
        ret_dict['table_name'] = table_name
        a.write_dict_to_row(ret_dict, style=xlStyle)

a.write_value_to_row(['表文件名', '列名', '对应行数', '单元格内参数', '错误信息'], 1, style=xlStyle)
a.save()
