from ConfigCheckDriver import CheckList
from XlsReader import XlsReader
from utils import xls_float_correct
import re

"""  本框架里所有表格相关的索引数值均从1开始计算 """
from utils import ncol_2_column

#
a = CheckList()
a.run()