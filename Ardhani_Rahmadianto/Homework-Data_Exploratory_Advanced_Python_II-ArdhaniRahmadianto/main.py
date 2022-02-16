# 1. Please choose one data set from kaggle https://www.kaggle.com/
# 2. Please do data exploratory such as :
#   a. Checking Introductory Details About Data
#   b. Statistical Insight
#   c. Data Cleaning
#   d. Data Visualization
# 3. Please submit your task in github

# Name : Ardhani Rahmadianto

import pandas as pd
import time #for sleep & to know how long the process 
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from functions_homework import * #Function for data manipulation / cleaning

time1 = time.time() 

# path to dataset (from : https://www.kaggle.com/iamsouravbanerjee/analytics-industry-salaries-2022-india )
PATH_FILE_CSV = 'archive/Salary Dataset.csv'

df = pd.read_csv(PATH_FILE_CSV)
pd.options.display.float_format = '{:.2f}'.format

print('RAW Dataframe of .csv file from : https://www.kaggle.com/iamsouravbanerjee/analytics-industry-salaries-2022-india : \n')
print(df)
# Statistical Insight
# idea is to visualize data of TOP 10 company that has highest salary for Data Engineer role (in IDR currency and per Month), also consider the number of respondent in salary reported.

# Data Cleaning
# create new dataframe (df) with Data Engineer (de) only --> df_de
df_de = df.loc[df['Job Title'].str.contains('Data Engineer')]
# Filter df_de with only "Salary Reported" above and equal than 5 
df_de = df_de.loc[df_de['Salaries Reported'] >= 5]

# Apply function "return_comp_spec_name" with 2 arguments : 1-column ('Company Name') 2-column ('Location') from df_de
# This is to return new column in df_de with name 'Company Name (with City)'
# The objective is to create new data company name with Location as 1 string <CompanyName-Location> --> for visualization purpose
df_de['Company Name (with City)']  = df_de.apply(return_comp_spec_name,col_name_1='Company Name',col_name_2 ='Location',axis=1)

# apply function "return_annualy" to df_de with input of data in all column "Salary"
# Objective is to exctract all number string became float --> for number aritmatic  purpose
# Also take care of currency data (available is Rupee ₹ & USD $) --> convert all to Rupee first
# Then also check the salary-per (available is /yr /mo /hr) --> create annually (yearly), assigned to new column "Annual Salary (₹)""
df_de['Annual Salary (₹)']  = df_de.apply(return_annually,col_name ='Salary',axis=1)

# apply function "return_IDR_annual" to df_de with input of data in all column "Annual Salary (₹)"
# Objective to convert all rupee to IDR --> assigned in new column "Annual Salary (IDR)"
df_de['Annual Salary (IDR)']  = df_de.apply(return_IDR_annual,col_name='Annual Salary (₹)',axis=1)

# apply function "return_IDR_monthly" to df_de with input of data in all column "Annual Salary (₹)"
# Objective to convert all rupee to IDR based on monthly salary --> assigned in new column "Monthly Salary (IDR)"
df_de['Monthly Salary (IDR)']  = df_de.apply(return_IDR_monthly,col_name='Annual Salary (₹)',axis=1)

# Sort the value of Salary for highest to be first index
df_de = df_de.sort_values(by='Annual Salary (₹)', ascending=False)
# reset the dataframe index, drop=true mean delete the new column that represent old index
df_de = df_de.reset_index(drop=True)

print('\n Dataframe with filtered & adding the calculation of Annual & Monthly Salary : \n')
print(df_de)
# Create new dataframe for top 10 company name with highest salary 
company_salary = df_de.loc[0:9,['Company Name (with City)','Monthly Salary (IDR)']]
print('\n Dataframe with only Top 10 Company with Highest Monthly Salary (IDR) : \n')
print(company_salary)


# Data Visualization
# Plot Dataframe 'company_salary'
# initialize seaborn
sns.set()
# Create plot using bar plot, assign to new seaborn object "plotData"
# Assign the x and y component (x='Company Name (with City)',y='Monthly Salary (IDR)') --> from column of 'company_salary' dataframe
plotData = sns.barplot(x='Company Name (with City)',y='Monthly Salary (IDR)',data=company_salary)

# modify y component (y_tick_label) for display rounded value with additional string (20 Jt) instead of float full number 
data_in_JT = [str(int(y)) + ' Jt' for y in plotData.get_yticks()/1000000]
plotData.set_yticklabels(data_in_JT)

# Add title and subtitle
plotData.text(x=0.5, y=1.1, s='Top 10 Company with Data Engineer Salary in India', fontsize=18, weight='bold', ha='center', va='bottom', transform=plotData.transAxes)
plotData.text(x=0.5, y=1.05, s='Based on 5 respondents and above of Salary Reported ', fontsize=10, alpha=0.75, ha='center', va='bottom', transform=plotData.transAxes)

# Add the label in X and Y axis
plotData.set_xlabel("Company Name & City",fontsize=12,weight='bold')
plotData.set_ylabel("Salary / Month (IDR)",fontsize=12,weight='bold')

# Add number above bar data that represent actual value of that data per bar
for i in plotData.containers:
    plotData.bar_label(i,fmt='%.2s Jt',fontsize=10) # format of displayed changed, crop only 2 first number then add " jt"

# to know the processing time
time2 = time.time() 
print(f'Processing time untuk whole code : {time2-time1} seconds')

# Show the graph
plt.show() 