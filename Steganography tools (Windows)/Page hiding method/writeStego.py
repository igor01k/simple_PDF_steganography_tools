# This script is able to hide a PDF file in another PDF file (carrier). The algorythm is based on idea provided
# in this research:
# Koptyra, K.; Ogiela, M.R. Distributed Steganography in PDF Files—Secrets Hidden in Modified Pages.
# Entropy 2020, 22, 600. https://doi.org/10.3390/e22060600
#
# It combines carrier PDF with the stego PDF, then decreases the count of pages so the added part (secret PDF) is
# not displayed when opened with PDF reader.
#
# Carrier files are stored in \\carriers\\directory.
# Filled carriers (PDF files with embedded secret data) are stored in \\filled_carriers\\ directory.
# It is possible to process several containers at once.
#
# !!! BE AWARE !!!
# pikepdf library is required.

import glob
import os
import re
from pikepdf import Pdf

filenames = glob.glob('carriers\\*.pdf')
stego = Pdf.open('stego.pdf')  # file to be hidden
done = 0

for filename in filenames:
    try:
        print(os.path.basename(filename), end=' : ')
        pdf = Pdf.open(filename)
        N = len(stego.pages)
        pdf.pages.extend(stego.pages)  # add stegoPages
        pdf.save('tmp.pdf')
        tmpFile = open('tmp.pdf', 'rb')
        content = tmpFile.read()
        tmpFile.close()
        for pageTree in re.findall(b'<<.*\/Type\s*?\/Pages.*>>', content):
            decoded = pageTree.decode('UTF-8')
            countRecord = re.search(r'\/Count\s*(\d*)', decoded)
            pageCount = countRecord.string[countRecord.span()[0] + 6:countRecord.span()[1]]
            newPageTree = countRecord.string[:countRecord.span()[0] + 6]
            newPageCount = int(pageCount) - N  # decreasing page count to empty carrier's page count
            newPageCount = ' ' * (len(pageCount) - len(str(newPageCount))) + str(newPageCount)
            newPageTree = countRecord.string[:countRecord.span()[0] + 6] + newPageCount + countRecord.string[
                                                                                          countRecord.span()[1]:]
            encoded = newPageTree.encode('UTF-8')
            content = content.replace(pageTree, encoded, 1)
        try:
            os.mkdir('filled_carriers')
        except:
            pass
        f = open('filled_carriers/' + os.path.basename(filename)[:-4] + '_filled.pdf', 'wb')
        f.write(content)
        f.close()
        print('success')
        done += 1
        os.remove('tmp.pdf')
    except:
        print('error')
print('\n\nSuccesfully embedded in', done, 'of', len(filenames),
      'files (' + str(round(done / len(filenames) * 10000) / 100) + '%)\n---\n')
