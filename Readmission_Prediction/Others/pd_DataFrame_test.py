import pandas as pd

RESULT_FILE = '/Users/shanewang/Desktop/test.csv'
ROW = ['I','II','III','IV']
COL = ['a','b','c','d']

# Value stored in column style
file = [[1,2,3,4], [5,6,7,8], [9,8,7,6], [5,4,3,2]]
data = dict()

for col in COL:
    data[col] = file[COL.index(col)]

df = pd.DataFrame(data=data, index=ROW)

'''
	a	b	c	d
I	1	5	9	5
II	2	6	8	4
III	3	7	7	3
IV	4	8	6	2
'''

# Value stored in row style
data = {i : 0 for i in COL}

df = pd.DataFrame(data=data, index=ROW)
for i in range(len(file)):
    f = file[i]
    for j in range(len(COL)):
        df.loc[[ROW[i]], [COL[j]]] = f[j]
'''
	a	b	c	d
I	1	2	3	4
II	5	6	7	8
III	9	8	7	6
IV	5	4	3	2
'''

df.to_csv(RESULT_FILE)