import re

# conversion ratio
CONV_RATIO_RUPEE_TO_IDR = 189.74
CONV_RATIO_USD_TO_RUPEE = 75.20

# return only number from string datatype
def return_only_number(value_string):
    only_number =  re.findall(('\d+'),value_string)
    only_number = "".join(only_number)
    return only_number

#Return Salary only per year
def return_annually(row,col_name): #first argument is for dataframe row by column (input the column name)
    splitted_List = row[col_name].split('/') #to split string divided by "/"
    salary_value = int(return_only_number(splitted_List[0])) #for first index splitted_List contain salary number with currency
    currency_type = splitted_List[0][0] #get the currency character
    currency_val = 1
    # return the desired currency
    if currency_type == "$":
        currency_val = CONV_RATIO_USD_TO_RUPEE
    elif currency_type == "₹":
        currency_val = 1 

    # check what is salary return based (yearly, monthly od hourly)
    # convert all to annually
    if splitted_List[1] == 'yr':
        return (salary_value) * currency_val #
    elif splitted_List[1] == 'mo':
        return  (salary_value*12) * currency_val #
    elif splitted_List[1] == 'hr':
        return  (salary_value*8*5*4*12) * currency_val # --> asumsi 8 jam kerja per hari, 5 hari kerja per minggu dalam setahun

# convert Rupee value to IDR value, output as String with prefix "IDR " --> as annualy
def return_IDR_annual(row,col_name):
    val = row[col_name] * CONV_RATIO_RUPEE_TO_IDR
    val = '{:,}'.format(int(val))
    return 'IDR '+ val

# convert Rupee value to IDR value, output as float  --> as monthly
def return_IDR_monthly(row,col_name):
    val = (row[col_name] * CONV_RATIO_RUPEE_TO_IDR) / 12
    #val = '{:,}'.format(int(val))
    return val #'IDR '+ val

# to combine string
def return_comp_spec_name(row,col_name_1,col_name_2):
     return row[col_name_1] + '\n' + row[col_name_2]
 
