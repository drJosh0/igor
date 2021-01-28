import re, os, os.path
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup


data_path = os.getcwd() + '/data'
log_path = os.getcwd() + '/logs'
output_path = os.getcwd() + '/output'


def _sidekick_prompt():
    user = input(
        '''\nIGOR SIDEKICK functionality test:
        l - list output folders available
        c - compile summary tables from available files
        t - test 
        e - exit back to IGOR main program
        \n
        your input: ''')

    return user


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
                keys.append(tmpTable[i - 1].upper())
                vals.append(float(tmpTable[i].replace(',', '')))
        sumTable = dict(zip(keys, vals))
        return sumTable #output a dictionary with key/values that are from the summary table of a 10-q


    @property
    def fundamentals(self):  # return a dict of summary tables
        pass

    @property
    def techSector(self):
        pass


def _is_dollars(string):
    try:
        float(string.replace(',', ''))
        return True
    except:
        return False


def _is_not_dollars(string):
    try:
        float(string.replace(',', ''))
        return False
    except:
        return True

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


