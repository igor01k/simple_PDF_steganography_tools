# This script is embedding secret data in /MediaBox array values' decimal parts. The secret text is converted to
# ASCII code as 3 digits and is stored in fractional parts of numbers of /MediaBox array.
#
# PDF carriers are stored in \\carriers\\ directory.
# Filled carriers are stored in \\filled_carriers\\ directory.
#
# !!! BE AWARE !!!
# The carrier's cross-reference table is not being modified during data embedding, so filled carrier may not open
# properly in some PDF readers.

import re
import os
import glob
from math import ceil

filenames = glob.glob('carriers\\*.pdf')
done = 0
stego = 'Stego-Text'  # text to hide

for filename in filenames:
    print(os.path.basename(filename), end=' : ')
    with open(filename, "rb") as f:
        content = f.read()
        MediaBoxes = re.findall(b'/MediaBox\s?\[.*?\]', content)
        try:
            current = 0  # current 3 digits to be embedded
            toEmbed = ['0' * (3 - len(str(ord(char)))) + str(ord(char)) for char in stego]  # decimals to embed
            N = ceil(len(stego) / (len(MediaBoxes * 4)))  # stego's letters per number in /MediaBox
            for MediaBox in MediaBoxes:
                numbers = [int(float(el)) for el in re.findall(b'\d*\.?\d+', MediaBox)]  # finding all MediaBoxes
                MediaBoxWithStego = '/MediaBox['
                for number in numbers:
                    MediaBoxWithStego += str(number) + '.'
                    for i in range(N):
                        if current < len(toEmbed):
                            MediaBoxWithStego += toEmbed[current]
                        else:
                            MediaBoxWithStego += '000'  # if stego is fully embedded add zeros
                        current += 1
                    MediaBoxWithStego += ' '
                MediaBoxWithStego += ']'
                MediaBoxWithStego = MediaBoxWithStego.encode()
                content = content.replace(MediaBox, MediaBoxWithStego, 1)  # MediaBox --> MediaBox with stego
            try:
                os.mkdir('filled_carriers')
            except:
                pass
            outputfile = 'filled_carriers/' + os.path.basename(filename)[:-4] + '_filled.pdf'
            with open(outputfile, 'wb') as f:
                f.write(content)
            print('success')
            done += 1
        except Exception as e:
            print('corrupted file')
            print(e)
print('\n\nSuccesfully embedded in', done, 'of', len(filenames),
      'files (' + str(round(done / len(filenames) * 10000) / 100) + '%)\n---\n')
