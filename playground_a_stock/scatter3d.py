cache_path  = '/home/liusida/ipython/fund_scanner/data/a_stock/cache.pickle'
import pandas as pd
result = pd.read_pickle(cache_path)

import base
import fund_scanner.animation_framework.framework as fw

dots = [fw.FWDot(color='blue', pos_x=row[1][0], pos_y=row[1][1], pos_z=row[1][2]) for row in result.head(5).iterrows()]

stageArea=[[result[0].min()*1.1, result[0].max()*1.1],
           [result[1].min()*1.1, result[1].max()*1.1],
           [result[2].min()*1.1, result[2].max()*1.1]]
movie = fw.FWMovie(frame_num=5, stageArea=stageArea)
movie.add_objects(dots)
movie.display_movie(rotate=True)