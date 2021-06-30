# -*- coding: utf-8 -*-
""" 用于执行检测 """
from XlsReader import XlsReader

checklist_name = 'checkList.xls'


class CheckList(XlsReader):
    def __init__(self):
        super(CheckList, self).__init__(xls_name=checklist_name)
        self.ignore_lines = 1
        self.check_list = [value for value in zip(self.get_col_list_by_name('table_name'),
                                                  self.get_col_list_by_name('table_column'),
                                                  self.get_col_list_by_name('action'),
                                                  self.get_col_list_by_name('args')
                                                  )]
