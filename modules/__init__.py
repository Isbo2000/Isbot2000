import os
import sys
files = [x for x in os.listdir('./Modules')
    if os.path.isfile(os.path.join('./Modules', x))]

for file in files:
    sys.path.append(file)