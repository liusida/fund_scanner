import pandas as pd
import logging
#from IPython.display import display, HTML

import base
import fund_scanner.common_tools.logger as logger
import fund_scanner.business.grab_data as grab_data
import fund_scanner.common_tools.database as db
engine = db.get_sqlalchemy_engine()

log = logging.getLogger('get_funds_detail')
#log.addHandler(logging.StreamHandler())

df = pd.read_sql('select * from `funds` order by `update_time` limit 1', engine)
funds_code = df['funds_code'].tolist()

log.info(funds_code)

grab_data.update_funds(funds_code)
