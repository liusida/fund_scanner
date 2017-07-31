import pandas as pd
from IPython.display import display, HTML

import base
import fund_scanner.business.grab_data as grab_data
import fund_scanner.common_tools.database as db
engine = db.get_sqlalchemy_engine()

df = pd.read_sql('select * from `funds` order by `update_time` limit 5', engine)
funds_code = df['funds_code'].tolist()
print(funds_code)

grab_data.update_funds(funds_code)
