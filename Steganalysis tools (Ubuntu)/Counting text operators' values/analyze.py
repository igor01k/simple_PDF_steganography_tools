#!/bin/bash
# This script counts values of different PDF text operator's values. This may be useful for choosing text operator
# for embedding secret data in it's values.
#
# Stats for every PDF file in root directory is saved to \stats\ directory in a single .csv file that contains:
# PDF file's name
# Count of TJ operator's values
# Count of Tm operator's values
# Count of Tc operator's values
# Count of Tw operator's values
# Count of Td operator's values
#
# !!! BE AWARE !!!
# qpdf installation is required:
# sudo apt-get update
# sudo apt-get install qpdf

import glob
import re
import os

# regular expressions
TJregex = re.compile(b'\[.+\]\s*?TJ')
Tmregex = re.compile(b'(?:(?:-?\d+(?:\.\d+)?)\s)+\s*Tm')
Tcregex = re.compile(b'-?\d+(\.\d*)?\s*?Tc')
Twregex = re.compile(b'-?\d+(\.\d*)?\s*?Tw')
Tdregex = re.compile(b'-?\d+(\.\d*)?\s*?Td')
NUMBERSregex = re.compile(b'-?\d+(\.\d+)?')

csv = 'file,TJ,Tm,Tc,Tw,Td\n'
for filename in glob.glob('*.pdf'):
    # decompress PDF file via qpdf and save as temporary
    try:
        os.mkdir('tmp')
    except:
        pass
    os.system('qpdf ' + filename + ' tmp/' + filename + '_tmp.pdf' + ' --qdf --stream-data=uncompress')
    with open('tmp/' + filename + '_tmp.pdf', 'rb') as f:
        print(filename)
        content = f.read()
        TJ_numbers = sum(len(re.findall(b'(>|\))\s*?-?\d+(\.\d*)?\s*?(\(|<)', x)) for x in
                         re.findall(TJregex, content))  # always has multiple numbers
        print('TJ count:', TJ_numbers)
        Tm_numbers = sum(
            len(re.findall(NUMBERSregex, x)) for x in re.findall(Tmregex, content))  # always has multiple numbers
        print('Tm count:', Tm_numbers)
        Tc_numbers = len(re.findall(Tcregex, content))  # always has 1 number
        print('Tc count:', Tc_numbers)
        Tw_numbers = len(re.findall(Twregex, content))  # always has 1 number
        print('Tw count:', Tw_numbers)
        Td_numbers = len(re.findall(Tdregex, content)) * 2  # always has 2 numbers
        print('Td count:', Td_numbers)
        print()
        csv += filename + ',' + str(TJ_numbers) + ',' + str(Tm_numbers) + ',' + str(Tc_numbers) + ',' + str(
            Tw_numbers) + ',' + str(Td_numbers) + '\n'
with open('stats.csv', 'w') as f:
    f.write(csv)
try:
    os.system('rm -r tmp')
except:
    pass
