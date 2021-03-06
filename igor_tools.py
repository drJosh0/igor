'''
#backend functions for financial analysis

https://sec-api.io
API KEY: 9a273a2d85d081b8b1757ed508d6b3edf04030c4afd6e66add69eb6e9abab8f4

QUERY API: https://api.sec-api.io
STREAMING API: https://api.sec-api.io:3334/all-filings

'''

import os, os.path, re
import edgar
import pandas
import requests
import igor_sidekick

from datetime import datetime, timezone
from bs4 import BeautifulSoup

data_path = os.getcwd()+'/data'
log_path = os.getcwd()+'/logs'
output_path = os.getcwd()+'/output'

def _init_prompt():
    user = input(
'''\nActive instance of IGOR: What would you like to do??
d - download new data from SEC?
s - search existing local files?
t - test BETA tools
q - quit program
\n''')
    return user

def download_prompt():
    Download_Start_Year = input("Input FY to begin download (YYYY): ")
    print("Starting Download... This may take several minutes... ")
    available_files = _download(int(Download_Start_Year))
    print("{} files available in data path. \n\n".format(len(available_files)))

def search_prompt():
    Company = input("Input search term(s) for COMPANY (comma separated): ")
    C = _adv_search(Company)
    Report_Type = input("Enter report type of interest (i.e. 10-Q or 10-K) or 'X' to find available report types: ").upper()
    if Report_Type == 'X':
        _adv_report(C) #search through most recent 4 tsv files (1 calendar year) and get all filing types for that company
        Report_Type = input("Enter report type of interest (i.e. 10-Q or 10-K): ").upper()

    dates = input("Input date range for data pull (YYYY-YYYY): ").split('-')
    outputPath = report_download(C, Report_Type, int(dates[0]), int(dates[1]))



def _download(year: int):
    #download large .tsv files containing all listed filings per qtr
    #Would be good to add a check on data_path for existing files to only download most up-to-date files
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    edgar.download_index(data_path, year, skip_all_present_except_last=False)
    print("Downloading financial data")
    return os.listdir(data_path)


def _tsv_format(filename):  #open .tsv file and create dictionary with keys listed below -> use for search/filter
    with open(data_path+'/'+filename, 'r') as file:
        r = [row.split('|') for row in file]
        keys = ['Number', 'Company', 'Filing Type', 'Filing Date', 'Data File', 'Data File html']
        output = [dict(zip(keys, r[i])) for i in range(len(r))]
    return output

def _adv_search(search_string_in):
    string = search_string_in.split(',')
    string = [element.strip(' ') for element in string] #remove any leading/trailing spaces
    search_string = set(string)

    os.chdir(data_path)
    filenames = os.listdir()
    filenames.sort()
    filenames.reverse()

    count = 1
    matches = set()
    while len(matches) < 1:  #iterate over .tsv's until finding at least 1 match

        for f in filenames:
            print('looking in <<{}>>'.format(f))
            single_tsv = _tsv_format(f)

            for i in range(len(single_tsv)):
                company = set(single_tsv[i]['Company'].lower().replace(',', '').split(' '))
                if search_string.intersection(company):
                    matches.add(single_tsv[i]['Company'])
            filenames.pop(0)
            break #go back to while loop to determine if it is worth looking in another tsv file
        if count > 5:
            break  # if there are no matches after searching all files in data_path
        count += 1


    print('Found match(es): {}\n'.format(matches))
    match = list(matches) #convert to list to make callable
    if len(match) > 1: #user needs to select company name to search on
        user_index = input('Provide index of correct search criteria <<{}>> (N): '.format(match))
        print('Using Value: {}'.format(match[int(user_index)]))
        return match[int(user_index)]
    elif len(match) == 1:
        return match[0]
    else:
        print('Unexpected error in ADV SEARCH - most likely could not find company name provided')
        raise ValueError


def _adv_report(Company: str): #pull all available reports for a given company and output to an organized series of folders output/adv_search/Company/ --> year/report_type.html
    available_reports = set()
    recent_tsvs = os.listdir(data_path)
    recent_tsvs.sort(reverse=True)
    list_tsv = recent_tsvs[0:3]
    for tsv in list_tsv:
        for line in _tsv_format(tsv):
            if line['Company'] == Company:
                available_reports.add(line['Filing Type'])

        ar = list(enumerate(available_reports))
    return [print(x) for x in ar]


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

def save_page(html_string, save_path, save_filename):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    response = requests.get(html_string)
    soup = BeautifulSoup(response.text, 'html.parser')
    with open(save_filename, 'w') as file:
        file.write(soup.prettify())


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

def html_retrieve(filename, company):  #return all htmls for all reports for a given company
    base_url = 'https://www.sec.gov/Archives/'
    html = []
    report = []
    print('Searching through {}... '.format(filename))
    for line in _tsv_format(filename): #search each line of .tsv file for company
        if line['Company'] == company:
            h = base_url + line['Data File html']
            r = line['Filing Type']
            #html.append(base_url + line['Data File html'])
            #report.append(r)

            data = pandas.read_html(h, match=r)
            counter = 0
            for element in data[0]['Type']:  # search through dataframe of html tables
                if element == r:
                    htm_tail = data[0]['Document'][counter]
                    if "iXBRL" in htm_tail:
                        html.append(filename.replace('-', '').replace('index.html', '') + '/' + htm_tail.split(' ')[0])
                    else:
                        html.append(filename.replace('-', '').replace('index.html', '') + '/' + htm_tail)
                    break
                counter += 1

    keys = ['Company List', 'Report List', 'html List']
    vals = [[company]*len(html), report, html]
    return dict(zip(keys, vals))


def _filename_list_to_html(list_of_files, company, report_type): #take in list of tsv filenames, company, and report type to search
    html_list, count = [], 1
    base_url = 'https://www.sec.gov/Archives/'

    for file in list_of_files:
        print("Searching through {}... ".format(file))
        dict_ = _tsv_format(file) #open .tsv file and output data in a list
        for item in dict_:
            if item['Company'] == company and item['Filing Type'] == report_type:
                html_list.append(base_url+item['Data File html'].strip('\n'))
        if count > 4 and len(html_list) < 0:
            user = input('Could not find REPORT TYPE <<{}>> in 5 attempts --> continue? (y/n):'.format(report_type))
            if user == 'n':
                break
            elif user == 'y':
                count = 0

        count += 1
    return html_list

def report_download(company: str, report_type: str = '10-Q', date_range_start: int = datetime.now().year-1, date_range_end: int = datetime.now().year):
    filename_list = _filename_list(date_range_start, date_range_end)
    html_list = _filename_list_to_html(filename_list, company, report_type)
    htm_list = _html_to_htm(html_list, report_type)
    print("\nFound {} <<{}>> results: ".format(len(htm_list), report_type))

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_folder = company.replace(' ', '_').replace(',', '').replace('/', '-') + "_" + report_type + "_" + str(date_range_start) + "-" + str(date_range_end)
    #save individual html files
    filePath = _save_htm(htm_list, output_folder)


        #
    return output_path


