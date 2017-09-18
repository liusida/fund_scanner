import matplotlib
matplotlib.rcParams['backend'] = 'TkAgg'

import pandas as pd
import os
from IPython.display import display,HTML
from ipywidgets import IntProgress

sh_datapath = '/home/liusida/ipython/fund_scanner/data/a_stock/XSHG/'
sz_datapath = '/home/liusida/ipython/fund_scanner/data/a_stock/XSHE/'
pickle_path = '/home/liusida/ipython/fund_scanner/data/a_stock/a_stock_price_total.pickle'

def read_price_from_pickle():
    df_price_total = pd.read_pickle(pickle_path)
    return df_price_total

df = read_price_from_pickle()

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d

m_pca = PCA(n_components=50)
m_tsne = TSNE(n_components=3)
result = m_pca.fit_transform(df.fillna(-1).T)
result = m_tsne.fit_transform(result)

result = pd.DataFrame(result)
display(result.info())

fig = plt.figure(figsize=[16,9])
ax = axes3d.Axes3D(fig)
ax.scatter(result[0], result[1], result[2])
plt.show()

result['name'] = df.columns

fig = plt.figure(figsize=[64, 48])
ax = axes3d.Axes3D(fig)
# ax.text3D(result[0], result[1], result[2], result['name'])
for i in range(len(result)):
    f = str(result['name'][i])[0]
    if f == '6':
        bcolor = (1, 0.8, 0.8, 1)
        edgecolor = (0.8, 0.5, 0.5, 1)
    elif f == '3':
        bcolor = (0.8, 1, 0.8, 1)
        edgecolor = (0.5, 0.8, 0.5, 1)
    else:
        bcolor = 'white'
        edgecolor = (0.8, 0.8, 0.8, 1)
    ax.text3D(result[0][i], result[1][i], result[2][i], result['name'][i],
              bbox=dict(facecolor=bcolor, edgecolor=edgecolor, alpha=0.7))
    if i > 10000:
        break
    print('\r%d'%i, end='\r')

ax.set_xlim(result[0].min(), result[0].max())
ax.set_ylim(result[1].min(), result[1].max())
ax.set_zlim(result[2].min(), result[2].max())
plt.show()