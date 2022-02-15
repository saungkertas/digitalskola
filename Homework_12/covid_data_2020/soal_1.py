import os

dir = "C:\\Users\\Default.Default-THINK\\Dropbox\\My PC (Default-THINK)\\Documents\\DigitalSkola\\Homework_12\\covid_data_2020\\"
directory = os.listdir(dir)

searchstring = "Indonesia"

for fname in directory:
    if os.path.isfile(dir + fname):    
        with open(dir + fname,'r') as fileku: #read all csv file inside folder
            for line in fileku: #looping for search file
                if searchstring in line: # find 'indonesia' in looping
                    line = line.rstrip('\n') #remove space between line
                    with open(dir + 'wisnu_covid_indonesia_2020.csv','a') as f: #append data to new file csv
                        print(line, file=f)
