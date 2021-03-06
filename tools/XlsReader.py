# -*- coding: utf-8 -*-
""" 用于读取表格数据 """
import os
from xlrd import open_workbook
from utils import handle_xls_type
from setting import WORK_PATH


class XlsReader(object):
    def __init__(self, xls_name, path=WORK_PATH):
        self.work_path = path
        self.xls_name = xls_name
        self.xls_path = os.path.join(self.work_path, self.xls_name)
        self.ignore_lines = 5  # 获取数据时,跳过不会读取的行

        self.xl = open_workbook(self.xls_path)
        self.sheet = self.xl.sheet_by_index(0)
        self.end_tag_index = self.sheet.nrows
        self.set_end_tag_index()

    @handle_xls_type
    def get_row_value_list(self, rowx: int, start_colx: int = 0, end_colx: int = None) -> list:
        """
        获取表格内某一行的数据
        :param rowx: 在表格中的行数
        :param start_colx: 左切片
        :param end_colx: 右切片
        :return: 这一行的全部数据
        """
        return self.sheet.row_values(rowx - 1, start_colx, end_colx)

    @handle_xls_type
    def get_col_value_list(self, colx: int, start_rowx: int = 0, end_rowx: int = None) -> list:
        """
        获取表格内某一列的数据
        :param colx: 在表格中的列数
        :param start_rowx: 左切片
        :param end_rowx: 右切片
        :return: 这一列的全部数据
        """
        return self.sheet.col_values(colx - 1, start_rowx, end_rowx or self.end_tag_index)

    def get_cell_value(self, row_index: int, column_index: int):
        """
        获取某一行某一列的单元格内数据
        :param row_index: 在表格中的行数
        :param column_index: 在表格中的列数
        :return: 这一个单元格内的数据
        """
        return self.sheet.cell_value(row_index - 1, column_index - 1)

    def get_head_row_list(self) -> list:
        return self.get_row_value_list(self.ignore_lines)

    def get_head_col_name_list(self, blacklist: list = None) -> list:
        ret = []
        # if blacklist and not isinstance(blacklist, list):
        #     raise ValueError('blacklist must be list')
        for name in self.get_head_row_list():
            if name and name != '':
                if isinstance(blacklist, list) and name in blacklist:
                    pass
                else:
                    ret.append(name)
        return ret

    def get_col_list_by_name(self, name: str) -> list:
        head_list = self.get_row_value_list(self.ignore_lines)
        index = head_list.index(name) + 1 if name in head_list else None
        if index:
            return self.get_col_value_list(index)[self.ignore_lines:]
        else:
            raise ValueError('{xlsName}没有{name}列'.format(xlsName=self.xls_name, name=name))

    def get_col_number_by_name(self, name: str) -> int:
        head_list = self.get_row_value_list(self.ignore_lines)
        index = head_list.index(name) + 1 if name in head_list else None
        if index:
            return index
        else:
            raise ValueError('{xlsName}没有{name}列'.format(xlsName=self.xls_name, name=name))

    def set_end_tag_index(self):
        self.end_tag_index = self.get_end_tag_index()

    def get_end_tag_index(self):
        """ 数据表中第一列的最后一行都有 #END_TAG#, 获取时要舍弃这一行的数据 """
        try:
            firest_col = self.get_col_value_list(1, end_rowx=self.sheet.nrows)
            end_tag_index = firest_col.index('#END_TAG#')
        except ValueError:
            return self.sheet.nrows
        else:
            return end_tag_index
