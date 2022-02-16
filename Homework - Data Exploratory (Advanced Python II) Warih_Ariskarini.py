#!/usr/bin/env python
# coding: utf-8

# ### 1. Checking Introductory Details About Data

# data ini berupa atribut-atribut yang memicu penyakit jantung pada pasien

# ### 2. Statistical Insight dan Data Cleaning

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


data = pd.read_csv("heart.csv")
data = data.reset_index(drop=True)


# In[3]:


#pada data ini diambil atribut age, sex, trestbps, chol
data = data[['age','sex','trestbps','chol','thalach']]
data


# In[4]:


data_1 = data[['age','trestbps','chol']]
#merename kolom agar lebih mudah dipahami

data_1 = data_1.rename(columns={"trestbps":"tekanan_darah", "chol":"kolesterol"})
data_1


# In[5]:


data_1.describe()


# orang yang terkena penyakit jantung rata-rata berumur 54 tahun, memiliki tekanan darah 131 mm Hg saat masuk ke rumah sakit serta
# memiliki kadar kolesterol 246 mg/dl

# In[6]:


data_3 = data[['age','sex']]
data_3


# In[7]:


total = data_3.groupby('sex').count()
total = total.rename(columns={"age":"banyaknya_orang"})
total


# In[8]:


i = 0 
while i < len(total):
    jk = total.loc[i,'banyaknya_orang']
    jumlah = total.loc[0,'banyaknya_orang']+total.loc[1,'banyaknya_orang']
    total.loc[i,'presentase'] = jk*100/jumlah
    i=i+1
total


# keterangan 0 untuk perempuan dan 1 untuk laki-laki 

# penderita penyakit jantung 68 persen diantaranya adalah laki-laki sedangkan perempuan 32 persen. 

# ## 3. Data Visualization

# In[9]:


from matplotlib import pyplot
data_2 = data[['trestbps','chol','thalach']]
data_2 = data_2.rename(columns={"trestbps":"tekanan_darah", "chol":"kolesterol","thalach":"detak_jantung" })
data_2
data_2.plot()
pyplot.xlabel('pasien')
pyplot.ylabel('kadar')
pyplot.show()


# pasien penderita penyakit jantung cenderung memiliki kolesterol yang tinggi 

# In[ ]:




