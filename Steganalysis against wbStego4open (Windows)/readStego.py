# This script extracts files hidden in PDF documents with wbStego4open tool when no encryption was used.
# It uses 0x09 and 0x20 characters to write bit sequences between objects. 0x09 stands for 1 and 0x20 stands for 0.
# First 3 bytes are used to store hidden file's size. Next 3 bytes - hidden file's extension.
# The rest is hidden file's content.
#
# Filled carriers are stored in \\filled_carriers\\ directory.
# Extracted messages are stored in \\extracted_messages\\ directory.
# 
# !!! BE AWWARE !!!
# After testing this script with 99 PDF files containing secret file (42 txt + 18 jpg + 39 bmp) 2 JPG files were 
# not extracted successfully.
#
# wbStego4open available from:
# http://www.bailer.at/wbstego/pr_4ixopen.htm

import re
import os
import glob

filenames = glob.glob('filled_carriers/*.pdf')
done = 0
for filename in filenames:
    with open(filename, "rb") as f:
        print(os.path.basename(filename), end=':\t')

        byteList = []
        s = f.read()
        for i in re.finditer(b'(\x09|\x20){8,}', s):  # looking for every 8+ bit sequences
            byte = s[i.span()[0]:i.span()[1]].replace(b'\x09', b'1').replace(b'\x20', b'0')
            if int(byte, 2) < 256:
                byteList.append(byte)

        try:
            i = 0
            while i < len(byteList) and int(byteList[i], 2) == 0:
                i += 1
            size = int(byteList[i + 2] + byteList[i + 1] + byteList[i], 2) - 3
            i = i + 3
            fileFormat = ''
            for j in range(3):
                while i < len(byteList) and int(byteList[i], 2) == 0:
                    i += 1
                fileFormat += chr(int(byteList[i], 2))
                i += 1

            content = [int(x, 2) for x in byteList[i:i + size]]
            try:
                os.mkdir('extracted_messages')
            except:
                pass
            try:
                with open('extracted_messages/' + os.path.basename(filename)[:-4] + '_extracted.' + fileFormat,
                          'wb') as output:
                    output.write(bytes(content))
                    print('.' + fileFormat + ' file extracted (' + str(size) + ' bytes)\n---')
                    done += 1
            except Exception as e:
                print('***ERROR:', e)
                # print(size)
                # print(content)
                # print(byteList[i:])
                # print([int(x,2) for x in byteList[i:]])
                # output.close()
                # print(e)
                # print('***ERROR: ',content[0],content[1],content[2],'\t\t\t',os.path.basename(filename))
        except:
            print('Corrupted or empty carrier')
print('Successfully extracted from {0} out of {1} files ({2:3.2f}%)'.format(done, len(filenames),
                                                                            done / len(filenames) * 100))
