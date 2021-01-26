import igor_tools
import igor_sidekick
import os
output_path = os.getcwd() + '/output'

user = 0

while user != 'q':
    user = igor_tools._init_prompt()
    if user == 'd':
        igor_tools.download_prompt()
    elif user == 's':
        igor_tools.search_prompt()
    elif user == 't':
        user2 = igor_sidekick._sidekick_prompt()
        if user2 == 'l':
            print(os.listdir(output_path))
        elif user2 == 'c':
            print('do things')
        elif user2 == 't':
            print('test 123')
        elif user2 == 'e':
            print('Exiting Program...')
        else:
            print('Unsupported action <<{}>> Try again'.format(user))
    elif user == 'q':
        print('\n##### Shutting down IGOR instance #####\n')
    else:
        print('Unsupported action <<{}>> Try again'.format(user))



'''
os.chdir('/home/hjk/PycharmProjects/Igor/output/Virgin_Galactic_Holdings_Inc_10-Q_2018-2020')
data = Report('001.html')

everything = data.fundamentals

'''
