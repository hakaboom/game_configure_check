import pytest
import re
from loguru import logger
from tools.XlsReader import XlsReader
from .conftest import excel_assert
from tools.ConfigCheckerXlsx import check_null, check_regex, check_reference, CheckReference
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
            excel_assert(ret, self.xls_name)

    @allure.story('检查endTime')
    @allure.title('endTime')
    def test_col_endTime(self):
        """ 检查 endTime列 """
        with allure.step('Step1：读取endTime列'):
            check_dict = {
                'endTime': self.list.get_col_list_by_name('endTime')
            }
        with allure.step('Step2：检查格式'):
            ret = check_regex(check_dict=check_dict, xlsReader=self.list, regex=r'^-?\d+\.?\d*$')
            excel_assert(ret, self.xls_name)

    @allure.story('检查ratioPassenger')
    @allure.title('ratioPassenger')
    def test_col_ratioPassenger(self):
        """ 检查 ratioPassenger列 """
        with allure.step('Step1：读取表格对应列'):
            check_dict = {
                'ratioPassenger': self.list.get_col_list_by_name('ratioPassenger')
            }
        with allure.step('Step2：检查格式'):
            # 纯数字
            ret = check_regex(check_dict=check_dict, xlsReader=self.list, regex=r'^-?\d+\.?\d*$')
            excel_assert(ret, self.xls_name)

    @allure.story('检查rangePassengerList')
    @allure.title('rangePassengerList')
    def test_col_rangePassengerList(self):
        """ 检查 rangePassengerList列 """
        with allure.step('Step1：读取表格对应列'):
            check_dict = {
                'rangePassengerList': self.list.get_col_list_by_name('rangePassengerList')
            }
        with allure.step('Step2：检查格式'):
            # 类型ID，概率|类型ID，概率
            ret = check_regex(check_dict=check_dict, xlsReader=self.list, regex=r'^(-?(\d+,){1}-?(\d+)+\|?)+(?<=\d)$')
            excel_assert(ret, self.xls_name)
        with allure.step('Step3：检查类型ID是否存在于C_固定乘客表'):
            check = CheckReference(self.xls_name)
            check.handle_list('rangePassengerList', r'(-?\d+){1},(-?\d+)+\|?', ['id', 'probability'])
            ret = check.check_reference('id', 'C_随机乘客模板表（已确认）.xls;systemPassengerTemplateId')
            excel_assert(ret, self.xls_name)

