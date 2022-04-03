import os
import sys
files = [x for x in os.listdir('./SubMod')
    if os.path.isfile(os.path.join('./SubMod', x))]

for file in files:
    sys.path.append(file)