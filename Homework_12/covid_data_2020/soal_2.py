import csv
import os

month = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}
dir = "C:\\Users\\Default.Default-THINK\\Dropbox\\My PC (Default-THINK)\\Documents\\DigitalSkola\\Homework_12\\covid_data_2020\\"
directory = os.listdir(dir)

results = []
with open(dir + 'wisnu_covid_indonesia_2020.csv','r') as File:
    reader = csv.reader(File, delimiter=',') 
    for row in reader: # each row is a list
        results.append(row) # put result from csv reader to list

header = ['month','year','total_active_case','total_death_case'] #header for summary csv file
with open(dir + 'wisnu_monthly_report_covid_indonesia_2020.csv','w') as file_sum: # write new csv file
    writer = csv.writer(file_sum, lineterminator='\n') # assign variable for csv writer with remove newline
    writer.writerow(header) 
    for i in month:
        active_list = []
        death_list = []
        for row in results:
            if (row[0][5:7]) == i:
                active_list.append(int(row[1]))
                death_list.append(int(row[2]))
        summary = [month[i],'2021',sum(active_list),sum(death_list)]
        writer.writerow(summary)   