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