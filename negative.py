import pandas as pd

df=pd.read_csv('9606_experimental_score900.csv')

#positive
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

for index, row in pos.iterrows():
    new1=row['protein1'].find('00000')
    row['protein1']=row['protein1'][:new1]+'.ENSP'+row['protein1'][new1:]
    new2=row['protein2'].find('00000')
    row['protein2']=row['protein2'][:new2]+'.ENSP'+row['protein2'][new2:]

#non-repeat protein numbers
nonrpt_prot=[]
cnt=0
for i in range(0, len(pos['protein1'])):
    if pos['protein1'][i] not in visited:
        nonrpt_prot.append(pos['protein1'][i])
        cnt+=1
print("Number of non-repeat proteins: ", cnt)

#random sampling
from itertools import combinations
def combines(pro, r):
    return list(combinations(pro, r))
  
r=2
raw_list=combines(nonrpt_prot, r)
rd_smp=pd.DataFrame(raw_list, columns=['protein1', 'protein2'])

#negative
neg = pd.concat([pos, rd_smp]).drop_duplicates(keep=False)
n1=neg.reset_index(drop=True)
print(n1)
