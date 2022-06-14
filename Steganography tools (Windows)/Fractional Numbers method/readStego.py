# This script is reads secret data hidden in PDF file's /MediaBox array values' decimal parts by reading those parts,
# splitting every 3 digits and converting it from ASCII code to text.
#
# Filled carriers are stored in \\filled_carriers\\ directory.
# Extracted messages are stored in \\extracted_messages\\ directory.

import re
import os
import glob

filenames = glob.glob('filled_carriers/*.pdf')
done = 0

for filename in filenames:
    print(os.path.basename(filename), end=' : ')
    with open(filename, "rb") as f:
        content = f.read()  # save content of pdf
        MediaBoxes = re.findall(b'/MediaBox\s?\[.*?\]', content)  # Find every single /MediaBox
        try:
            stego = b''
            for MediaBox in MediaBoxes:  #
                numbers = [el[el.find(b'.') + 1:] for el in re.findall(b'\d*\.?\d+', MediaBox)]
                for number in numbers:
                    for i in range(0, len(number), 3):
                        if number[i:i + 3] != b'000':
                            stego += chr(int(number[i:i + 3])).encode()
            try:
                os.mkdir('extracted_messages')
            except:
                pass
            outputfile = 'extracted_messages/' + os.path.basename(filename)[:-4] + '_extracted.txt'
            with open(outputfile, 'wb') as f:
                f.write(stego)
            print('done')
            done += 1
        except Exception as e:
            print('Corrupted or empty carrier')
            print(e)
print('Succesfully extracted from', done, 'of', len(filenames),
      'files (' + str(round(done / len(filenames) * 10000) / 100) + '%)\n---\n')
