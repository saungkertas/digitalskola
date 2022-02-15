import json

dir = "C:\\Users\\Default.Default-THINK\\Dropbox\\My PC (Default-THINK)\\Documents\\DigitalSkola\\HW_13\\"
# Opening JSON file
#f = open(r'C:\Users\Default.Default-THINK\Dropbox\My PC (Default-THINK)\Documents\DigitalSkola\HW_13\shopee.json')
 

with open(dir + 'shopee.json') as f:
   data = json.loads(f.read().decode())
# returns JSON object as
# a dictionary
#data = json.loads(f.read().decode())

print(data)