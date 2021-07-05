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
a.write_value_to_row(['表名', '对应行数', '表格内参数', '问题'], 1, style=xlStyle)

for _ in ret:
    table_name = _[0]
    for ret_dict in _[1]:
        row = ret_dict.get('row')
        value = ret_dict.get('value')
        message = ret_dict.get('message')
        a.write_value_to_row([table_name, row, value, message], style=xlStyle)


a.save()
