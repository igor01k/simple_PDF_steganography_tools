# This script reads secret data hidden in a PDF file using PDF stream's TJ text operator's values with precision of 3,
# which means that it takes only part that comes after 3 decimal digits (first 3 digits after dot).
#
# Filled PDF carriers are stored in \filled_carriers\ directory.
# Extracted messages are stored in \extracted_messages\ directory.

import re
import zlib
import os
import glob

filenames = glob.glob('filled_carriers\\*.pdf')
done = 0
precision = 3  # number of decimal digits that can not be changed

# regular expressions:
streamRegEx = re.compile(b'.*?FlateDecode.*?stream(.*?)endstream', re.S)
TJRegEx = re.compile('\[.*\]TJ', re.S)
decimalsRegEx = re.compile('-?\d*\.\d*')

for filename in filenames:
    print(os.path.basename(filename), end=' : ')
    stegoOctal = ''
    i = 0
    f = open(filename, 'rb')
    content = f.read()  # save content of pdf
    f.close()

    streams = re.findall(streamRegEx, content)  # find every single stream
    for stream in streams:
        stripped = stream.strip(b'\r\n')
        try:
            decoded = zlib.decompress(stripped).decode('UTF-8')  # decompress and decode the original stream
            for TJ in re.findall(TJRegEx, decoded):  # looking for [..]TJs
                for number in re.findall(decimalsRegEx, TJ):  # looking for decimal digits
                    originalNumber = str(number)
                    stegoOctal += originalNumber[originalNumber.find('.') + 1 + precision:]  # saving stegopart

        except:
            pass
    try:
        stego = ''.join([chr(int(a, 8)) for a in list(
            filter(lambda a: a != '', stegoOctal.split('9')))])  # converting extracted stego from octal to text
        try:
            os.mkdir('extracted_messages')
        except:
            pass
        f = open('extracted_messages/' + os.path.basename(filename)[:-4] + '_extracted.txt', 'w')
        f.write(stego)
        f.close()
        print('success')
        done += 1
    except:
        print('error')
print('Succesfully extracted from', done, 'of', len(filenames),
      'files (' + str(round(done / len(filenames) * 10000) / 100) + '%)\n---\n')
