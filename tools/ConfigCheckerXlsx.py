# -*- coding: utf-8 -*-

import re
from .XlsReader import XlsReader
from utils import ncol_2_column, xls_float_correct, generate_result
from loguru import logger


def check_null(check_dict: dict, xlsReader: XlsReader):
    """ 检查列表内有无空数据 """
    ret_list = []
    for name, col_list in check_dict.items():
        # name在表格中对应列数
        col_number = xlsReader.get_col_number_by_name(name)
        for key, value in enumerate(col_list):
            if value is None:
                row_number = key + 1 + xlsReader.ignore_lines
                err_message = "'值为空".format(col=ncol_2_column(col_number), row=row_number)
                logger.error("'{xls_name}'中：{name}属性, 第{col}列,第{row}行值为空".format(
                                xls_name=xlsReader.xls_name, name=name,
                                col=ncol_2_column(col_number), row=row_number))
                ret_list.append(generate_result(column_name=name, row=row_number, message=err_message, value=value))
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
                err_message = "格式不符合规则"
                logger.error("'{xls_name}'中：{name}属性, 第{col}列,第{row}行值为'{value}' 不符合要求".format(
                    xls_name=xlsReader.xls_name, name=name,
                    col=ncol_2_column(col_number), row=row_number,
                    value=value))
                ret_list.append(generate_result(column_name=name, row=row_number, message=err_message, value=value))
    return ret_list


def check_range(check_dict: dict, xlsReader: XlsReader, rule):
    ret_list = []
    rule = re.compile("^((-?)\d+\.?\d?)[\s\S]((-?)\d+\.?\d?)$").findall(rule)
    if not rule:
        raise ValueError('rule错误无法解析 value={}'.format(rule))

    min_num, max_num = xls_float_correct(rule[0][0]), xls_float_correct(rule[0][2])
    for name, col_list in check_dict.items():
        # name在表格中对于的列数
        for key, value in enumerate(col_list):
            if value:
                num = xls_float_correct(value)
                row_number = key + 1 + xlsReader.ignore_lines
                if num <= min_num:
                    err_message = "小于最低要求{min_num}".format(value=value, min_num=min_num)
                    logger.error(err_message)
                    ret_list.append(generate_result(column_name=name, row=row_number, message=err_message))
                elif num >= max_num:
                    err_message = "大于最大要求{max_num}".format(value=value, max_num=max_num)
                    logger.error(err_message)
                    ret_list.append(generate_result(column_name=name, row=row_number, message=err_message, value=value))

    return ret_list


def check_reference(check_dict: dict, xlsReader: XlsReader, rule):
    """ 根据规则检查索引 """
    ret_list = []
    rule = re.compile("^([\s\S]+);([\s\S]+)$").findall(rule)
    if not rule:
        raise ValueError('rule错误无法解析 value={}'.format(rule))

    """
        target_table_name: 需要索引到的表名
        target_name: 需要索引到的列名
    """
    target_table_name, target_name = rule[0][0], rule[0][1]
    target_table = XlsReader(target_table_name)
    target_list = target_table.get_col_list_by_name(target_name)
    target_list = [str(v) for v in target_list]
    for name, col_list in check_dict.items():
        for key, value in enumerate(col_list):
            row_number = key + 1 + xlsReader.ignore_lines
            if not (str(value) in target_list):
                err_message = "未能在{target_xls_name}的{target_name}列找到对应索引{value}".format(
                    value=value, target_xls_name=target_table.xls_name, target_name=target_name
                )
                logger.error(err_message)
                ret_list.append(generate_result(column_name=name, row=row_number, message=err_message, value=value))

    return ret_list


class CheckReference(object):
    """
    一个检查索引的类
    类型ID，概率|类型ID，概率
    """
    def __init__(self, xlsReader: XlsReader, regex, regex_report: list):
        """
        :param xlsReader: 原表
        :param regex: 正则
        :param regex_report: 正则分割后的结果
        """
        self.xl = xlsReader
        self.regex = regex
        self.regex_report = regex_report

    def handle_list(self, name):
        col_list = self.xl.get_col_list_by_name(name)
        print(col_list)