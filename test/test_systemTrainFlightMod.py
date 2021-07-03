from tools.XlsReader import XlsReader
from tools.ConfigCheckerXlsx import check_null
import pytest
import allure


@allure.feature("列车班次生成表")
class TestClass(object):
    @allure.title('初始化')
    def setup_class(self):
        self.xls_name = 'B_列车班次生成表.xls'
        with allure.step('Step: 读取表格'):
            try:
                self.list = XlsReader(xls_name=self.xls_name)
            except FileNotFoundError as e:
                allure.attach("读取表格", "没有找到表:{}, 请检查表名".format(self.xls_name))
                raise e
        allure.attach(self.xls_name, "读取")

    @allure.story("是否有空值")
    @allure.title('systemTrainFlightMod')
    def test_systemTrainFlightModId(self):
        """ 对systemTrainFlightModId 进行 check_null """
        with allure.step('Step1: 读取表格对应列'):
            check_list = self.list.get_col_list_by_name('systemTrainFlightModId')
        with allure.step('Step2: 检查是否为空'):
            check_dict = {
                'systemTrainFlightModId': check_list,
            }

            ret = check_null(check_dict=check_dict, xlsReader=self.list)

        text = ''.join([value.get('message') for value in ret])
        print(text)
        assert not ret

    @allure.story("是否有空值")
    @allure.title('name')
    def test_name(self):
        """ 对name 进行check_null"""
        with allure.step('Step1: 读取表格对应列'):
            check_list = self.list.get_col_list_by_name('name')
        with allure.step('Step2: 检查是否为空'):
            check_dict = {
                'name': check_list,
            }
            ret = check_null(check_dict=check_dict, xlsReader=self.list)

        text = ''.join([value.get('message') for value in ret])
        print(text)
        assert not ret
