#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
pd.options.display.max_columns = 150
transaction_data = pd.read_csv('QVI_transaction_data.csv')
customer_data = pd.read_csv('QVI_purchase_behaviour.csv')


# In[2]:


merged_data = pd.merge(left = customer_data, right = transaction_data, how='left', on='LYLTY_CARD_NBR')
merged_data.info()


# In[3]:


merged_data = merged_data.drop(merged_data.columns[3:4], axis = 1)
merged_data.head()


# In[4]:


merged_data = merged_data.rename(columns = {'LYLTY_CARD_NBR':'ID','PREMIUM_CUSTOMER':'Customer Segment'})
merged_data.head()


# In[5]:


merged_data['Brand'] = merged_data['PROD_NAME'].str.split().str[0]
merged_data.head()


# In[6]:


merged_data['Customer Segment'].value_counts()


# In[7]:


merged_data['LIFESTAGE'].value_counts()


# ## Correlation of the data

# In[8]:


get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import matplotlib.pyplot as plt
correlation = merged_data.corr()
mask = np.triu(np.ones_like(correlation, dtype=np.bool))
f, ax = plt.subplots(figsize=(12, 9))
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(correlation, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})


# In[9]:


merged_data['PROD_QTY'].value_counts(normalize = True).sort_index()


# ## Customer chip size purchasing behaviour

# In[36]:


import re
pattern = r'(\d+)' #extract digits 
merged_data['Chip_size'] = merged_data['PROD_NAME'].str.extract(pattern, flags =re.I)
merged_data['Chip_size'] = merged_data['Chip_size'].astype(int)
merged_data['Chip_size'].value_counts(bins = 10).sort_index()
merged_data['Chip_size'].plot.hist(grid = True)
plt.xlabel('Chip Sizes (g)')
plt.title('Average Chip Size of Customer Segments')


# In[11]:


group_by_customer = merged_data.groupby("ID")
last_transaction = group_by_customer["Customer Segment"].max() #groups customer by customer segment 
best_cust = pd.DataFrame(last_transaction) #create dataframe
best_cust["nr_of_transactions"] = group_by_customer.size()
best_cust['amount_spent'] = group_by_customer['TOT_SALES'].sum() 
best_cust['Chips'] = group_by_customer['PROD_NAME'].unique()
best_cust['Family'] = group_by_customer['LIFESTAGE'].unique()
best_cust['size_of_chips'] = group_by_customer['Chip_size'].unique()
best_cust.head()


# ## Customer Rankings
#  ** (1/2 *Number of purchases) + (1/2 * Amount Spent)
#  
#  **Recale statistical formular X - Xmin / Xmax - Xmin**

# In[12]:


best_cust['scaled_tran'] = (best_cust['nr_of_transactions'] - best_cust['nr_of_transactions'].min())/(best_cust['nr_of_transactions'].max() - best_cust['nr_of_transactions'].min())
best_cust['scaled_amount'] = (best_cust['amount_spent'] - best_cust['amount_spent'].min())/(best_cust['amount_spent'].max() - best_cust['amount_spent'].min())
best_cust['score'] = ((best_cust['scaled_tran'] /2) + (best_cust['scaled_amount'] /2)) * 100
best_cust = best_cust.sort_values(by ='score', ascending = False)
best_cust['score'].describe()


# In[13]:


best_cust = best_cust.head(50)
customer_segment = best_cust['Customer Segment'].value_counts(normalize = True)
customer_segment.plot(kind ='barh', figsize = (10,5))
plt.title('Top 50 Customer Ranking based on total sales')


# ## Customer Segment Purchasing Behaviour

# In[14]:


family_Type = best_cust['Family'].value_counts()


# In[15]:


family_Type.plot(kind = 'pie', figsize=(10,5), autopct = '%.2f%%', title = 'Percentage of family who buys chips')
plt.ylabel('')


# In[16]:


Older_Families = merged_data[merged_data['LIFESTAGE'] == 'OLDER FAMILIES']
Older_Families['Chip_size'].plot.hist(grid = True)
plt.xlabel('Chip Sizes (g)')
plt.title('Purchasing behavior of Older Families')


# In[17]:


Young_Families = merged_data[merged_data['LIFESTAGE'] == 'YOUNG FAMILIES']
Young_Families['Chip_size'].plot.hist(grid = True)
plt.xlabel('Chip Sizes (g)')
plt.title('Purchasing Behavior of Young Families')


# In[18]:


retired = merged_data[merged_data['LIFESTAGE'] == 'RETIREES']
retired['Chip_size'].plot.hist(grid = True)
plt.xlabel('Chip Sizes (g)')
plt.title('Purchasing Behavior of Retirees')


# **Task 1**
# 
# Customer Segmentation is divided into three categories namely Premium, Mainstream and budget. With the implementation of the statistical analysis formular to identify high value customers, the histogram proves that the top 50 customers came from Budget and Midstream segments accounting for **73%** of the total high value customer segmentation. With a deep analysis on customer segmentation, older and younger families represent **72%** of total chips purchased with a packet size range of **132g to 194g** indicated in the histogram above. 
# 
# **Stragey**
# 
# 380g of Dorito Corn Chips(high margin brand products) should be marketed to Older Families that are premium customers. 
# 
# Premium customers purchase larger chip size packets with an average of 297g while Mainstream and Budget customers purchase an average packet size of 182g. 
# 
# Highest Sales came from MainStream & Budget Customers
# 
# **Pie chart illustrates the driving factor of sales for each family:**
# 
# 1) Most Premium customers are from Older Singles/Couples which represent 12% of the driving force of sales. The top 5 brands from this segments are Kettle, Smiths, Pringles, Doritos and Thins.
# 
# 2) 6% of the Driving factor of sales came from MainStream customer segments who are young singles/couples.The top 5 brands from this segments are kettle, Pringles, Doritos, Smiths and Thins. 
# 
# 3) Most Budget customers are from Older Families which represent 46% of the driving force of sales. The top 5 brands from this segments are Kettle, smiths, doritos, Pringles and RRD. 
# 
# 4) Bedget customer customers with older Families are more likely to purchase RRD chips compared to the rest of the population
# 
# 
# 
# 
# 

# In[19]:


Premium = merged_data[merged_data['Customer Segment'] =='Premium']
Mainstream = merged_data[merged_data['Customer Segment'] =='Mainstream']
Budget = merged_data[merged_data['Customer Segment'] =='Budget']
Premium['LIFESTAGE'].value_counts(normalize = True)
#premium with older singles/couples


# In[42]:


Premium_chips = merged_data[(merged_data['Customer Segment'] =='Premium') & (merged_data['LIFESTAGE'] == 'OLDER SINGLES/COUPLES')]
p = Premium_chips['Brand'].value_counts(normalize = True).head()
p.plot(kind ='barh', figsize = (10,5))
plt.title('Premium & Older Singles/Couples Top Purchasing Chip Brands')


# In[21]:


Premium['Chip_size'].describe()


# In[22]:


Mainstream['LIFESTAGE'].value_counts(normalize = True)
#Mainstream with Young single?couples


# In[41]:


Main_chips = merged_data[(merged_data['Customer Segment'] =='Mainstream') & (merged_data['LIFESTAGE'] == 'YOUNG SINGLES/COUPLES')]
m = Main_chips['Brand'].value_counts(normalize = True).head()
m.plot(kind ='barh', figsize = (10,5))
plt.title('Mainstream & Young Singles/Couples Top Purchasing Chip Brands')


# In[24]:


Mainstream['Chip_size'].describe()


# In[25]:


Budget['LIFESTAGE'].value_counts(normalize = True)
#Budget with older families


# In[40]:


Budget_chips =  merged_data[(merged_data['Customer Segment'] =='Budget') & (merged_data['LIFESTAGE'] == 'OLDER FAMILIES')]
b = Budget_chips['Brand'].value_counts(normalize = True).head()
b.plot(kind ='barh', figsize = (10,5))
plt.title('Budget & Older Family Top Purchasing Chip Brands')


# In[27]:


Budget['Chip_size'].describe()


# In[ ]:




