import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('an.business.csv', sep=',')

# df.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 19 entries, 0 to 18
Data columns (total 9 columns):
 #   Column              Non-Null Count  Dtype  
---  ------              --------------  -----  
 0   building            19 non-null     object 
 1   address             19 non-null     object 
 2   area                19 non-null     object 
 3   total_floors        19 non-null     object 
 4   size                19 non-null     float64
 5   size_range          19 non-null     object 
 6   daily_price         19 non-null     float64
 7   monthly_price       19 non-null     float64
 8   monthly_price_size  19 non-null     float64
dtypes: float64(4), object(5)
memory usage: 1.5+ KB
'''

print('-------------------------------------\n')
mean_area = (df.loc[:, ['area', 'daily_price', 'monthly_price_size']].groupby('area').mean())
mean_area = mean_area.reset_index()
print('按楼层区域划分: 【日单价（元/平方） 月单价（元/平方）】\n', mean_area)
print('-------------------------------------\n')

'''
按楼层区域划分【日单价（元/平方） 月单价（元/平方）】: 
   area  daily_price  monthly_price_size
0   中区     1.864286           55.910718
1   高区     1.790000           53.691892
'''

mean_floors = (df.loc[:, ['total_floors', 'daily_price', 'monthly_price_size']].groupby('total_floors').mean())
mean_floors = mean_floors.reset_index()
print('按最高楼层划分: 【日单价（元/平方） 月单价（元/平方）】\n', mean_floors)
print('-------------------------------------\n')

'''
按最高楼层划分: 【日单价（元/平方） 月单价（元/平方）】
   total_floors  daily_price  monthly_price_size
0          20层     1.860000           55.774123
1          24层     2.050000           61.500000
2          25层     1.872222           56.148766
3          26层     1.400000           42.000000
4          31层     1.700000           51.000000
'''

mean_size = (df.loc[:, ['size_range', 'daily_price', 'monthly_price_size']].groupby('size_range').mean())
mean_size = mean_size.reset_index()
print('按楼出租面积划分:【日单价（元/平方） 月单价（元/平方）】 \n', mean_size)
print('-------------------------------------\n')

'''
按楼出租面积划分: 【日单价（元/平方） 月单价（元/平方）】
      size_range  daily_price  monthly_price_size
0      (0, 100]     1.400000           42.000000
1    (100, 500]     1.866667           55.983076
2  (1000, 2000]     1.940000           58.194721
3   (500, 1000]     1.787500           53.597054
'''


p1 = plt.figure(figsize=(12, 6))

p1.add_subplot(1, 2, 1)
plt.title('Distribution of Size')
size = df['size']
group = [i for i in range(0, 2000, 200)]
plt.hist(size, group)
plt.xticks(group)

p1.add_subplot(1, 2, 2)
plt.title('Monthly price per size')
x = df['size_range']
y = df['monthly_price_size']
plt.bar(x, y, color='sandybrown')
plt.xticks(x)

# plt.savefig('an_business.png')
# plt.show()
