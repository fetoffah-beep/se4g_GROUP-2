# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 00:15:43 2020

@author: sahar
"""


import psycopg2 
import seaborn as sns
import matplotlib.pyplot as plt  
import pandas as pd  
#connection to postgres  
con = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1",port="5432", database="SE4G")
#cursor
cur = con.cursor()
#execute querys
cur.execute('SELECT  "Vm", "WaA", "Wbuf", "PLOS" FROM public."Enhanced_PLOS"')
rows= cur.fetchall()
for r in rows:
    print(f" Vm {r[0]}, WaA{r[1]}, Wbuf{r[2]}, PLOS{r[3]}")
#close cursor
cur.close()
#close the connection
con.close()
df=pd.DataFrame(rows,columns=[ "Vm", "WaA", "Wbuf", "PLOS"])
#plot 
#histogram
f , axes = plt.subplots (2, 2, figsize =(7, 7), sharex =False)
sns.distplot (df["Vm"], bins=20 ,color="blue", ax= axes [0,0])
sns.distplot (df["WaA"] , bins=20 ,color="green", ax=axes [0,1])
sns.distplot ( df["Wbuf"] ,bins=20 , color="orange", ax=axes [1,0])
sns.distplot ( df["PLOS"], bins=20 , color="red", ax=axes [1,1])
#Correlogram without regression
sns.pairplot (df, kind='scatter')
#Correlogram with regression
sns.pairplot (df , kind='reg')
#pairplot
sns.pairplot (df, kind='scatter', hue='PLOS', plot_kws=dict (s=80,edgecolor ='white', linewidth=2.5))
#PairGrid
g = sns.PairGrid(df)
g.map_diag(sns.kdeplot)
g.map_offdiag(sns.kdeplot, n_levels=6);

