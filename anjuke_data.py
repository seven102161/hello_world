import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = open('an_house.json', encoding='utf-8').read()

house_info = json.loads(data)
# print(len(house_info))

df = pd.DataFrame(data=house_info, index=[i+1 for i in range(len(house_info))])
# print(df['size'])

df['size'] = df['size'].transform(lambda x: x.replace('m²', ''))

df['price'] = df['price'].astype('int64')
df['size'] = df['size'].astype('int64')

df_mean = (df[['type', 'size', 'price']].groupby('type').mean())
df_mean = df_mean.reset_index()
print(df_mean)
print('------------')
print(df['size'].describe())

#
# plt.figure()
#
# #修改字体：
# plt.rcParams['font.sans-serif'] = 'SimHei'
# #正常显示符号问题：
# plt.rcParams['axes.unicode_minus'] = False
#
# x = [1, 2, 3]
# y = df_mean['price']
#
# plt.bar(x, y)
#
# plt.xticks(x, list(df_mean['type']))
#
# for x, y in zip(x, y):
#     plt.text(x, y+20, y, ha='center', fontsize=11)
#
# plt.show()
#
#
#
