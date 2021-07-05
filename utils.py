import re


def generate_result(column_name=None, row=None, value=None, message=""):
    return dict(
        value=value,
        row=row,
        message=message,
    )


def handle_xls_type(func):
    """ 处理表内数据格式"""
    def wrapper(self, *args, **kwargs):
        new_list = []
        xls_list = func(self, *args, **kwargs)
        for value in xls_list:
            if isinstance(value, (float, int)):
                # 处理xlrd在转换数字时,会把int转换为float
                new_list.append(xls_float_correct(value))
            elif isinstance(value, str) and len(value.strip()) == 0:
                # 判断数据为空
                new_list.append(None)
            else:
                new_list.append(value)
        return new_list

    return wrapper


def xls_float_correct(num):
    """ 用于处理xlrd在转换数字时,会把int转换为float"""
    s = str(num)
    s_split = s.split('.')
    if len(s_split) == 1:  # s = '1'
        return int(num)
    elif len(s_split) == 2:  # s = '1.0'
        if int(s_split[1]) == 0:
            return int(s_split[0])
        else:
            return float(num)
    else:
        raise ValueError('传入值错误 num={}'.format(num))


def ncol_2_column(num):
    """ 转换数字行数为表格中的字母列数"""
    num = num - 1  # 本框架里所有表格相关的数值均从1开始计算
    m = num // 26
    r = num % 26
    if m >= 1:
        left = chr(m + 64)
        right = chr(r + 65)
        return '{}{}'.format(left, right)
    else:
        return chr(num + 65)


def get_type(value):
    s = re.findall(r'<class \'(.+?)\'>', str(type(value)))
    if s:
        return s[0]
    else:
        raise ValueError('unknown error,can not get type: value={}, type={}'.format(value, type(value)))


def get_space(SpaceNum=1):
    return '\t'*SpaceNum


def pprint(*args):
    _str = []
    for index, value in enumerate(args):
        if isinstance(value, (dict, tuple, list)):
            _str.append('[{index}]({type}) = {value}\n'.format(index=index, value=_print(value),
                                                                     type=get_type(value)))
        else:
            _str.append('[{index}]({type}) = {value}\n'.format(index=index, value=value,
                                                                   type=get_type(value)))
    print(''.join(_str))


def _print(args, SpaceNum=1):
    _str = []
    SpaceNum += 1
    if isinstance(args, (tuple, list)):
        _str.append('')
        for index, value in enumerate(args):
            _str.append('{space}[{index}]({type}) = {value}'.format(index=index, value=_print(value, SpaceNum),
                                                                    type=get_type(value), space=get_space(SpaceNum)))
    elif isinstance(args, dict):
        _str.append('')
        for key, value in args.items():
            _str.append('{space}[{key}]({type}) = {value}'.format(key=key, value=_print(value,SpaceNum),
                                                                  type=get_type(value), space=get_space(SpaceNum)))
    else:
        _str.append(str(args))

    return '\n'.join(_str)


def decode_check_list_ret(ret):
    return_list = []
    for v in ret:
        if v and isinstance(v, (tuple, list)):
            table_name = v[0]
            message_list = v[1]
            s = check_list_ret_decode({table_name: [value.get('message') for value in message_list]})
            return_list.append(s)

    return return_list


def check_list_ret_decode(*args):
    _str = []
    for index, value in enumerate(args):
        if isinstance(value, (dict, tuple, list)):
            _str.append('{value}'.format(value=_check_list_ret_decode(value)))
        else:
            _str.append('{value}'.format(value=value))
    return ''.join(_str)


def _check_list_ret_decode(args, SpaceNum=0):
    _str = []
    SpaceNum += 1
    if isinstance(args, (tuple, list)):
        _str.append('')
        for index, value in enumerate(args):
            _str.append('{space}{value}'.format(value=_check_list_ret_decode(value, SpaceNum),
                                                space=get_space(SpaceNum)))
    elif isinstance(args, dict):
        _str.append('')
        for key, value in args.items():
            _str.append('{key}: {space}{value}'.format(key=key, value=_check_list_ret_decode(value, SpaceNum),
                                                       space=get_space(SpaceNum)))
    else:
        _str.append(str(args))

    return '\n'.join(_str)