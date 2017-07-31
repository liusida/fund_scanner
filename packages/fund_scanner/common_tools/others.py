# Need to be moved to formal modules

import math

def extract_percentage(s, key):
    ret = None
    try:
        ret = float(s[key].strip('%'))
        if math.isnan(ret):
            ret = None
    finally:
        return ret

def extract_float(s, key):
    ret = None
    try:
        ret = float(s[key])
        if math.isnan(ret):
            ret = None
    finally:
        return ret

#正则中代表一个中英文字符、数字及常用符号
def re_utf_char():
    return '[\u4e00-\u9fa5|a-z|A-Z|0-9|\-\.]+'

def re_numbers():
    return '[-+]?[0-9]*\.?[0-9]+'