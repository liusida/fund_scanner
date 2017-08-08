import lxml.html as LH
import pandas as pd
import datetime

import base
import fund_scanner.common_tools.database as db
engine = db.get_sqlalchemy_engine(dbname='stock_index')

import logging
import fund_scanner.common_tools.logger as logger
log = logging.getLogger('get_indexes')


hour = datetime.datetime.now().hour
if hour>8 and hour<16:
    print('Please run this file after 16:00.')
    exit(1)

url_1 = 'http://data.10jqka.com.cn/funds/hyzjl/field/tradezdf/order/desc/page/1/ajax/1/'
url_2 = 'http://data.10jqka.com.cn/funds/hyzjl/field/tradezdf/order/desc/page/2/ajax/1/'

def get_dataframe(url):
    table = LH.parse(url)
    for df in pd.read_html(url, encoding='GB2312'):
        df['index_code'] = table.xpath('//tr/td[contains(@class, "tl")]/a/@href')
        df['index_code'] = df['index_code'].str.extract(r'/code/(\d+)/', expand=False)
        df['涨跌幅'] = df['涨跌幅'].str.extract(r'(.*?)%$', expand=False)
        df['涨跌幅.1'] = df['涨跌幅.1'].str.extract(r'(.*?)%$', expand=False)
    return df.set_index('序号')

df_1 = get_dataframe(url_1)
df_2 = get_dataframe(url_2)

df = pd.concat([df_1,df_2])
df['发布日期'] = pd.to_datetime('today')

row_to_compare = 1
index_name = df.loc[row_to_compare,'index_code']
df_sql = pd.read_sql('select * from stock_indexes where `index_code`=%s order by `发布日期` desc limit 1'%index_name, engine)

def write_to_sql(dataframe):
    try:
        df.to_sql('stock_indexes', engine, if_exists='append')
        log.info('{} rows inserted.'.format(len(dataframe)))
    except:
        log.info('Mysql Error.')


if len(df_sql)==0:
    write_to_sql(df)
else:
    if df_sql.loc[0,'行业指数']==df.loc[row_to_compare,'行业指数'] and df_sql.loc[0,'涨跌幅']==float(df.loc[row_to_compare,'涨跌幅']):
        log.info('already found some same record.')
    else:
        write_to_sql(df)
