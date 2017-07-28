import sys
sys.path.append('/home/liusida/ipython/fund_scanner/packages')

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