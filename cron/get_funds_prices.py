import base

import sys
import json
from collections import namedtuple
import re
import ngender
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import logging

# my private modules
import fund_scanner.common_tools.logger as logger
import fund_scanner.common_tools.database as db
import fund_scanner.common_tools.readurl
import fund_scanner.common_tools.others as o

log = logging.getLogger('get_funds_prices')

url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=%s&page=1&per=30&sdate=&edate=&rt='+str(time.time())

def read_funds_historical_price( funds_code='000001' ):
    print('reading ', funds_code)
    ret = {}
    body = fund_scanner.common_tools.readurl.simple_read_from_url(url%funds_code)
    body = body[re.search('{', body).start():]
    insider = re.search('\"(.*?)\"', body).group(1)
    return pd.read_html(insider)

def load_funds_price(funds_code='540006', funds_id=4269):

    dfs = read_funds_historical_price(funds_code)
    df = dfs[0]

    with db.get_connection() as cursor:

        for index, row in df.iterrows():
            try:
                #print(row['净值日期'])
                sql = 'INSERT ignore INTO `funds_historical_price` '+\
                '(`funds_id`, `funds_price_date`, `funds_price`, `funds_price_adjust`, `funds_raising_percentage`) '+\
                'VALUES (%s,%s,%s,%s,%s)'
                cursor.execute(sql, (funds_id, row['净值日期'], 
                                     o.extract_float(row, '单位净值'), o.extract_float(row, '累计净值'), 
                                     o.extract_percentage(row, '日增长率')))
            finally:
                sql = 'Update `funds` set `historical_price_time`=Now() where `funds_id`=%s'
                cursor.execute(sql, (funds_id))

with db.get_connection() as cursor:
    sql = 'Select * from funds order by historical_price_time limit 1'
    cursor.execute(sql)
    result = cursor.fetchall()

for row in result:
    time.sleep(1)
    log.info(row['funds_code'])
    load_funds_price(funds_code=row['funds_code'], funds_id=row['funds_id'])
