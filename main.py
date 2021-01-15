import igor_tools
import igor_sidekick
import os

#Company = 'Tesla, Inc.'
#Report_Type = '10-K'

if input('Download new data? (y/n)  ') == 'y':
    Download_Start_Year = input("Input FY to begin download (YYYY): ")
    print("Starting Download... This may take several minutes... ")
    available_files = igor_tools._download(int(Download_Start_Year))
    print(f"{len(available_files)} files available in /data path. \n\n")


#test case for attempting to get years/qtrs out of date range
if input("Make PULL attempt based on Company/Report/Dates? (y/n): ") == 'y':
    Company = input("Input company name to pull (must match exact string as recorded by SEC): ")
    C = igor_tools.adv_search(Company)
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

#h_list contains .htmls that need to be accessed and appended to get the final .html address for the specified report(s)
#