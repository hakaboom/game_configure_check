from tools.ConfigCheckDriver import CheckList
from tools.XlsReader import XlsReader
from functools import wraps
import re
import time

"""  本框架里所有表格相关的索引数值均从1开始计算 """
""" 
pytest {test目录} --alluredir {导出的目录}
allure generate {pytest生成的alluredir} -o {导出的目录}
allure open {导出的目录}
"""


class print_run_time(object):
    def __init__(self, s=None):
        self.s = s

    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            ret = func(*args, **kwargs)
        return wrapped_function()
