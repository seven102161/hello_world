import json
import pandas as pd
import openpyxl
from xlwt import Workbook


data = open('an_business.json', encoding='utf-8').read()
house_info = json.loads(data)
df = pd.DataFrame(data=house_info, index=[i+1 for i in range(len(house_info))])

# print(df.shape)
'''
(20, 6)
'''

# print(df.columns)
'''
Index(['building', 'floor', 'address', 'size', 'daily_price', 'monthly_price'], dtype='object')
'''

# print(df.describe())
'''
Index(['building', 'floor', 'address', 'size', 'daily_price', 'monthly_price'], dtype='object')
       building    floor          address   size daily_price monthly_price
count        20       20               20     20          20            20
unique        3        7                9     15          11            15
top     青岛国际创新园  中区/共25层  崂山 青岛二中 松岭路169号  240m²   1.7元/m²/天      10.35万/月
freq         11        7                6      2           4             2
'''

# df.info()
'''
<class 'pandas.core.frame.DataFrame'>
Int64Index: 20 entries, 1 to 20
Data columns (total 6 columns):
 #   Column         Non-Null Count  Dtype 
---  ------         --------------  ----- 
 0   building       20 non-null     object
 1   floor          20 non-null     object
 2   address        20 non-null     object
 3   size           20 non-null     object
 4   daily_price    20 non-null     object
 5   monthly_price  20 non-null     object
dtypes: object(6)
memory usage: 1.1+ KB
'''

# print(df.head())
'''
  building    floor          address   size daily_price monthly_price
1  青岛国际创新园  中区/共25层  崂山 青岛二中 松岭路169号  376m²     2元/m²/天       2.26万/月
2  青岛国际创新园  高区/共26层  崂山 青岛二中 松岭路169号   95m²   1.4元/m²/天       3990元/月
3  青岛国际创新园  中区/共25层  崂山 汽车东站 松岭路169号  240m²   2.2元/m²/天       1.58万/月
4  青岛国际创新园  高区/共25层  崂山 青岛二中 松岭路169号  740m²  1.15元/m²/天       2.55万/月
5  青岛国际创新园  高区/共24层  崂山 青岛二中 松岭路169号  191m²   1.6元/m²/天       9168元/月
'''

# print(df['building'].unique())
'''
['青岛国际创新园' '不可分割' '可分割']
'''
df.loc[df['building'] != '青岛国际创新园', 'building'] = '青岛国际创新园'
# print(df['building'].unique())
'''
['青岛国际创新园']
'''


# 查看去重后的floor列
# print(df['floor'].unique())
'''
['中区/共25层' '高区/共26层' '高区/共25层' '高区/共24层' '中区/共20层' '中区/共31层' '85.0%']
'''

# 删除楼层信息为"85%"的行
mask = df['floor'] == '85.0%'
df.drop(labels=mask.index[mask], axis=0, inplace=True)
# print(df['floor'].unique())
'''
['中区/共25层' '高区/共26层' '高区/共25层' '高区/共24层' '中区/共20层' '中区/共31层']
'''

# 拆分楼层信息
df['area'] = df['floor'].transform(lambda x: x.split('/共')[0])
df['total_floors'] = df['floor'].transform(lambda x: x.split('/共')[1])
# print(df['area'].unique())
'''
['中区' '高区']
'''

# print(df['total_floors'].unique())
'''
['25层' '26层' '24层' '20层' '31层']
'''

# 删除"floor"列
df.drop(labels=['floor'], axis=1, inplace=True)

# df.info()
'''
<class 'pandas.core.frame.DataFrame'>
Int64Index: 19 entries, 1 to 20
Data columns (total 7 columns):
 #   Column         Non-Null Count  Dtype 
---  ------         --------------  ----- 
 0   building       19 non-null     object
 1   address        19 non-null     object
 2   size           19 non-null     object
 3   daily_price    19 non-null     object
 4   monthly_price  19 non-null     object
 5   area           19 non-null     object
 6   total_floors   19 non-null     object
dtypes: object(7)
memory usage: 1.2+ KB
'''

# 查看地址信息情况
# print(df['address'].unique())
'''
['崂山 青岛二中 松岭路169号' '崂山 汽车东站 松岭路169号' '8.97元/m²/月' '面议' '崂山 北村 松岭路169号'
 '崂山 北村 山东省青岛市崂山区新锦路' '崂山 中韩 青岛国际创新园' '8.7元/m²/月' '8.96元/m²/月']
'''

# 查看其他要素是否缺失
# print(df.loc[df['address'] == '面议', ('size', 'daily_price', 'monthly_price')])
# print('-------')
# print(df.loc[df['address'] == '8.97元/m²/月', ('size', 'daily_price', 'monthly_price')])
# print('-------')
# print(df.loc[df['address'] == '8.7元/m²/月', ('size', 'daily_price', 'monthly_price')])
# print('-------')
# print(df.loc[df['address'] == '8.96元/m²/月', ('size', 'daily_price', 'monthly_price')])

'''
      size daily_price monthly_price
7    376m²     2元/m²/天       2.26万/月
10  1500m²   2.3元/m²/天      10.35万/月
12   145m²   1.1元/m²/天       4785元/月
-------
     size daily_price monthly_price
6  1500m²   2.3元/m²/天      10.35万/月
-------
     size daily_price monthly_price
15  580m²   2.5元/m²/天       4.35万/月
-------
         size daily_price monthly_price
18      558m²   1.8元/m²/天       3.01万/月
19  1253.59m²   1.7元/m²/天       6.39万/月
20      315m²   1.8元/m²/天        1.7万/月
'''

# 地址缺失信息修改为"未知"
wrong_address = ['面议', '8.97元/m²/月', '8.7元/m²/月', '8.96元/m²/月']

for i in wrong_address:
    df.loc[df['address'] == i, 'address'] = '未知'

# print(df['address'].unique())
'''
['崂山 青岛二中 松岭路169号' '崂山 汽车东站 松岭路169号' '未知' '崂山 北村 松岭路169号'
 '崂山 北村 山东省青岛市崂山区新锦路' '崂山 中韩 青岛国际创新园']
'''

# 面积处理

# 面积修改为数值型
df['size'] = df['size'].transform(lambda x: float(x.replace('m²', '')))
# print(df['size'].describe())
'''
count      19.000000
mean      660.422632
std       565.700249
min        95.000000
25%       240.000000
50%       376.000000
75%       996.795000
max      1700.000000
Name: size, dtype: float64
'''

# 面积数据离散化，等分切割为：[(0, 100] < (100, 500] < (500, 1000] < (1000, 2000]
df['size_range'] = pd.cut(df['size'], [0, 100, 500, 1000, 2000])
'''
Categories (4, interval[int64]): [(0, 100] < (100, 500] < (500, 1000] < (1000, 2000]]
'''
# print(df['size_range'])

# df.info()
'''
<class 'pandas.core.frame.DataFrame'>
Int64Index: 19 entries, 1 to 20
Data columns (total 8 columns):
 #   Column         Non-Null Count  Dtype   
---  ------         --------------  -----   
 0   building       19 non-null     object  
 1   address        19 non-null     object  
 2   size           19 non-null     float64 
 3   daily_price    19 non-null     object  
 4   monthly_price  19 non-null     object  
 5   area           19 non-null     object  
 6   total_floors   19 non-null     object  
 7   size_range     19 non-null     category
dtypes: category(1), float64(1), object(6)
memory usage: 1.4+ KB
'''

# 价格处理

# 日单价处理
# print(df['daily_price'].describe())
'''
count            19
unique           11
top       1.7元/m²/天
freq              4
Name: daily_price, dtype: object
'''

# 日单位修改为数值型（浮点型）
df['daily_price'] = df['daily_price'].transform(lambda x: float(x.replace('元/m²/天', '')))

# print(df['daily_price'].describe())
'''
count    19.000000
mean      1.844737
std       0.376716
min       1.100000
25%       1.700000
50%       1.800000
75%       2.100000
max       2.500000
Name: daily_price, dtype: float64
'''

# 月单位修改为数值型（浮点型）
# print(df['monthly_price'].describe())
'''
count          19
unique         15
top       8.67万/月
freq            2
Name: monthly_price, dtype: object
'''

# print(df['monthly_price'].unique())
'''
['2.26万/月' '3990元/月' '1.58万/月' '2.55万/月' '9168元/月' '10.35万/月' '8151元/月'
 '8.67万/月' '4785元/月' '2.73万/月' '4.35万/月' '2.16万/月' '3.01万/月' '6.39万/月'
 '1.7万/月']
'''
# 将单位"元/月"调整为"万/月"
yuan = []
for i in df['monthly_price'].unique():
    if '元' in i:
        yuan.append(i)

for k in yuan:
    new_price = float(k.split('元/月')[0])/ 10000
    df.loc[df['monthly_price'] == k, 'monthly_price'] = str(new_price) + '万/月'

# print(df['monthly_price'].unique())
'''
['2.26万/月' '0.399万/月' '1.58万/月' '2.55万/月' '0.9168万/月' '10.35万/月'
 '0.8151万/月' '8.67万/月' '0.4785万/月' '2.73万/月' '4.35万/月' '2.16万/月' '3.01万/月'
 '6.39万/月' '1.7万/月']
'''

# 月单位修改为数值型（浮点型）
df['monthly_price'] = df['monthly_price'].transform(lambda x: float(x.replace('万/月', '')))
# print(df['monthly_price'].describe())
'''
count    19.000000
mean      3.748389
std       3.375167
min       0.399000
25%       1.580000
50%       2.260000
75%       5.370000
max      10.350000
Name: monthly_price, dtype: float64
'''

# 每平方月单价
df['monthly_price_size'] = df['monthly_price'] / df['size'] * 10000
# print(round(df['price_m_s'], 2))
# print(df['price_m_s'].describe())
'''
Name: price_m_s, dtype: float64
count    19.000000
mean     55.326816
std      11.294696
min      33.000000
25%      50.979854
50%      53.968254
75%      62.969858
max      75.000000
Name: price_m_s, dtype: float64
'''

# 最后的表格结果
# df.info()
'''
<class 'pandas.core.frame.DataFrame'>
Int64Index: 19 entries, 1 to 20
Data columns (total 9 columns):
 #   Column         Non-Null Count  Dtype   
---  ------         --------------  -----   
 0   building       19 non-null     object  
 1   address        19 non-null     object  
 2   size           19 non-null     float64 
 3   daily_price    19 non-null     float64 
 4   monthly_price  19 non-null     float64 
 5   area           19 non-null     object  
 6   total_floors   19 non-null     object  
 7   size_range     19 non-null     category
 8   price_m_s      19 non-null     float64 
dtypes: category(1), float64(4), object(4)
memory usage: 1.6+ KB
'''

# 保存到excel
# writer = pd.ExcelWriter('an.business.xlsx')
# columns参数的顺序就是excel的列顺序
# df为需要保存的DataFrame
# df.to_excel(writer, columns=['building', 'address', 'area', 'total_floors',
#                              'size', 'size_range', 'daily_price', 'monthly_price', 'price_m_s'],
#             index=False, encoding='utf-8', sheet_name='Sheet1')
# 生成csv文件
df.to_csv(r'./an.business.csv', columns=['building', 'address', 'area', 'total_floors',
                                         'size', 'size_range', 'daily_price', 'monthly_price', 'monthly_price_size'],
          index=False, sep=',')
# writer.save()
# writer.close()
