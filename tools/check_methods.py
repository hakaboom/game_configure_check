# -*- coding: utf-8 -*-
import re
from .XlsReader import XlsReader
from utils import ncol_2_column, xls_float_correct, generate_result, pprint
from loguru import logger


def check_null(check_dict: dict, xlsReader: XlsReader):
    """ 检查列表内有无空数据 """
    ret_list = []
    for col_name, col_list in check_dict.items():
        # name在表格中对应列数
        col_number = xlsReader.get_col_number_by_name(col_name)
        for key, value in enumerate(col_list):
            if value is None:
                row_number = key + 1 + xlsReader.ignore_lines
                err_message = "值为空".format(col=ncol_2_column(col_number), row=row_number)
                logger.error("'{xls_name}'中：{name}属性, 第{col}列,第{row}行值为空".format(
                                xls_name=xlsReader.xls_name, name=col_name,
                                col=ncol_2_column(col_number), row=row_number))
                ret_list.append(generate_result(column_name=col_name, row=row_number, message=err_message, value=value))
    return ret_list


"""
常用正则：
    判断是否有指定字符 '^[A-Z]+$'
    判断格式 '1,2,3|4,5,6|7,8,9'可以使用 ^((\d+,){2}(\d+)+\|?)+(?<=\d)$
"""


def check_regex(check_dict: dict, xlsReader: XlsReader, regex):
    """ 检查数据有无格式错误 """
    ret_list = []
    for col_name, col_list in check_dict.items():
        # name在表格中对应的列数
        col_number = xlsReader.get_col_number_by_name(col_name)
        for key, value in enumerate(col_list):
            pattern = re.compile(regex)
            if pattern.search(str(value)) is None:
                row_number = key + 1 + xlsReader.ignore_lines
                err_message = "格式不符合规则"
                logger.error("'{xls_name}'中：{name}属性, 第{col}列,第{row}行值为'{value}' 不符合要求".format(
                    xls_name=xlsReader.xls_name, name=col_name,
                    col=ncol_2_column(col_number), row=row_number,
                    value=value))
                ret_list.append(generate_result(column_name=col_name, row=row_number, message=err_message, value=value))
    return ret_list


def check_range(check_dict: dict, xlsReader: XlsReader, rule):
    ret_list = []
    rule = re.compile("^((-?)\d+\.?\d?)[\s\S]((-?)\d+\.?\d?)$").findall(rule)
    if not rule:
        raise ValueError('rule错误无法解析 value={}'.format(rule))

    min_num, max_num = xls_float_correct(rule[0][0]), xls_float_correct(rule[0][2])
    for col_name, col_list in check_dict.items():
        # name在表格中对于的列数
        for key, value in enumerate(col_list):
            if value:
                num = xls_float_correct(value)
                row_number = key + 1 + xlsReader.ignore_lines
                if num <= min_num:
                    err_message = f'小于最低要求{min_num}'
                    logger.error(err_message)
                    ret_list.append(generate_result(column_name=col_name, row=row_number, message=err_message))
                elif num >= max_num:
                    err_message = f'大于最大要求{max_num}'
                    logger.error(err_message)
                    ret_list.append(generate_result(column_name=col_name, row=row_number, message=err_message, value=value))

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
    for col_name, col_list in check_dict.items():
        for key, value in enumerate(col_list):
            row_number = key + 1 + xlsReader.ignore_lines
            if not (str(value) in target_list):
                err_message = f"未找到{value}. 查找表:{target_table.xls_name},列{target_name}"
                logger.error(err_message)
                ret_list.append(generate_result(column_name=col_name, row=row_number, message=err_message, value=value))

    return ret_list


class CheckReference(object):
    """ 预先处理表数据后进行检查 """
    def __init__(self, xls_name: str):
        """
        例如数据为 100,10|200,20
        需要按照|分割为一组,一组内按照,分割
        regex=(-?\d+){1},(-?\d+)+\|?
        regex_report = ['id', 'probability']
        最后会生成一个列表, 数据格式为
        [
            {id: [], probability: []},
            {id: [], probability: []},
            {id: [], probability: []},
        ]
        :param xlsReader: 原表
        :param regex: 正则
        :param regex_report: 正则分割后的结果
        """
        self.xl = XlsReader(xls_name=xls_name)
        self.col_name = None
        self.col_list = None  # 处理后的列数据

    def handle_list(self, name, regex: str, regex_report: list):
        patter = re.compile(regex)
        col_list = []
        for cell_value in self.xl.get_col_list_by_name(name):
            _table = {}
            ret = patter.findall(cell_value)
            for index, _name in enumerate(regex_report):
                _table[_name] = [value[index] for value in ret]
            col_list.append(_table)

        self.col_list = col_list
        self.col_name = name

    def get_list_by_name(self, name):
        """ 根据名字,获取处理后都数据 """
        return [value.get(name) for value in self.col_list]

    def check_reference(self, name, rule):
        """
        :param name: 填入regex_report中定义的name,注意不是列表名
        :param rule: 规则
        :return:
        """
        ret_list = []
        rule = re.compile("^([\s\S]+);([\s\S]+)$").findall(rule)
        if not rule:
            raise ValueError('rule错误无法解析 value={}'.format(rule))
        check_list = self.get_list_by_name(name)
        """
            target_table_name: 需要索引到的表名
            target_name: 需要索引到的列名
        """
        target_table_name, target_name = rule[0][0], rule[0][1]
        target_table = XlsReader(target_table_name)
        target_list = target_table.get_col_list_by_name(target_name)
        target_list = [str(v) for v in target_list]
        for row, col_list in enumerate(check_list):
            row_number = row + self.xl.ignore_lines + 1
            for index, value in enumerate(col_list):
                if not (str(value) in target_list):
                    err_message = f"未找到{name}:{value}. 查找表:{target_table.xls_name},列:{target_name}"
                    logger.error(err_message)
                    cell_value = self.xl.get_cell_value(row_number, self.xl.get_col_number_by_name(self.col_name))
                    ret_list.append(generate_result(column_name=self.col_name, row=row_number, message=err_message,
                                                    value=cell_value))
        return ret_list
