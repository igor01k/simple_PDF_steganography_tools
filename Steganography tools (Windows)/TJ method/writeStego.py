# This script is using PDF stream's TJ text operator's values to hide text. The text is being converted into the octal
# (base-8 number system) ASCII code with 9 as a separator (because 9 is not used in the octal number system).
#
# The secret data is being embedded using decimal parts of the fractional numbers with a precision of 3. It means that
# first 3 numbers after dot will not be changed.
#
# To be sure that the data was embedded succesfully, after it is embedded it is also being checked for ability do
# extract the secret data. If the extracted data equals to the text which was supposed to hide, then it is done.
#
# PDF files which are used as carriers are taken from \carriers\ directory.
# PDF files with embedded secret data are stored in \filled_carriers\ directory.
# It is possible to process many files at once.
#
# !!! BE AWARE !!!
# This script is far from perfect, so for PDF files containing a big amount of TJ values it may take a REALLY LONG TIME to process.
# Keep in mind that carrier's cross-reference table is being modified which can cause problems opening filled carrier in some
# PDF readers.

import re
import zlib
import os
import glob

filenames = glob.glob('carriers\\*.pdf')
done = 0
precision = 3  # number of decimal digits that can not be changed
stego = 'Stego-Text' * 50  # text to hide
stegoOctal = ''.join([str(oct(ord(char))[2:]) + '9' for char in stego])  # stego to octal. '9' is used as separator

# regular expressions:
streamRegEx = re.compile(b'.*?FlateDecode.*?stream(.*?)endstream', re.S)
TJRegEx = re.compile('\[.*\]TJ', re.S)
decimalsRegEx = re.compile('-?\d*\.\d*')
for filename in filenames:
    print(os.path.basename(filename), end=' : ')

    i = 0  # length of already embedded part
    test = ''
    f = open(filename, 'rb')
    content = f.read()  # save content of pdf
    f.close()

    streams = re.findall(streamRegEx, content)  # find every single stream
    for stream in streams:
        stripped = stream.strip(b'\r\n')
        try:
            decoded = zlib.decompress(stripped).decode('UTF-8')  # decompress and decode the original stream
            for TJ in re.findall(TJRegEx, decoded):  # looking for [..]TJs
                iterator = list(re.finditer(decimalsRegEx, TJ))
                newTJ = ''
                prev = 0
                for j in iterator:
                    replacement = TJ[j.span()[0]:j.span()[1]]
                    N = (len(replacement[replacement.find(
                        '.') + 1:]) - precision)  # number of decimal digits that can be replaced with stego
                    if N > 0:
                        if i > len(stegoOctal):  # if message is fully embedded, just fill replacable digits with '9'
                            replacement = replacement[:replacement.find('.') + 1 + precision] + N * '9'
                        else:  # else replace digits with stego
                            replacement = replacement[:replacement.find('.') + 1 + precision] + stegoOctal[i:i + N]
                            if N > len(stegoOctal) - i:  # if message is fully embedded, fill the rest with '9'
                                replacement += (N - (len(stegoOctal) - i)) * '9'
                            i += N  # update the length of already embedded part
                    newTJ += TJ[prev:j.span()[0]] + replacement
                    prev = j.span()[1]
                newTJ += TJ[prev:]
                decoded = decoded.replace(TJ, newTJ, 1)  # replace the original TJ with newTJ

                ### extracting stegotext to varible 'test'
            for TJ in re.findall(TJRegEx, decoded):
                for originalNumber in re.findall(decimalsRegEx, TJ):
                    test += originalNumber[originalNumber.find('.') + 1 + precision:]
                ### for later comparison between stego and actually embedded message
            encoded = zlib.compress(decoded.encode('UTF-8'))  # encode and compress edited stream
            content = content.replace(stripped, encoded, 1)
        except Exception as e:
            pass
            # print(e)
    embedded = ''.join([chr(int(a, 8)) for a in list(
        filter(lambda a: a != '', test.split('9')))])  # converting extracted stego from octal to text
    if i < len(stegoOctal):
        print('!!!too small carrier or too big stego!!!')
    else:
        if embedded == stego:  # checking if extracted stego actually equals to stego which was supposed to be embedded
            try:
                os.mkdir('filled_carriers')
            except:
                pass
            f = open('filled_carriers/' + os.path.basename(filename)[:-4] + '_filled.pdf', 'wb')
            f.write(content)
            f.close()
            print('success')
            done += 1
        else:
            print('!!!something went wrong!!!')
print('\n\nSuccesfully embedded in', done, 'of', len(filenames),
      'files (' + str(round(done / len(filenames) * 10000) / 100) + '%)\n---\n')
