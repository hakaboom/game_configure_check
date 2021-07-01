# -*- coding: utf-8 -*-
import re
from XlsReader import XlsReader
from utils import ncol_2_column, xls_float_correct
from loguru import logger


def generate_result(column_name, row):
    return dict(
        name=column_name,
        row=row,
    )


def check_null(check_list: dict, xlsReader: XlsReader):
    """ 检查列表内有无空数据 """
    ret_list = []
    for name, col_list in check_list.items():
        # name在表格中对应列数
        col_number = xlsReader.get_col_number_by_name(name)
        for key, value in enumerate(col_list):
            if value is None:
                row_number = key + 1 + xlsReader.ignore_lines
                logger.error("'{xls_name}'中：{name}属性, 第{col}列,第{row}行值为空".format(
                    xls_name=xlsReader.xls_name, name=name, col=ncol_2_column(col_number), row=row_number))

                ret_list.append(generate_result(column_name=name, row=key))

    return ret_list


"""
常用正则：
    判断是否有指定字符 '^[A-Z]+$'
    判断格式 '1,2,3|4,5,6|7,8,9'可以使用 ^((\d+,){2}(\d+)+\|?)+(?<=\d)$
"""


def check_regex(check_list: dict, xlsReader: XlsReader, regex):
    """ 检查数据有无格式错误 """
    ret_list = []
    for name, col_list in check_list.items():
        # name在表格中对应的列数
        col_number = xlsReader.get_col_number_by_name(name)
        for key, value in enumerate(col_list):
            pattern = re.compile(regex)
            if pattern.search(str(value)) is None:
                row_number = key + 1 + xlsReader.ignore_lines
                logger.error("'{xls_name}'中：{name}属性, 第{col}列,第{row}行值为'{value}'  不符合要求".format(
                    xls_name=xlsReader.xls_name, name=name,
                    col=ncol_2_column(col_number), row=row_number,
                    value=value))

                ret_list.append(generate_result(column_name=name, row=key))

    return ret_list


def check_range(check_list: dict, xlsReader: XlsReader, rule):
    ret_list = []
    rule = re.compile('(\d*\.?\d+)?[\s\S](\d*\.?\d+)?').findall(rule)
    if not rule:
        raise ValueError('rule错误无法解析 value={}'.format(rule))
    min_value, max_value = xls_float_correct(rule[0][0]), xls_float_correct(rule[0][1])
    for name, col_list in check_list.items():
        # name在表格中对于的列数
        col_number = xlsReader.get_col_number_by_name(name)
        for key, value in enumerate(col_list):
            if value:
                pas