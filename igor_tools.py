'''
#backend functions for financial analysis

https://sec-api.io
API KEY: 9a273a2d85d081b8b1757ed508d6b3edf04030c4afd6e66add69eb6e9abab8f4

QUERY API: https://api.sec-api.io
STREAMING API: https://api.sec-api.io:3334/all-filings

'''
igor_version = '2021-01-06'

import os, os.path, sys
import edgar
import pandas
import requests
import igor_sidekick

from urllib.parse import urljoin
from datetime import datetime, timezone
from bs4 import BeautifulSoup

data_path = os.getcwd()+'/data'
log_path = os.getcwd()+'/logs'
output_path = os.getcwd()+'/output'

def _write_to_log(message: str):
    #method for debugging purposed, log critical events: date of last download, queries made, etc.
    if not os.path.exists(log_path):
        os.makedirs(log_path)
        with open(log_path+'/log.txt', 'w'):
            print('initiated log file.')
    with open(log_path+'/log.txt', 'a') as file:
        date = str(datetime.now(timezone.utc))
        file.write(date + '    ' + message + '\n')


def _download(year: int):
    #download large .tsv files containing all listed filings per qtr
    #Would be good to add a check on data_path for existing files to only download most up-to-date files
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    edgar.download_index(data_path, year, skip_all_present_except_last=False)
    print("Downloading financial data")
    _write_to_log(f"***** Downloaded New Data {year} to present *****")
    return os.listdir(data_path)


def _tsv_format(filename):
    #open .tsv file and create dictionary with keys listed below -> use for search/filter
    with open(data_path+'/'+filename, 'r') as file:
        r = [row.split('|') for row in file]
        keys = ['Number', 'Company', 'Filing Type', 'Filing Date', 'Data File', 'Data File html']
        output = [dict(zip(keys, r[i])) for i in range(len(r))]

    return output

def adv_search(search_string):
    #search and return possible matches to input string
    pass


def _calc_financials(raw_data_dict):
    #take earnings dictionary and perform relevant calculations

    pass


def _format_10Q_to_dict(list_of_htms):
    #take list of htmls for a single company across multiple year(s) and generate a dictionary of earnings data
    #query htmls individually and put financial data into a dict
    for htm in list_of_htms:
        data = pandas.read_html(htm, match='Balance Sheet')
    pass

def _html_to_htm(list_of_htmls, report_type: str = '10-Q'): #default report = 10-Q
    #take list of htmls, access each one and get the final url for accessing reports directly
    counter = 0
    html_string = []
    for item in list_of_htmls: #iterate over each .html address
        data = pandas.read_html(item, match=report_type)
        for element in data[0]['Type']: #search through dataframe of html tables
            if element == report_type:
                htm_tail = data[0]['Document'][counter]
                if "iXBRL" in htm_tail:
                    html_string.append(item.replace('-', '').replace('index.html', '') + '/' + htm_tail.split(' ')[0])
                else:
                    html_string.append(item.replace('-', '').replace('index.html', '') + '/' + htm_tail)
                break
            counter += 1

    return html_string


def _save_htm(list_of_htms, pageFolder):
    print("Saving .html files to output directory... ")
    if not os.path.exists(output_path + '/' + pageFolder): # create only once
        os.mkdir(output_path + '/' + pageFolder)
    file_num = 1
    for u in list_of_htms:
        response = requests.get(u)
        url = response.url
        soup = BeautifulSoup(response.text, 'html.parser')
        s_file_num = '{:03}'.format(file_num)
        total_path = output_path + '/' + pageFolder + '/' + s_file_num + '.html'
        with open(total_path, 'w') as file:
            file.write(soup.prettify())
        file_num += 1
    print(f"See generated files in directory: {output_path + '/' + pageFolder}")
    return output_path + '/' + pageFolder

def _filename_list(date_range_start: int, date_range_end: int):
    current_year = datetime.now().year
    quarters = ['-QTR1.tsv', '-QTR2.tsv', '-QTR3.tsv', '-QTR4.tsv']
    years = [x + date_range_start for x in range(date_range_end + 1 - date_range_start)]
    filename_list = []
    for y in years:
        for q in quarters:
            filename_list.append(str(y) + q)

    filename_set = set(filename_list)
    data_set = set(os.listdir(data_path))
    target_files = list(filename_set.intersection(data_set))
    target_files.sort()

    return target_files


def _filename_list_to_html(list_of_files, company, report_type):
    html_list = []
    base_url = 'https://www.sec.gov/Archives/'

    for file in list_of_files:
        print(f"Searching through {file}... ")
        dict_ = _tsv_format(file) #open .tsv file and output data in a list
        for item in dict_:
            if item['Company'] == company and item['Filing Type'] == report_type:
                html_list.append(base_url+item['Data File html'].strip('\n'))
        _write_to_log(f"Retrieved {company} - {report_type} from {file} | IGOR revision: {igor_version}")
    return html_list

def report_download(company: str, report_type: str = '10-Q', date_range_start: int = datetime.now().year-1, date_range_end: int = datetime.now().year):
    filename_list = _filename_list(date_range_start, date_range_end)
    html_list = _filename_list_to_html(filename_list, company, report_type)
    htm_list = _html_to_htm(html_list, report_type)
    print(f"Found {len(htm_list)} results. ")

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_folder = company.replace(' ', '_').replace(',', '').replace('/', '-') + "_" + report_type + "_" + str(date_range_start) + "-" + str(date_range_end)
    #save individual html files
    filePath = _save_htm(htm_list, output_folder)


        #
    return output_path





#