# -*- coding: utf-8 -*-
import re
from XlsReader import XlsReader
from utils import ncol_2_column
from loguru import logger


def generate_result(column_name, row):
    return dict(
        name=column_name,
        row=row,
    )


def check_null(check_list: dict, xlsReader: XlsReader):
    """ 检查列表内有无空数据 """
    ret_list = []
    for name, list_check in check_list.items():
        # name在表格中对应列数
        col_number = xlsReader.get_col_number_by_name(name)
        for key, value in enumerate(list_check):
            if value is None:
                row_number = key + 1 + xlsReader.ignore_lines
                logger.error("'{xls_name}'中：{name}属性, 第{col}列,第{row}行值为空".format(
                    xls_name=xlsReader.xls_name, name=name, col=ncol_2_column(col_number), row=row_number))

                ret_list.append(generate_result(column_name=name, row=key))

    return ret_list


"""
常用正则：
    判断是否有指定字符 '^[A-Z]+$'
    判断格式 ^(\d+,?)+\d$
"""


def check_regex(check_list: dict, xlsReader: XlsReader, regex):
    """ 检查数据有无格式错误 """
    ret_list = []
    for name, list_check in check_list.items():
        # name在表格中对应的列数
        col_number = xlsReader.get_col_number_by_name(name)
        for key, value in enumerate(list_check):
            pattern = re.compile(regex)
            if pattern.search(str(value)) is None:
                row_number = key + 1 + xlsReader.ignore_lines
                logger.error("'{xls_name}'中：{name}属性, 第{col}列,第{row}行值为{value},不符合要求".format(
                    xls_name=xlsReader.xls_name, name=name,
                    col=ncol_2_column(col_number), row=row_number,
                    value=value))

                ret_list.append(generate_result(column_name=name, row=key))

    return ret_list
