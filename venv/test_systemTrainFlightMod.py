from tools.XlsReader import XlsReader
from tools.ConfigCheckerXlsx import check_null
from pytest_html import extras
import pytest


class TestClass(object):
    def setup(self):
        self.list = XlsReader(xls_name='B_列车班次生成表.xls')

    def test_systemTrainFlightModId(self, extra):
        """ 对systemTrainFlightModId 进行 check_null """
        check_list = self.list.get_col_list_by_name('systemTrainFlightModId')
        check_dict = {
            'systemTrainFlightModId': check_list,
        }
        ret = check_null(check_dict=check_dict, xlsReader=self.list)
        text = '{}:\n{}'.format(self.list.xls_name,
                                ';\n'.join([value.get('message') for value in ret]))
        extra.append(extras.text(text))
        # assert ret is None
