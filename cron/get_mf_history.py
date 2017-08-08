import pandas as pd
import logging
import time
#from IPython.display import display, HTML


import base
import fund_scanner.common_tools.logger as logger
import fund_scanner.common_tools.database as db
import fund_scanner.business.grab_data as grab_data
engine = db.get_sqlalchemy_engine()

log = logging.getLogger('get_mf_history')

url = 'http://fund.eastmoney.com/manager/%s.html'

with db.get_connection() as cursor:
    sql = 'select * from managers order by funds_history_update_time limit 3 '
    cursor.execute(sql)
    managers = cursor.fetchall()
    
    for manager in managers:
        log.info(manager['managers_code'])

        managers_id = manager['managers_id']
        sql = 'UPDATE `managers` set funds_history_update_time=Now() where managers_id=%s;'
        cursor.execute(sql, (managers_id))

        df = pd.read_html(url%manager['managers_code'])[1]

        #len(df)
        try:
            if df.iloc[0,-1][-1] != '%' and df.iloc[0,-1][-1] != '-':
                log.info('抓取到的格式错误！')
                display(df)
                continue
        except:
            log.info('other error.')
            continue
        df['start_date'] = df.loc[:,'任职时间'].apply(lambda x: x.split(' ~ ')[0])
        df['end_date'] = df.loc[:,'任职时间'].apply(lambda x: x.split(' ~ ')[1].replace('至今', '2222-2-2'))
        df['funds_code'] = df.loc[:,'基金代码'].apply(lambda x: str(x).zfill(6))

        codes = df['基金代码'].tolist()
        codes = ','.join([str(w) for w in codes])

        df_funds = pd.read_sql('select * from funds where funds_code in (%s)'%(codes), engine)

        df = pd.merge(df, df_funds, on='funds_code', how='left')

        funds_need_update = df[df['funds_type'].isnull()]['funds_code'].tolist()
        if len(funds_need_update)>1:
            grab_data.update_funds(funds_need_update)
            time.sleep(1)

        df_funds = pd.read_sql('select * from funds where funds_code in (%s)'%(codes), engine)

        df = pd.merge(df, df_funds, on='funds_code', how='inner')

        #display(df)
        
        for row in df.iterrows():
            
            start_date = row[1]['start_date']
            end_date = row[1]['end_date']
            funds_id = row[1]['funds_id_x']
            sql = 'INSERT INTO `managers_2_funds_history` (managers_id, funds_id, history_start_date, history_end_date) VALUES (%s, %s, %s, %s) '\
            'ON DUPLICATE KEY UPDATE history_end_date=%s;'
            #log.info(sql%(managers_id, funds_id, start_date, end_date, end_date))
            cursor.execute(sql, (managers_id, funds_id, start_date, end_date, end_date))
            



