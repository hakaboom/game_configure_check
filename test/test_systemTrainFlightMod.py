import pytest
import re
from loguru import logger
from tools.XlsReader import XlsReader
from .conftest import excel_assert
from tools.ConfigCheckerXlsx import check_null, check_regex, check_reference, CheckReference, check_range
import allure

param = [
    ('B_班次类型表(已确认).xls', '检查是否有空值', 'ALL',
     dict(action='check_null', blacklist=['fixedPassengerList', 'eventList'])),
    ('B_班次类型表(已确认).xls', '检查endTime', 'endTime',
     dict(action='check_regex', args=r'^-?\d+\.?\d*$')),
    ('B_班次类型表(已确认).xls', '检查ratioPassenger', 'ratioPassenger',
     dict(action='check_regex', args=r'^-?\d+\.?\d*$')),
    ('B_班次类型表(已确认).xls', '检查ratioPassenger', 'rangePassengerList',
     dict(action='check_reference', format=[r'(-?\d+){1},(-?\d+)+\|?', ['id', 'probability']],
          args=['id', 'C_随机乘客模板表（已确认）.xls;systemPassengerTemplateId'])),
]


class TestClass(object):
    @allure.title('初始化')
    def setup_class(self):
        self.xls_name = 'B_班次类型表(已确认).xls'
        with allure.step('Step: 读取表格'):
            try:
                self.xl = XlsReader(xls_name=self.xls_name)
            except FileNotFoundError as e:
                allure.attach("读取表格", "没有找到表:{}, 请检查表名".format(self.xls_name))
                raise e
        allure.attach(self.xls_name, "读取")

    @staticmethod
    def action_run(action, check_dict, xlsReader, args=None):
        if action == 'check_null':
            ret = check_null(check_dict, xlsReader=xlsReader)
        elif action == 'check_regex':
            ret = check_regex(check_dict, xlsReader=xlsReader, regex=args)
        elif action == 'check_range':
            ret = check_range(check_dict, xlsReader=xlsReader, rule=args)
        elif action == 'check_reference':
            ret = check_reference(check_dict, xlsReader=xlsReader, rule=args)
        else:
            raise ValueError('未知action参数 action={}'.format(action))
        return ret

    @allure.feature('配置表检查')
    @allure.title("{table_name};{story}")
    @pytest.mark.parametrize('table_name,story,col_name,case', param)
    def test_ttt(self, table_name, story, col_name, case):
        with allure.step('Step1: 读取表格数据'):
            blacklist = case.get('blacklist')
            check_dict = {}
            column_head_name_list = self.xl.get_head_col_name_list(blacklist)
            if col_name == 'ALL':
                for name in column_head_name_list:
                    check_dict[name] = self.xl.get_col_list_by_name(name)
            elif col_name in column_head_name_list:
                check_dict[col_name] = self.xl.get_col_list_by_name(col_name)
            else:
                raise ValueError(f"未能寻找到对应列名'{col_name}'", column_head_name_list)

        with allure.step('Step2：检查action是否正确'):
            action = case.get('action')
            if action not in ['check_null', 'check_regex', 'check_range', 'check_reference']:
                raise ValueError(f'action 填写错误 {action}:(check_null/check_regex/check_range/check_reference)')

        with allure.step('Step3：预处理表格数据'):
            if case.get('format') and col_name != 'ALL':
                xlformat = case.get('format')
                check = CheckReference(self.xls_name)
                check.handle_list(col_name, xlformat[0], xlformat[1])
            elif case.get('format') and col_name == 'ALL':
                raise ValueError('title为ALL时, 不能指定format参数')

        with allure.step(f"Step3：执行'{action}'检查"):
            args = case.get('args')
            if case.get('format'):
                if action == 'check_reference':
                    ret = check.check_reference(*args)
            else:
                ret = TestClass.action_run(action, check_dict=check_dict, xlsReader=self.xl,
                                           args=args)
            excel_assert(ret, self.xls_name)
