"""sample.py uses models generated by training.py and
generates a sample output based on it. The sample is saved
in the /sample directory.
"""

import os
import sys
import glob
from pathlib import Path
from subprocess import Popen

# try:
#     import torch
#     import torchvision
# except ImportError:
#     print('The modules required to run this script are not installed.')
#     print('Please run "python3 main.py" to install them.')
#     sys.exit()

print('sample.py takes a model and generates sample output.')
print('If you do not have a model file, close and run training.py')
print('Click enter to continue or "q" to exit.')
option = input(': ')
print()

# pull model name and numer of epochs from jsoon/csv/yaml file
# have it list and allow the user to choose which one they would
# like to sample
# someone determine the length of the sample file
# save to sample in sample/ or something

if not option == 'q':
    print('Tpye in the name of the model.')
    model_name = input(': ')
    print()

    model_path = ('models/' + model_name + '/')
    model_verify = Path(model_path + model_name + '_0.0')

    while not model_verify.is_file():
        print(model_name + '_0.json does not exist.')
        print('Are you sure you typed it correctly?')
        print('Try again, or type "q" to exit.')
        model_name = input(': ')
        model_path = ('models/' + model_name + '/')
        model_verify = Path(model_path + model_name + '_0.0')
        print()
        if model_name == 'q':
            sys.exit()

    print(model_name + ' found.')
    first_model = '0'
    model_count = len(glob.glob1(model_path, '*.0')) - 1
    print('Between ' + first_model + ' and ' + str(model_count) +
          ', choose which model you would to sample from.')
    print('If you would like to exit, type "q".')
    model_choice = input(': ')

    if not model_choice == 'q':
        if not Path('samples/' + model_name + '/').exists():
            if not Path('samples/').exists():
                os.mkdir('samples')
            os.mkdir('samples/' + model_name)

        sample_path = ('samples/' + model_name + '/')
        if not Path(sample_path + model_name + '_' + model_choice +
                    '_0.txt').exists():
            sample_name = model_name + '_' + model_choice + '_0'
        else:
            sample_count = len(glob.glob1(sample_path, model_name + '_' +
                                          model_choice + '*.txt'))
            sample_name = model_name + '_' + \
                model_choice + '_' + str(sample_count)
            print()

        print('How large do you want the ' + sample_name + '.txt to be?')
        print('This script may take a while to run and uses all available '
              'CPU resoucres, '
              'so choose a resonable amount.')
        print('This value is in bytes. The default is 65536 B (64KB).')
        print('Do you want to specify MB or KB? Press enter to accept default')
        print('1. KB')
        print('2. MB')
        size_option = input(': ')
        print()

        if size_option == '1':
            max_size = input('Input size: ')
            print()

        if size_option == '2':
            mb_size = input('Input size: ')
            max_size = mb_size * 1024

        if size_option == '':
            max_size = '65536'

        # OMP_NUM_THREADS

        # print('How many threads would you like to use?')
        # print('It is recommended to use less than all '
        #       'threads available as causes a slowdown.')
        # print('Not specifying a value will use all '
        #       'available threads.')
        # threads = input(': ')

        # print('Writing to ' + sample_name + '.txt')
        # with open(sample_path + sample_name + '.txt', 'w') as sample_file:
        #     sample_write = Popen('set OMP_NUM_THREADS={args.threads} '
        #                          '&& python3 -B pytorch-rnn/sample.py '

        print('Writing to ' + sample_name + '.txt')
        with open(sample_path + sample_name + '.txt', 'w') as sample_file:
            sample_write = Popen('python3 -B pytorch-rnn/sample.py '
                                 '--checkpoint ' + model_path
                                 + model_name + '_' + model_choice
                                 + '.json', stdout=sample_file)
            file_size = 0
            while file_size < int(max_size):
                file_size = sample_file.tell()
            if sample_file.tell() > int(max_size):
                Popen.terminate(sample_write)
            sample_file.close()

        print('Sample successful: ' + sample_name + '.txt')


sys.exit()
