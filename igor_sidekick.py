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


def html_to_list(html_file): #will need to os.chdir() to the output folder
    with open(html_file) as file:
        soup = BeautifulSoup(file, 'html.parser')

    locator = 'div table tr td p'
    dollar_regex = '[0-9]*,*[0-9]*,*[0-9]+'

    item = soup.select(locator)
    lines = []

    for i in item:
        if i.string is None:
            pass
        elif i.contents[0] == '\n':
            pass
        else:
            line = str(i.contents[0])  # convert single element list to string
            line = line.replace('\n', '').replace('  ', '').replace('(', '').replace(')', '')  # strip string characters
            lines.append(line.strip())

    while '' in lines:
        lines.remove('')
    while '—' in lines:
        lines.remove('—')
    while '$' in lines:
        lines.remove('$')
    print('...processing {}'.format(html_file))
    print(lines)
    return lines


def structure(list): #delete all dat prior to first month
    months = {'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'}
    reg = '(\S)*'
    for i in range(len(list)):  #
        string = re.search(reg, list[i])
        try:
            string = {string.group(0)}
        except:
            pass
        if string.intersection(months):
            print('*************************found first month.')
            del list[:i]
            break

    return list


def structureB(list):
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