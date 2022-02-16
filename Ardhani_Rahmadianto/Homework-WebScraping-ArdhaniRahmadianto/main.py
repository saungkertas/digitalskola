# Made by Ardhani Rahmadianto for Homework Web Scraping purpose

import time #for sleep & to know how long the process 
from selenium import webdriver  #for webscraping purpose

from bs4 import BeautifulSoup

time1 = time.time() 

# path to chromedriver.exe (I used ChromeDriver 98.0.4758.80 windows)
# May change due to different environment
PATH = 'C:\Program Files (x86)\chromedriver.exe'

op = webdriver.ChromeOptions()
# try to access with headless(without opening chrome).. no response from server(suspect BOT detected)
# op.add_argument('headless')
# # user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'    
# # user_agent = 'Joko'    
# # op.add_argument('user-agent={0}'.format(user_agent))

# to fix error about Open GL in end of program
op.add_argument('--disable-gpu') 

driver = webdriver.Chrome(PATH,options=op)

# URL from Tokped
driver.get("https://www.tokopedia.com/tokoexpert/etalase/vga-nvidia")
# driver.get("https://www.tokopedia.com/tokoexpert/etalase/vga-amd-radeon") # alternative link

# Scroll down for reveal all of product list element
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# wait some of time then minimize window
time.sleep(3)
driver.minimize_window()
# print(driver.title)

# initialize variable for getting the datas
productStart = 1
productList = []

# Get the maximum product list displayed in 1 page
# <span class="css-1cecfpj">80</span>
# //*[@id="zeus-root"]/div/div[2]/div[2]/div[4]/div/div[2]/div[2]/div/span[4]/span
# productEnd = driver.find_element_by_css_selector('#zeus-root > div > div:nth-child(2) > div.css-zvvilv > div.css-1kn5b1o > div > div.css-8atqhb > div.css-8pg9bu > div > span:nth-child(4) > span')
# use XPath of HTML element
productEnd = driver.find_element_by_xpath('//*[@id="zeus-root"]/div/div[2]/div[2]/div[4]/div/div[2]/div[2]/div/span[4]/span')
productEnd = int(productEnd.text)
print(' \n --> productEnd =',productEnd,' with type : ',type(productEnd),'\n')

# looping for get the HTML element code per product as string, collected to productList list
for i in range(productStart,productEnd +productStart):
    #use exception handling for unmatched number displayed of product list with productEnd
    try:
        product_detail = driver.find_element_by_xpath(f'//*[@id="zeus-root"]/div/div[2]/div[2]/div[4]/div/div[2]/div[1]/div[{i}]/div/div/div/div/div/div[2]/a')
        productList.append(product_detail.get_attribute('innerHTML'))
    except:
        print(f'List produk out kurang dari {productEnd}')
        break

# List product by element (For debug purpose)
# 1
#<a class="pcv3__info-content css-gwkf0u" href="https://www.tokopedia.com/tokoexpert/gigabyte-rtx-3090-gaming-oc-24gb-gddr6x" title="GIGABYTE RTX 3090 GAMING OC 24GB GDDR6X"><div class="css-wp2pck" aria-label="gimmick">Produk Terbaru</div><div class="css-1b6t4dn" data-testid="linkProductName">GIGABYTE RTX 3090 GAMING OC 24GB GDDR6X</div><div class="css-1ksb19c" data-testid="linkProductPrice">Rp 40.850.000</div><div class="css-yaxhi2" data-productinfo="true"></div></a>
#//*[@id="zeus-root"]/div/div[2]/div[2]/div[4]/div/div[2]/div[1]/div[1]/div/div/div/div/div/div[2]/a

# 2
#<a class="pcv3__info-content css-gwkf0u" href="https://www.tokopedia.com/tokoexpert/vga-asus-rog-strix-gaming-rtx-3050-oc-edition-8gb-gddr6" title="VGA ASUS ROG STRIX GAMING RTX 3050 OC EDITION 8GB GDDR6"><div class="css-1b6t4dn" data-testid="linkProductName">VGA ASUS ROG STRIX GAMING RTX 3050 OC EDITION 8GB GDDR6</div><div class="css-1ksb19c" data-testid="linkProductPrice">Rp 8.250.000</div><div class="css-yaxhi2" data-productinfo="true"><div class="css-q9wnub"><i class="css-1es2iep" aria-label="Rating Star"></i><span class="css-t70v7i" data-testid="">5.0</span><span class="css-138sgdp"></span><span class="css-1duhs3e" data-testid="">Terjual 1</span></div></div></a>
#//*[@id="zeus-root"]/div/div[2]/div[2]/div[4]/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[2]/a

# 3
# <a class="pcv3__info-content css-gwkf0u" href="https://www.tokopedia.com/tokoexpert/leadtek-quadro-t1000-8gb-ddr6-128-bit-4port-mini-display" title="LEADTEK QUADRO T1000 8GB DDR6 128-bit 4port mini display"><div class="css-wp2pck" aria-label="gimmick">Produk Terbaru</div><div class="css-1b6t4dn" data-testid="linkProductName">LEADTEK QUADRO T1000 8GB DDR6 128-bit 4port mini display</div><div class="css-1ksb19c" data-testid="linkProductPrice">Rp 7.590.000</div><div class="css-yaxhi2" data-productinfo="true"></div></a>
# //*[@id="zeus-root"]/div/div[2]/div[2]/div[4]/div/div[2]/div[1]/div[3]/div/div/div/div/div/div[2]/a

# Number of Max Product displayed
# 80
#//*[@id="zeus-root"]/div/div[2]/div[2]/div[4]/div/div[2]/div[1]/div[80]/div/div/div/div/div/div[2]/a

# For saving to .csv file
# print(productList)
with open('Result_Homework-WebScraping_Ardhani_Rahmadianto.csv', 'w') as f:
    f.write('No,Product Name,Price\n')
    for i, x in enumerate(productList) :
        # x.split('\n')
        # f.write(f'Product No : {i+1} \n{x} \n\n')
        # parse the HTML code using beautifulSoup
        soup = BeautifulSoup(x, 'html.parser')
        productName = soup.find('div',{'data-testid' : 'linkProductName'})
        productPrice = soup.find('div',{'data-testid' : 'linkProductPrice'})
        f.write(f'{i+1},{productName.text},{productPrice.text}\n')

# close and quit chrome window
driver.close()
driver.quit()

# display the running time
time2 = time.time() 
print(f'Processing time untuk whole code : {time2-time1} seconds')