import igor_tools
import igor_sidekick

#Company = 'Tesla, Inc.'
#Report_Type = '10-K'

user = 0

while user != 'q':
    user = igor_tools._init_prompt()
    if user == 'd':
        igor_tools.download_prompt()
    elif user == 's':
        igor_tools.search_prompt()
    elif user == 't':
        igor_sidekick._init_prompt()
    elif user == 'q':
        print('\n##### Shutting down IGOR instance #####\n')
    else:
        print('Unsupported action <<{}>> Try again'.format(user))

'''
#test case for attempting to get years/qtrs out of date range
if input("Make PULL attempt based on Company/Report/Dates? (y/n): ") == 'y':
    Company = input("Input search term(s) for COMPANY (comma separated): ")
    C = igor_tools._adv_search(Company)
    Report_Type = input("Enter report type of interest (i.e. 10-Q or 10-K): ").upper()
    dates = input("Input date range for data pull (YYYY-YYYY): ").split('-')
    outputPath = igor_tools.report_download(C, Report_Type, int(dates[0]), int(dates[1]))


if input("Sidekick test? (y/n)") == 'y':
    outputPath = os.getcwd()+'/'+'output'+'/'+'Tesla_Inc._10-Q_2019-2020'
    os.chdir(outputPath)  # drill into output folder
    file_list = os.listdir().sort()
    for file in [x for x in file_list]:
        fmt = igor_sidekick.html_to_list(file)
        data = igor_sidekick.structure(fmt)

if input('adv report demo? (y/n): ') == 'y':
    Company = input("Input search term(s) for COMPANY (comma separated): ")
    years = input("Input date range for data pull (YYYY-YYYY): ")
    igor_tools._adv_report(Company, years)
#h_list contains .htmls that need to be accessed and appended to get the final .html address for the specified report(s)
#
'''