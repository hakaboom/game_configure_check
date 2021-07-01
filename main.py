from ConfigCheckDriver import CheckList
from XlsReader import XlsReader
import re

"""  本框架里所有表格相关的索引数值均从1开始计算 """
from utils import ncol_2_column

#
# a = CheckList()
# a.run()


s = '1,6|2,7000|'

# p = re.compile('^(\d+,?)+\d$')
p = re.compile('^(\d+,+\d+\|?)$')

print(p.search(s))