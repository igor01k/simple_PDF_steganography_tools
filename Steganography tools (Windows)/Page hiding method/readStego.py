# This script is able to extract the secret PDF file hidden in other PDF file with writeStego.py in this directory.
# By counting the page references in the page tree it detects how many pages are hidden by  subtraction visible pages
# count. Then hidden part is separated from the whole file and saved in the \\extracted_messages\\ directory.
#
# !!! BE AWARE !!!
# pikepdf library is required.

import glob
import os
import re
from pikepdf import Pdf

filenames = glob.glob('filled_carriers\\*.pdf')
done = 0

for filename in filenames:
    try:
        print(os.path.basename(filename), end=' : ')
        f = open(filename, 'rb')
        content = f.read()
        f.close()
        pageTrees = re.findall(b'<<.*\/Type\s*?\/Pages.*>>', content)
        if len(pageTrees) < 1:
            raise Exception('could not find a page tree')
        for pageTree in pageTrees:
            decoded = pageTree.decode('UTF-8')
            pages = re.search(r'\/Kids\s*?\[.*\]', decoded)
            actualPageCount = len(pages.string[pages.string.find('[') + 1:pages.string.find(
                ']')].split()) // 3  # count /Kids array's element count (each three elements are reference to 1 page)
            countRecord = re.search(r'\/Count\s*(\d*)', decoded)
            fakePageCount = int(countRecord.string[countRecord.span()[0] + 6:countRecord.span()[
                1]])  # /Count parameter's value in PDF file
            stegoPageCount = actualPageCount - fakePageCount
            if stegoPageCount > 0:
                print(stegoPageCount)
            else:
                raise Exception('empty carrier')
            newPageCount = str(actualPageCount)
            countRecord = re.search(r'\/Count\s*(\d*)', decoded)
            newPageTree = countRecord.string[:countRecord.span()[0] + 7] + newPageCount + countRecord.string[
                                                                                          countRecord.span()[1]:]
            # print(countRecord.string)
            # print(newPageTree)
            encoded = newPageTree.encode('UTF-8')
            content = content.replace(pageTree, encoded, 1)
            f = open('tmp.pdf', 'wb')
            f.write(content)
            f.close()
            tmpFile = Pdf.open('tmp.pdf')
            del tmpFile.pages[:fakePageCount]
            try:
                os.mkdir('extracted_messages')
            except:
                pass
            tmpFile.save('extracted_messages/' + os.path.basename(filename)[:-4] + '_extracted.pdf')
            tmpFile.close()
            os.remove('tmp.pdf')
        try:
            os.remove('tmp.pdf')
        except:
            pass

        print('success')
        done += 1
    except Exception as e:
        # print('error')
        print(e)
        pass
print('\n\nSuccesfully extracted from', done, 'of', len(filenames),
      'files (' + str(round(done / len(filenames) * 10000) / 100) + '%)\n---\n')
