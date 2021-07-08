import pytest

from tools.XlsReader import XlsReader
from tools.ConfigCheckerXlsx import check_null
import allure


@allure.feature("列车班次生成表")
class TestClass(object):
    @allure.title('初始化')
    def setup_class(self):
        self.xls_name = 'B_班次类型表(已确认).xls'
        with allure.step('Step: 读取表格'):
            try:
                self.list = XlsReader(xls_name=self.xls_name)
            except FileNotFoundError as e:
                allure.attach("读取表格", "没有找到表:{}, 请检查表名".format(self.xls_name))
                raise e
        allure.attach(self.xls_name, "读取")

    @allure.story('检查是否有空值')
    @allure.title('ALL')
    def test_check_all_null(self):
        """ 检查所有参数是否有空值 """
        with allure.step('Step1: 读取表格对应列'):
            blacklist = ['fixedPassengerList', 'eventList']
            column_name_list = self.list.get_head_col_name_list(blacklist)
            check_dict = {}
            for name in column_name_list:
                check_dict[name] = self.list.get_col_list_by_name(name)
        with allure.step('Step2: 检查是否为空'):
            ret = check_null(check_dict=check_dict, xlsReader=self.list)

        text = ''.join([value.get('message') for value in ret])
        assert not ret

