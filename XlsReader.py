# -*- coding: utf-8 -*-
""" 用于读取表格数据 """
import xlrd

xls_path = "D:\python\game_configure_check"


class XlsReader(object):
    def __init__(self, xls_name):
        self.path = xls_path
        self.xls_name = xls_name
        self.ignore_lines = 5  # 获取数据时,跳过不会读取的行
        self.xl = xlrd.open_workbook(self.path+"\\"+self.xls_name)
        self.sheet = self.xl.sheet_by_index(0)

    def get_row_list(self, rowx: int, start_colx: int = 0, end_colx: int = None):
        """
        获取表格内某一行的数据
        :param rowx: 在表格中的行数
        :param start_colx: 左切片
        :param end_colx: 右切片
        :return: 这一行的全部数据
        """
        return self.sheet.row_values(rowx - 1, start_colx, end_colx)

    def get_col_list(self, clox: int, start_rowx: int = 0, end_rowx: int = None):
        """
        获取表格内某一列的数据
        :param clox: 在表格中的列数
        :param start_rowx: 左切片
        :param end_rowx: 右切片
        :return: 这一列的全部数据
        """
        return self.sheet.col_values(clox-1, start_rowx, end_rowx)

    def get_cell_value(self, row_index: int, column_index: int):
        """
        获取某一行某一列的单元格内数据
        :param row_index: 在表格中的行数
        :param column_index: 在表格中的列数
        :return: 这一个单元格内的数据
        """
        return self.sheet.cell_value(row_index - 1, column_index - 1)

    def get_col_list_by_name(self, name: str):
        head_list = self.get_row_list(self.ignore_lines)
        index = head_list.index(name) + 1 if name in head_list else None
        if index:
            return self.get_col_list(index)[self.ignore_lines:]
        else:
            raise ValueError('{xlsName}没有{name}列'.format(xlsName=self.xls_name, name=name))