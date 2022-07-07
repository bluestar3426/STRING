import time
time_start=time.time()

import pandas as pd

df=pd.read_csv('9606_experimental.csv')

pos=df.loc[:, 'protein1':'protein2']
pos['protein1']=pos['protein1'].replace(r'\D', r'', regex=True)
pos['protein2']=pos['protein2'].replace(r'\D', r'', regex=True)
quer=0
for index, row in pos.iterrows():
    if row['protein1']>row['protein2']:
        quer=row['protein1']
        row['protein1']=row['protein2']
        row['protein2']=quer
    else:
        continue

pos=pos.sort_values(by=['protein1', 'protein2'])
pos=pos.drop_duplicates(keep='first').reset_index(drop=True)

nonrpt_prot=[]
cnt=0
for i in range(0, len(df['protein1'])):
    if df['protein1'][i] not in nonrpt_prot:
        nonrpt_prot.append(df['protein1'][i])
        cnt+=1
		
from itertools import combinations

def combines(pro, r):
    return list(combinations(pro, r))

r=2
raw_list=combines(nonrpt_prot, r)
rd_smp=pd.DataFrame(raw_list, columns=['protein1', 'protein2'])

rd_smp['protein1']=rd_smp['protein1'].replace(r'\D', r'', regex=True)
rd_smp['protein2']=rd_smp['protein2'].replace(r'\D', r'', regex=True)

neg = pd.concat([pos, rd_smp])
neg = neg.drop_duplicates(keep=False)

neg=neg.reset_index(drop=True)

for index, row in pos.iterrows():
    new1=row['protein1'].find('00000')
    row['protein1']=row['protein1'][:new1]+'.ENSP'+row['protein1'][new1:]
    new2=row['protein2'].find('00000')
    row['protein2']=row['protein2'][:new2]+'.ENSP'+row['protein2'][new2:]
create_pos=pos.to_csv('pos.csv', index=False)

for index, row in neg.iterrows():
    new1=row['protein1'].find('00000')
    row['protein1']=row['protein1'][:new1]+'.ENSP'+row['protein1'][new1:]
    new2=row['protein2'].find('00000')
    row['protein2']=row['protein2'][:new2]+'.ENSP'+row['protein2'][new2:]
create_neg=neg.to_csv('neg.csv', index=False)

time_end=time.time()
time_c=time_end-time_start
print('time cost', time_c, 's')
