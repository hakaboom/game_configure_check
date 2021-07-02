import pytest
from XlsReader import XlsReader
from ConfigCheckDriver import CheckList
from ConfigCheckerXlsx import check_null


class TestClass(object):
    def setup(self):
        self.list = XlsReader(xls_name='B_列车班次生成表.xls')

    def test_systemTrainFlightModId(self):
        check_list = self.list.get_col_list_by_name('systemTrainFlightModId')
        check_dict = {
            'systemTrainFlightModId': check_list,

        }
        ret = check_null(check_dict=check_dict, xlsReader=self.list)
        assert ret is None
