#!/usr/bin/env python
# coding: utf-8

# In[38]:


import pandas as pd                            #for analyzing data
import numpy as np                             #to work with numerical values
import matplotlib.pyplot as plt                #for creating visualization
import seaborn as sns                          #for plotting data
from wordcloud import WordCloud                #used to show which word is most frequently used
import squarify                                #for visualization
from collections import Counter                #for visualization


# In[17]:


zomato = pd.read_csv('Zomato_restaurants_in_india.csv')       #since the data is imported from my hardisk
zomato.head()                                                 


# Data Cleansing: To clean the raw we need to remove duplicate cells, need to delete the column which is not required for analyzing, need to remove null values and so on.

# In[19]:


#to delete the columns
zomato.drop(['res_id', 'address', 'latitude', 'longitude', 'locality_verbose',
       'timings', 'rating_text', 'delivery', 'takeaway'],axis=1,inplace=True)
zomato.columns


# In[20]:


print('No. of features:',zomato.shape[1],'\nNo. of resturants:',zomato.shape[0])


# In[21]:


zomato.isnull().sum()


# In[22]:


zomato.cuisines.fillna('NA',inplace=True)
zomato.cuisines = zomato.cuisines.apply(lambda x : x.split(sep=','))
zomato['establishment'] = zomato.establishment.apply(lambda x : 'NA' if x=='[]' else x[2:-2])


# In[23]:


#filtering only Chennai city restaurants
zch = zomato[zomato['city'] == 'Chennai']
print('No. of resturants in Chennai:',zch.shape[0])
zch.head()
zch.to_csv('mycsvfile.csv',index=False)


# In[24]:


rd_type = zch.establishment.value_counts().reset_index().set_index('index')
plt.figure(figsize=(8,8))
sns.barplot(x=rd_type.index,y=rd_type.establishment)
plt.xlabel('Restaurant Type')
plt.ylabel('Count')
plt.xticks(rotation='vertical')


# In[25]:


rd_loc = zch.locality.value_counts().head(20).reset_index().set_index('index') 
plt.figure(figsize=(8,8))
sns.barplot(x=rd_loc.index,y=rd_loc.locality)
plt.xlabel('Locality')
plt.ylabel('Number')
plt.xticks(rotation='vertical')


# In[26]:


rd_pr = zch.price_range.value_counts().reset_index().set_index('index') 
f,ax = plt.subplots(1,2,figsize=(20,10))
sns.barplot(x=rd_pr.index,y=rd_pr.price_range,ax=ax[1])
plt.xlabel('Price_Range')
plt.xticks(ticks=(0,1,2,3),labels=('Low','Medium','High','Very High'))
plt.ylabel('Count')
sns.distplot(zch.average_cost_for_two,ax=ax[0],color='r')


# In[27]:


zch_rat = zch[zch.aggregate_rating != 0]
f,ax=plt.subplots(1,2,figsize=(20,10))
sns.distplot(zch_rat.aggregate_rating,bins=20,kde=True,color='r',ax=ax[0])
sns.boxplot(zch_rat.aggregate_rating,ax=ax[1],color='r',saturation=0.5)


# In[32]:


lis = []
for i in range(0,zch.shape[0]):
    for j in zch.iloc[i,4]:
        lis.append(j)
for k in range(0,len(lis)):
    lis[k] = lis[k].strip()
    

cuisine_count = Counter(lis)

wc = WordCloud(background_color='white')
wc.generate_from_frequencies(cuisine_count)
plt.figure(figsize=(12,8))
plt.imshow(wc,interpolation='bilinear')
plt.axis('off')
plt.show()


# In[37]:



plt.figure(figsize=(18,10))
squarify.plot(sizes=zch.locality.value_counts().head(40),label=zch.locality.value_counts().head(40).index,
              color=sns.color_palette('RdYlGn_r',52))
plt.axis('off')


# In[ ]:




