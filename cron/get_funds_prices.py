import base

import sys
import pandas as pd
import json
from collections import namedtuple
import re
import ngender
from bs4 import BeautifulSoup
import numpy as np
import urllib
import time

# my private modules
import fund_scanner.database
import fund_scanner.readurl

url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=%s&page=1&per=10000&sdate=&edate=&rt='+str(time.time())

print(url)

def read_funds_historical_price( funds_code='000001' ):
    print('reading ', funds_code)
    ret = {}
    body = fund_scanner.readurl.simple_read_from_url(url%funds_code)
    body = body[re.search('{', body).start():]
    insider = re.search('\"(.*?)\"', body).group(1)
    return pd.read_html(insider)

def load_funds_price(funds_code='540006', funds_id=4269):

    dfs = read_funds_historical_price(funds_code)

    df = dfs[0]

    with fund_scanner.database.get_connection() as cursor:

        for index, row in df.iterrows():
            #print(row['净值日期'])
            sql = 'INSERT ignore INTO `funds_historical_price` '+\
            '(`funds_id`, `funds_price_date`, `funds_price`, `funds_price_adjust`, `funds_raising_percentage`) '+\
            'VALUES (%s,%s,%s,%s,%s)'
            cursor.execute(sql, (funds_id, row['净值日期'], 
                                 base.extract_float(row, '单位净值'), base.extract_float(row, '累计净值'), 
                                 base.extract_percentage(row, '日增长率')))

            sql = 'Update `funds` set `historical_price_time`=Now() where `funds_id`=%s'
            cursor.execute(sql, (funds_id))






with fund_scanner.database.get_connection() as cursor:
    sql = 'Select * from funds order by historical_price_time limit 0,10'
    cursor.execute(sql)
    result = cursor.fetchall()

for row in result:
    time.sleep(3)
    load_funds_price(funds_code=row['funds_code'], funds_id=row['funds_id'])
