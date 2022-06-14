#!/bin/bash
# This script writes down all of TJ operator's values between -16 and 16. Originally this script was written to
# analyze PDF files containing hidden data embedded with pdf_hide tool (https://github.com/ncanceill/pdf_hide).
# Values are stored in a .csv file. There are two directories with output.csv:
# - \stats\ containing all values in [-16;16]
# - \stats_absolute\ containing all absolute values in [-16;16]
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
NUMBERSregex = re.compile(b'-?\d+(\.\d+)?')

for filename in glob.glob('*.pdf'):
    csv = filename + '\n'
    csv_abs = filename + '\n'
    # decompress PDF file via qpdf and save as temporary
    try:
        os.mkdir('tmp')
    except:
        pass
    os.system('qpdf ' + filename + ' tmp/' + filename + '_tmp.pdf' + ' --qdf --stream-data=uncompress')
    with open('tmp/' + filename + '_tmp.pdf', 'rb') as f:
        print(filename)
        content = f.read()
        # b'\)\s*?-?\d+(\.\d*)?\s*?\('
        TJs = re.findall(TJregex, content)
        numbers = []
        for TJ in TJs:
            for m in re.finditer(b'(?:>|\))\s*?-?\d+(\.\d*)?\s*?(?:\(|<)', TJ):
                if -16 <= float(TJ[m.span()[0] + 1:m.span()[1] - 1]) <= 16:
                    csv += TJ[m.span()[0] + 1:m.span()[1] - 1].decode() + '\n'
                    csv_abs += str(abs(float(TJ[m.span()[0] + 1:m.span()[1] - 1].decode()))) + '\n'
        try:
            os.mkdir('stats')
        except:
            pass
        try:
            os.mkdir('stats_absolute')
        except:
            pass
        with open('stats/' + filename[:-4] + '.csv', 'w') as f2:
            f2.write(csv)
        with open('stats_absolute/' + filename[:-4] + '_abs.csv', 'w') as f3:
            f3.write(csv_abs)
        os.system('rm -r tmp')

