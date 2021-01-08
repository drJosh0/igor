import re, os, os.path
from bs4 import BeautifulSoup

data_path = os.getcwd()+'/data'
log_path = os.getcwd()+'/logs'
output_path = os.getcwd()+'/output'



def _not_num(n):
    try:
        n = int(n)
        return False
    except:
        pass
    try:
        n = float(n)
        return False
    except:
        return True

def _is_num(n):
    try:
        n = int(n)
        return True
    except:
        pass
    try:
        n = float(n)
        return True
    except:
        return False


def structure(list):
    key_temp = []
    val_temp = []
    for i in list:
        i = year(i)  #search for year first to avoid matching with dollar amounts
        i = monies(i)
        if _not_num(i):
            #print(f'{i} is not a number')
            key_temp.append(i)
        elif _is_num(i):
            #print(f'{i} is a number')
            val_temp.append(i)
    return dict(zip(key_temp, val_temp))

def monies(string):
    dollar_regex = '[0-9]*,*[0-9]*,*[0-9]+'
    match = re.match(dollar_regex, string)
    if match:
        value = match.group()
        return value.replace(',','')
    return string

def year(string):
    year_regex = '2[0-9][0-9][0-9]'  #any year between 2000 - 2999
    match = re.match(year_regex, string)
    if match:
        value = 'Year:' + match.group() #add to year to make string != number
        return value
    return string



#