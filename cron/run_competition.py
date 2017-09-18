import pandas as pd
import math
import gc
from IPython.display import display, HTML

import base
import fund_scanner.common_tools.database as db
import fund_scanner.common_tools.my_weixin as wx

engine = db.get_sqlalchemy_engine()
#
# 准备所有参赛者

sql = 'select * from funds a left join funds_update b on a.funds_id=b.funds_id'

df_all_candidates = pd.read_sql(sql, engine).iloc[:,[0,1,2,3,4,5,11]]

df_all_candidates = df_all_candidates.set_index('funds_id')

df_all_candidates['last_price'] = math.nan
df_all_candidates['current_price'] = math.nan
df_all_candidates['gain_ratio'] = math.nan
df_all_candidates['good'] = 0
good = {
    'not_in_yet' : 0,
    'healthy' : 1,
    'hurt_once' : 2,
    'hurt_twice' : 3,
    'out' : 10,
    'noway' : 11
    }
# good值:
#     0 : 未参赛
#     1 : 已参赛，正活跃
#     2 : 受伤 1次
#     3 : 受伤 2次
#     10 : 淘汰
#     11 : 没有参赛资格
# last_price: 上一轮净值
# current_price: 这一轮净值
# gain_ratio: 这一轮涨幅
df_all_candidates['current_ranking'] = 0
df_all_candidates['total_ranking'] = 0

df_all_candidates = df_all_candidates.sort_values('funds_start_date')

#df_all_candidates.tail(3)

#
# game2 游戏规则
# 选择 2016年 前成立的老基金们参赛，从 2016年 开始，每 14天 比一次净值的涨幅，
# 累加每一次比赛得到的排名
# 一直跑到 today，
# 返回所有参赛基金的排名积分的累加

def game2(funds_start_date='2016-1-1', competition_start_date='2016-1-1', competition_end_date='today',
          competition_time_span=14, watching_code=None):
    
    gc.collect()
    # 重新读取数据
    df_competition = df_all_candidates.copy()

    # 所有队伍先设置状态
    df_competition.loc[:,'good'] = good['healthy']
    
    # 2017年1月1日以后成立的基金或者没有写成立时间的基金没有参赛资格
    df_competition.loc[df_competition['funds_start_date']>pd.to_datetime(funds_start_date), 'good'] = good['noway']
    df_competition.loc[df_competition['funds_start_date'].isnull(),'good'] = good['noway']

    #资产规模小于1亿，或者没有数据的没有资格参赛
    df_competition.loc[df_competition['funds_amount']<1, 'good'] = good['noway']
    df_competition.loc[df_competition['funds_amount'].isnull(),'good'] = good['noway']

    df_competition = df_competition[df_competition['good']==good['healthy']]
    #参赛队伍准备完毕

    
    #比赛从最早一直基金成立开始
    #start_point = pd.to_datetime(df_competition.iloc[0,3])
    #比赛从2013年1月1日开始
    start_point = pd.to_datetime(competition_start_date)
    round_count = 1
    current_date = start_point
    while current_date < pd.to_datetime(competition_end_date):
        df_current_price = pd.read_sql('select * from funds_historical_price where funds_price_date=\'%s\''%current_date, engine)
        if len(df_current_price)<10:
            current_date = current_date + pd.DateOffset(1)
            continue

        # 把当前价格设为上一期价格
        df_competition['last_price'] = df_competition['current_price']
        # 设置当天价格（如果当天没几个价格就查次日的）
        df_current_price = df_current_price.set_index('funds_id')
        df_competition['current_price'].update(df_current_price['funds_price_adjust'])

        # 如果价格从非0到有，则说明价格变化了，计算变化率
        df_competition['gain_ratio'] = \
        ( df_competition['current_price'] - df_competition['last_price'] ) / df_competition['last_price']

        # 按变化率排序，累加排名
        df_competition = df_competition.sort_values('gain_ratio', ascending=True)
        df_competition = df_competition.assign(current_ranking=[i for i in range(len(df_competition))])
        df_competition.loc[df_competition['gain_ratio']>-100, 'total_ranking'] = df_competition['total_ranking'] + df_competition['current_ranking'] - len(df_competition)/2
        
        print('Round %d: %s'% (round_count, current_date))

        round_count += 1
        current_date = current_date + pd.DateOffset(competition_time_span)

        # 观测特定基金的状态
        if watching_code is not None:
            if type(watching_code) == list:
                display(df_competition.loc[df_competition['funds_code'].isin(watching_code), :].sort_index())
            elif type(watching_code) == str:
                display(df_competition.loc[df_competition['funds_code'] == (watching_code), :])
            else:
                pass


    # The winner is (return the full list, and the winner is on the top with highest ranking):
    return df_competition.loc[df_competition['good']==good['healthy']].sort_values('total_ranking', ascending=False)

df = game2()

winner = df.head(10).loc[:, ['funds_code', 'funds_name_full']]
msg = ''
for i,r in winner.iterrows():
    msg += '\n' + (r['funds_code'] + ' => ' + r['funds_name_full'])
    
print(msg)

wx.send(msg)


