# This Python script ensures that the dependencies for converter.py and
# fetcher.py are installed. This file should be run before the 
# aforementioned, and updated whenever the dependencies change.

import os
print('installing dependencies...')
os.system('pip3 install -r requirements.txt')
exit()