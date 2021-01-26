import re, os, os.path
from bs4 import BeautifulSoup

data_path = os.getcwd() + '/data'
log_path = os.getcwd() + '/logs'
output_path = os.getcwd() + '/output'


class Report:

    def __init__(self, html_file):
        self.file = html_file
        with open(html_file) as file:
            self.soup = BeautifulSoup(file, 'html.parser')

    @property
    def summary(self):
        locator = 'table'
        item = self.soup.find_all(locator)

        for everything in item:
            tmpTable = []
            table = everything.text.replace('\n', '').replace('$', '').replace('—', '').split('  ')
            for i in table:
                if i != '':  # empty strings are still persistent for some reason?
                    tmpTable.append(i.strip())
            comparison = set(tmpTable[:9])
            comp = {'ASSETS', 'assets', 'Assets'}
            if comparison.intersection(comp):  # find the first table that intersects with 'comp'
                break  # tmpTable

        keys, vals = [], []
        for i in range(1, len(tmpTable)):
            if _is_dollars(tmpTable[i]) and _is_not_dollars(tmpTable[i - 1]):
                keys.append(tmpTable[i - 1])
                vals.append(int(tmpTable[i].replace(',', '')))
        sumTable = dict(zip(keys, vals))
        return sumTable

    @property
    def fundamentals(self):  # return a dict of summary tables
        pass

    @property
    def techSector(self):
        pass


def _init_prompt():
    print('Sidekick test')


def _not_num(n):
    try:
        n = float(n)
        return False
    except:
        return True


def _is_num(n):
    try:
        n = float(n)
        return True
    except:
        return False


def html_to_list(html_file):  # will need to os.chdir() to the output folder
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
            line = line.replace('\n', '').replace('  ', '').replace('(', '').replace(')', '').replace('\xa0',
                                                                                                      ' ')  # strip string characters
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


def structure(list, starter=1):  # starter must be a set of strings expected at the start of a table
    if starter == 1:
        starter = {'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December'}
    print(starter)
    index = 0
    for element in list:  #
        element.replace(u'\xa0', u' ')
        comp = set(element.split(' '))
        if comp.intersection(starter):
            print('*************************found starting condition.')
            del list[:index]
            break
        index += 1
    return list


def structureB(list):
    key_temp = []
    val_temp = []
    for i in list:
        i = filter_year(i)  # search for year first to avoid matching with dollar amounts
        i = filter_monies(i)
        if _not_num(i):
            # print(f'{i} is not a number')
            key_temp.append(i)
        elif _is_num(i):
            # print(f'{i} is a number')
            val_temp.append(i)
    return dict(zip(key_temp, val_temp))


def filter_monies(string):
    dollar_regex = '[0-9]*,*[0-9]*,*[0-9]+'
    match = re.match(dollar_regex, string)
    if match:
        value = match.group()
        return value.replace(',', '')
    return string


def filter_year(string):
    year_regex = '2[0-9][0-9][0-9]'  # any year between 2000 - 2999
    match = re.match(year_regex, string)
    if match:
        value = 'Year:' + match.group()  # add to year to make string != number
        return value
    return string


#
