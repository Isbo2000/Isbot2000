import os
import sys
files = [x for x in os.listdir('./Scripts')
    if os.path.isfile(os.path.join('./Scripts', x))]

for file in files:
    sys.path.append(file)