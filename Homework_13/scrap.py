import urllib.request, json, csv, timeit, pandas as pd

dir = "C:\\Users\\Default.Default-THINK\\Dropbox\\My PC (Default-THINK)\\Documents\\GitHub\\digitalskola\\Homework_13\\"

shopee_url = "https://shopee.co.id/api/v4/search/search_items?by=relevancy&keyword=kipas%20angin&limit=60&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
print(shopee_url)
with urllib.request.urlopen(shopee_url) as url:
     data_shopee = json.loads(url.read().decode('ascii', 'ignore'))

#type(data_shopee)
#print(data_shopee['items'][0]['item_basic']['name'])

header = ['Product Name','Price'] #
with open(dir + 'Data_kipas_angin_Shopee_Wisnu.csv','a') as file: # write new csv file
   writer = csv.writer(file, lineterminator='\n') # assign variable for csv writer with remove newline
   writer.writerow(header) 
   items = data_shopee['items']

   for item in items:
      name = item['item_basic']['name']
      price = item['item_basic']['price']
      data_price = [name, int(price/100000)]
      #print(data_price)
      writer.writerow(data_price)
