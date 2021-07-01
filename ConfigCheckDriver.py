# -*- coding: utf-8 -*-
""" 用于执行检测 """
from XlsReader import XlsReader
from utils import pprint
from ConfigCheckerXlsx import check_null, check_regex, check_range

checklist_name = 'checkList.xls'


class CheckList(XlsReader):
    def __init__(self):
        super(CheckList, self).__init__(xls_name=checklist_name)
        self.ignore_lines = 1
        # [(table_name, table_column, action, args),...]
        self.check_list = [value for value in zip(self.get_col_list_by_name('table_name'),
                                                  self.get_col_list_by_name('table_column'),
                                                  self.get_col_list_by_name('action'),
                                                  self.get_col_list_by_name('args')
                                                  )]

    def run(self):
        for index in self.check_list:
            table_name, table_column, action, args = index

            xlsReader_table = XlsReader(xls_name=table_name)
            xlsReader_table.set_end_tag_index()

            # 获取配置表名称
            configure_name = xlsReader_table.get_cell_value(1, 1)

            # 获取id列
            column_name_list = [name for name in xlsReader_table.get_row_list(5) if name != '']
            check_list = {}

            if table_column == 'ALL':
                # 全部id下的数据都需要检查
                for name in column_name_list:
                    check_list[name] = xlsReader_table.get_col_list_by_name(name)
            elif table_column in column_name_list:
                check_list[table_column] = xlsReader_table.get_col_list_by_name(table_column)

            if action == 'check_null':
                ret = check_null(check_list, xlsReader=xlsReader_table)
            elif action == 'check_regex':
                ret = check_regex(check_list, xlsReader=xlsReader_table, regex=args)
            elif action == 'check_range':
                ret = check_range(check_list, xlsReader=xlsReader_table, rule=args)

