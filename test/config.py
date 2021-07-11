# -*- coding: utf-8 -*-
import re
import os
import loguru

from tools.XlsReader import XlsReader
from tools.pyxl import Pyxl
from setting import CHECKLIST_NAME, CHECKLIST_PATH, WORK_PATH
from utils import pprint


class CheckList(XlsReader):
    def __init__(self):
        super(CheckList, self).__init__(xls_name=CHECKLIST_NAME, path=CHECKLIST_PATH)
        self.ignore_lines = 1
        self.check_list = []

        for row, table_name in enumerate(self.get_col_list_by_name('table_name')):
            row = row + 1 + self.ignore_lines
            table_name, story, table_column, action, value_format, args, blacklist = self.get_row_value_list(row)
            format_args = []
            if value_format:
                formatRE = re.compile('regex=\((.+)\);split=\((.+)\)')
                ret = formatRE.findall(value_format)[0]
                format_regex = ret[0]
                format_split = re.split(',', ret[1])
                format_args = [format_regex, format_split]

            if blacklist:
                blacklistRE = re.compile('(\w+);?')
                blacklist = blacklistRE.findall(blacklist)

            if value_format:
                """ 
                如果将参数分割处理,args则需要指定选择参数,与split里分割的相因
                """
                argsRE = re.compile('^([\s\S]+),([\s\S]+)$')
                args = argsRE.findall(args)[0]

            self.check_list.append([table_name, story, table_column, dict(
                action=action, blacklist=blacklist, format=format_args,
                args=args
            )])


class LoadAllExcel(object):
    def __init__(self):
        self.xls = {}
        for root, dirs, files in os.walk(WORK_PATH):
            for file in files:
                if os.path.splitext(file)[1] == '.xls':
                    self.xls[file] = XlsReader(path=WORK_PATH, xls_name=file)
                elif os.path.splitext(file)[1] == '.xlsx':
                    self.xls[file] = Pyxl(file_name=file, path=WORK_PATH)

    def get_xl_by_name(self, name):
        return self.xls.get(name)
