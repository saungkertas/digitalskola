#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import urllib.request, json, timeit, pandas as pd 


# In[ ]:


shopee_url = "https://shopee.co.id/api/v4/search/search_items?by=relevancy&limit=60&match_id=1028154&newest=0&order=desc&page_type=collection&scenario=PAGE_COLLECTION_SEARCH&version=2"
print(shopee_url)


# In[ ]:


with urllib.request.urlopen(shopee_url)as url:
    data_shopee = json.loads(url.read().decode('ascii','ignore')) 


# In[ ]:


header = ['Product Name','Price']
with open('Data_kipas_angin_Shopee.csv','w') as file :
    writer = csv.writer(file, lineterminator = '\n')
    writer.writerow(header)
    
    items = data_shopee['items']
    for item in items:
        name = item['item_basic']['name']
        price = item['item_basic']['price']
        data_price = [name, int(price/100000)]
        print(data_price)
        writer.writerow(dataprice)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




