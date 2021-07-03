# -*- coding: utf-8 -*-
import re
from .XlsReader import XlsReader
from utils import ncol_2_column, xls_float_correct
from loguru import logger


def generate_result(column_name, row, message):
    return dict(
        message=message,
    )


def check_null(check_dict: dict, xlsReader: XlsReader):
    """ 检查列表内有无空数据 """
    ret_list = []
    for name, col_list in check_dict.items():
        # name在表格中对应列数
        col_number = xlsReader.get_col_number_by_name(name)
        for key, value in enumerate(col_list):
            if value is None:
                row_number = key + 1 + xlsReader.ignore_lines
                # err_message = "'{xls_name}'中：{name}属性, 第{col}列,第{row}行值为空".format(
                #     xls_name=xlsReader.xls_name, name=name, col=ncol_2_column(col_number), row=row_number)
                err_message = "'第{col}列,第{row}行值为空".format(col=ncol_2_column(col_number), row=row_number)
                logger.error(err_message)
                ret_list.append(generate_result(column_name=name, row=key, message=err_message))
    return ret_list


"""
常用正则：
    判断是否有指定字符 '^[A-Z]+$'
    判断格式 '1,2,3|4,5,6|7,8,9'可以使用 ^((\d+,){2}(\d+)+\|?)+(?<=\d)$
"""


def check_regex(check_dict: dict, xlsReader: XlsReader, regex):
    """ 检查数据有无格式错误 """
    ret_list = []
    for name, col_list in check_dict.items():
        # name在表格中对应的列数
        col_number = xlsReader.get_col_number_by_name(name)
        for key, value in enumerate(col_list):
            pattern = re.compile(regex)
            if pattern.search(str(value)) is None:
                row_number = key + 1 + xlsReader.ignore_lines
                # err_message = "'{xls_name}'中：{name}属性, 第{col}列,第{row}行值为'{value}' 不符合要求".format(
                #     xls_name=xlsReader.xls_name, name=name,
                #     col=ncol_2_column(col_number), row=row_number,
                #     value=value)
                err_message = "'第{col}列,第{row}行值为'{value}' 不符合要求".format(
                    col=ncol_2_column(col_number), row=row_number,
                    value=value)
                logger.error(err_message)
                ret_list.append(generate_result(column_name=name, row=key, message=err_message))
    return ret_list


def check_range(check_dict: dict, xlsReader: XlsReader, rule):
    ret_list = []
    rule = re.compile('^((-?)\d+\.?\d+)[\s\S]''((-?)\d+\.?\d+)$').findall(rule)
    if not rule:
        raise ValueError('rule错误无法解析 value={}'.format(rule))

    min_num, max_num = xls_float_correct(rule[0][0]), xls_float_correct(rule[0][2])
    for name, col_list in check_dict.items():
        # name在表格中对于的列数
        col_number = xlsReader.get_col_number_by_name(name)
        for key, value in enumerate(col_list):
            if value:
                num = xls_float_correct(value)
                row_number = key + 1 + xlsReader.ignore_lines
                err_message = ''
                if num < min_num:
                    # err_message = "'{xls_name}'中：{name}属性, 第{col}列,第{row}行值为{value} 小于最低要求{min_num}".format(
                    #     xls_name=xlsReader.xls_name, name=name,
                    #     col=ncol_2_column(col_number), row=row_number,
                    #     value=value, min_num=min_num)
                    err_message = "'第{col}列,第{row}行值为{value} 小于最低要求{min_num}".format(
                        col=ncol_2_column(col_number), row=row_number,
                        value=value, min_num=min_num)
                elif num > max_num:
                    # err_message = "'{xls_name}'中：{name}属性, 第{col}列,第{row}行值为{value} 大于最大要求{max_num}".format(
                    #     xls_name=xlsReader.xls_name, name=name,
                    #     col=ncol_2_column(col_number), row=row_number,
                    #     value=value, max_num=max_num)
                    err_message = "'第{col}列,第{row}行值为{value} 大于最大要求{max_num}".format(
                        col=ncol_2_column(col_number), row=row_number,
                        value=value, max_num=max_num)

                logger.error(err_message)
                ret_list.append(generate_result(column_name=name, row=key, message=err_message))

    return ret_list
