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
            [print(x) for x in os.listdir(output_path)]
        elif user2 == 'c':
            print('time to do things...')
            [print(x) for x in enumerate(os.listdir(output_path))]
            available_paths = list(os.listdir(output_path))
            filepath = available_paths[int(input('Select folder path for summary calculation: '))]
            print('Selected <<{}>>'.format(filepath))

            os.chdir(os.getcwd()+'/output/'+filepath)
            for file in os.listdir():
                print(file)
                data = igor_sidekick.Report(file).summary
                print(data)
                print('Dollaz : ${}'.format(data['TOTAL ASSETS']))
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



