import pymysql
import pandas as pd


#sql 연결
f = open('/opt/ml/mysql.txt',"r")
host = f.readline().strip()
user = f.readline().strip()
password = f.readline().strip()

conn = pymysql.connect(host=host, user=user, password=password, db='nftdb', charset='utf8')
cursor = conn.cursor()

# trade 불러오기
cursor.execute("Select * from ntfdb.TRADE")
data=cursor.fetchall() 
trade=pd.DataFrame(data)

# item 불러오기
cursor.execute("Select * from ntfdb.ITEM")
data2=cursor.fetchall() 
item=pd.DataFrame(data2)

# $가 있는 것만 뽑기
dollar=[]
for i in trade.iloc[:,7]:
    if '$' in i:
        dollar.append(True)
    else:
        dollar.append(False)

trade2=trade.iloc[dollar,[5,7]]

# price float로 저장
price=[]
for i in trade2.iloc[:,1]:
    print(i)
    if ',' in i:
        price.append(float(''.join(i[i.index('$')+1:-1].split(','))))
    else:
        price.append(float(i[i.index('$')+1:-1]))

trade2['price']=price

# 중복 제거 하기 위해 평균값 사용
trade3=trade2.groupby('5').agg({'price':'mean'})

del item[0]
del item[3]
del item[4]
del item[5]
del item[6]
del item[7]

# item과 trade 합쳐서 새로운 csv 만들기
df = pd.merge(item, trade3, left_on=1, right_on='5', how='left')


df.columns=['id','artifact', 'is_artifact', 'category', 'eastern_resource', 'environment', 'koda_clothing', 'is_koda_clothing', 'koda_core', 'koda_eyes', 'koda_head', 'is_koda_mega', 'koda_weapon', 'is_koda_weapon', 'koda_id', 'is_koda', 'northern_resource', 'sediment', 'southern_resource', 'western_resource', 'easteren_resource', 'environment_tier', 'koda', 'northern_resource_tier', 'plot', 'sediment_tier', 'southern_resource_tier', 'western_resource_tier', 'eastern_resource_tier','price']
df2=df[['artifact','category', 'eastern_resource', 'environment', 'koda_clothing', 'koda_core', 'koda_eyes', 'koda_head', 'koda_weapon', 'is_koda', 'northern_resource', 'sediment', 'southern_resource', 'western_resource', 'easteren_resource' ]]

# 확률 구하기
len_df2=len(df2)
d={}
for j in range(len(df2.columns)):
    for i in df2.iloc[:,j].unique():
        if i != 'None':
            d[i]=len(df2[df2.iloc[:,j] == i])/len_df2

# None을 1로 바꾸기
d[None]=1

# id 와 price 추가하여 dataframe만들기
df3 = pd.DataFrame()
for i in ['artifact','category', 'eastern_resource', 'environment', 'koda_clothing', 'koda_core', 'koda_eyes', 'koda_head', 'koda_weapon', 'is_koda', 'northern_resource', 'sediment', 'southern_resource', 'western_resource', 'easteren_resource']:
    df3[i] = df2[i].map(d)
df3['id'] = df['id']
df3['price'] = df['price']
df3[['id','artifact','category', 'eastern_resource', 'environment', 'koda_clothing', 'koda_core', 'koda_eyes', 'koda_head', 'koda_weapon', 'is_koda', 'northern_resource', 'sediment', 'southern_resource', 'western_resource', 'easteren_resource','price']]

# csv저장
df3.to_csv('pro.csv', index = False)
