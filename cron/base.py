import sys
sys.path.append('/home/liusida/ipython/fund_scanner/packages')

def extract_percentage(s, key):
    ret = None
    try:
        ret = float(s[key].strip('%'))
    finally:
        return ret

def extract_float(s, key):
    ret = None
    try:
        ret = float(s[key])
    finally:
        return ret