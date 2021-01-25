import igor_tools
from igor_sidekick import Report
import os


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
os.chdir('/home/hjk/PycharmProjects/Igor/output/Virgin_Galactic_Holdings_Inc_10-Q_2018-2020')
data = Report('001.html')

everything = data.fundamentals

'''
